"""Defines a common interface to color palettes used in rho_plus."""

from __future__ import annotations
import abc
from typing import List
import matplotlib.colors as mpl_colors


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
