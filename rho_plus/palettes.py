"""Defines a common interface to color palettes used in rho_plus."""

from __future__ import annotations
import abc
from typing import List
import matplotlib.colors as mpl_colors
import numpy as np
from scipy import interpolate as interp
import colour
from colour.utilities import suppress_warnings


class SequentialPaletteMixin(abc.ABC):
    """Mixin for sequential palettes that handles conversion to different formats."""

    @abc.abstractmethod
    def name(self) -> str:
        """The name of the palette."""
        raise NotImplementedError("Subclasses must define a name")

    @abc.abstractmethod
    def hex_colors(self) -> List[str]:
        """Returns a list of hex colors to interpolate between."""
        raise NotImplementedError("Subclasses must implement method hex_colors")

    def rev(self) -> SequentialPaletteMixin:
        """Returns a reversed version of the color palette."""
        return ReversedPalette(self)

    def as_mpl_cmap(self) -> mpl_colors.Colormap:
        """Returns a Matplotlib colormap."""
        return mpl_colors.LinearSegmentedColormap.from_list(
            self.name(), self.hex_colors(), N=len(self.hex_colors())
        )


class ReversedPalette(SequentialPaletteMixin):
    """Reversed color palette."""

    def __init__(self, rev_palette: SequentialPaletteMixin):
        self.rev_palette = rev_palette

    def name(self) -> str:
        return self.rev_palette.name() + "_r"

    def hex_colors(self) -> List[str]:
        return self.rev_palette.hex_colors()[::-1]


class SequentialPalette(SequentialPaletteMixin):
    def __init__(self, name: str, colors: List[str]):
        self._name = name
        self._colors = colors

    @classmethod
    def from_mpl_cmap(cls, cmap: mpl_colors.Colormap):
        """Initializes from a Matplotlib cmap object."""
        return cls(cmap.name, [mpl_colors.to_hex(rgb) for rgb in cmap(range(cmap.N))])

    def name(self) -> str:
        return self._name

    def hex_colors(self) -> List[str]:
        return self._colors


def hex2oklch(hexs):
    with suppress_warnings(colour_usage_warnings=True):
        lchs = []
        if isinstance(hexs, str):
            hexs = [hexs]
        for hex in hexs:
            L, a, b = colour.convert(mpl_colors.to_rgb(hex), "sRGB", "Oklab")
            h = np.rad2deg(np.arctan2(b, a)) % 360
            c = np.hypot(b, a)
            lchs.append(np.array([L, c, h]))

    return np.array(lchs)


def oklch2hex(oklch):
    with suppress_warnings(colour_usage_warnings=True):
        return np.array(
            [
                mpl_colors.to_hex(
                    np.clip(
                        colour.convert(
                            (L, c * np.cos(np.deg2rad(h)), c * np.sin(np.deg2rad(h))),
                            "Oklab",
                            "sRGB",
                        ),
                        0,
                        1,
                    )
                )
                for L, c, h in np.array(oklch).reshape(-1, 3)
            ]
        )


def hex2oklab(hexs):
    with suppress_warnings(colour_usage_warnings=True):
        labs = []
        if isinstance(hexs, str):
            hexs = [hexs]
        for hex in hexs:
            L, a, b = colour.convert(mpl_colors.to_rgb(hex), "sRGB", "Oklab")
            labs.append(np.array([L, a, b]))

        return np.array(labs)


def oklab2hex(oklab):
    with suppress_warnings(colour_usage_warnings=True):
        return np.array(
            [
                mpl_colors.to_hex(np.clip(colour.convert(lab, "Oklab", "sRGB"), 0, 1))
                for lab in np.array(oklab).reshape(-1, 3)
            ]
        )


class OklchPalette(SequentialPaletteMixin):
    """A sequential color palette in Oklch space."""

    def __init__(self, name, keys, hue_cool, nodes=None, correct=True):
        """Keys is a list of colors. Hue_cool is a matching list of Booleans (with first element removed)
        indicating whether the interpolation to that color should go forward (ROYGBIV) or backwards.
        Nodes, if given, is a list of numbers the same length as keys that indicate how they should be spaced.
        (Scaled within [0, 1].)
        If correct, then apply a correction to ensure perceptual uniformity."""

        if isinstance(keys[0], str):
            self.keys = keys
            self.lch_keys = hex2oklch(keys)
        else:
            self.keys = oklch2hex(keys)
            self.lch_keys = [list(key) for key in keys]
        self._name = name

        for i, cool in enumerate(hue_cool):
            # if equal or very close, do nothing
            if abs(self.lch_keys[i][2] - self.lch_keys[i + 1][2]) < 1e-2:
                continue

            # whether the hue will already go forwards
            cool_default = self.lch_keys[i][2] < self.lch_keys[i + 1][2]
            if cool == cool_default:
                # no need to do anything
                pass
            elif cool and not cool_default:
                # hue 2 is smaller than hue 1, but it needs to wrap around the other way
                # add 360 to hue 2
                self.lch_keys[i + 1][2] += 360
            elif not cool and cool_default:
                # hue 2 is larger, but needs to wrap around the other way
                # subtract 360 from second hue
                self.lch_keys[i + 1][2] -= 360

        if nodes is None:
            self.nodes = np.linspace(0, 1, len(keys))
        else:
            self.nodes = (np.array(nodes) - np.min(nodes)) / np.ptp(nodes)

        self.spline = interp.interp1d(self.nodes, self.lch_keys, kind="linear", axis=0)
        self.uncorrected_spline = self.spline
        if correct:
            self.correct()

    def correct(self):
        """Corrects for any perceptual uniformity issues by resampling the colormap."""
        # https://arxiv.org/pdf/1509.03700.pdf
        # at small scales, lightness is the only major factor in perceptual difference
        # so we get the cumulative lightness changes and then resample to evenly space those out

        # cumulative lightness change (now monotonic)
        ll = hex2oklch(self.colors(256))[:, 0]
        abs_ll = np.cumsum(np.abs(np.diff(ll, prepend=0)))

        # interpolate from % of total cumulative lightness to [0, 1] in original
        # only do this if the color scheme has meaningful lightness change
        if np.ptp(ll) > 0.05:
            corr_spline = interp.interp1d(
                (abs_ll - np.min(abs_ll)) / np.ptp(abs_ll),
                np.linspace(0, 1, len(abs_ll)),
                kind="linear",
                axis=0,
            )

            # this spline applied to an evenly-spaced list produces the x
            # required to achieve that equispaced map in the original
            self.spline = lambda x: self.uncorrected_spline(corr_spline(x))

    def colors(self, n):
        """Gets the palette as a list of n colors."""
        return oklch2hex(self.spline(np.linspace(0, 1, n)))

    def hex_colors(self):
        return self.colors(256)

    def name(self):
        return self._name
