#!/usr/bin/env python3
"""Matplotlib themes as dictionaries."""

from typing import List, Tuple
from .colors import LIGHT_COLORS, DARK_COLORS, LIGHT_SHADES, DARK_SHADES
from .sequential_palettes import SEQUENTIAL

# Colors are taken from BlueprintJS. Background-foreground colors are default in Elastic UI.

rho = {
    # text sizes
    "font.size": 12,
    "axes.labelsize": "large",
    "axes.titlesize": "x-large",
    "figure.titlesize": "xx-large",
    # text weights
    "axes.titleweight": 400,
    "figure.titleweight": 700,
    # if grid is turned on, have it go below plots
    "axes.axisbelow": "false",
    "grid.linestyle": "-",
    "grid.linewidth": 1.0,
    # turn off grid by default
    "axes.grid": "false",
    # turn off ticks on axes
    "xtick.major.size": 0,
    "xtick.minor.size": 0,
    "ytick.major.size": 0,
    "ytick.minor.size": 0,
    # sans-serif by default
    "font.family": "sans-serif",
    # use Computer Modern for LaTeX
    "mathtext.fontset": "cm",
    # turn off right and top spines
    "axes.spines.right": "false",
    "axes.spines.top": "false",
    # set default figure size to a bit more than 6.4 x 4.8
    "figure.figsize": (8, 6),
    # slightly thicker lines by default are easier to see
    "lines.linewidth": 3,
    "image.cmap": "rho_viridia",
}


rho_light = rho.copy()
rho_dark = rho.copy()

for rc, shades in [(rho_light, LIGHT_SHADES), (rho_dark, DARK_SHADES)]:
    empty, lightest, light, medium, dark, darkest = [x[1:] for x in shades]
    rc["figure.facecolor"] = empty
    rc["savefig.facecolor"] = empty
    rc["axes.facecolor"] = empty

    rc["axes.edgecolor"] = light
    rc["grid.color"] = light
    rc["figure.edgecolor"] = light
    rc["savefig.edgecolor"] = light
    rc["legend.edgecolor"] = light
    rc["boxplot.flierprops.color"] = light
    rc["boxplot.boxprops.color"] = light
    rc["boxplot.whiskerprops.color"] = light
    rc["boxplot.capprops.color"] = light

    rc["xtick.color"] = medium
    rc["ytick.color"] = medium

    rc["xtick.labelcolor"] = dark
    rc["ytick.labelcolor"] = dark
    rc["legend.labelcolor"] = dark

    rc["text.color"] = darkest
    rc["axes.labelcolor"] = darkest
    rc["axes.titlecolor"] = darkest


def boxstyle(is_dark=None) -> dict:
    """Returns kwargs that style Matplotlib/Seaborn boxplots to match the theme.
    If filled, then main color is used to fill the box. Otherwise, the box has a border
    but no fill.

    If is_dark is True/False, use that for theming. Otherwise, uses current theme."""
    if is_dark is None:
        import matplotlib.pyplot as plt

        bg = plt.rcParams["axes.facecolor"]
        fg = plt.rcParams["xtick.labelcolor"]
    else:
        empty, _lightest, _light, _medium, dark, _darkest = (
            DARK_SHADES if rho_dark else LIGHT_SHADES
        )
        bg = empty
        fg = dark

    lw = 1.5
    opts = dict(
        medianprops={"color": bg, "lw": lw},
        boxprops={"ec": bg, "lw": lw},
        flierprops={"mfc": fg},
        whiskerprops={"color": fg, "lw": lw},
        capprops={"color": fg, "lw": lw},
    )

    return opts


def unfill_boxplot(ax=None) -> None:
    """Inverts boxplot colors so the borders are the color being plotted and the inner box is empty. Modifies an axis in-place.
    If no axis is given, defaults to current axis."""

    if ax is None:
        import matplotlib.pyplot as plt

        ax = plt.gca()

    for patch in ax.patches:
        patch.set(ec=patch.get_fc())
        patch.set(fill=False)

    for i in range(len(ax.lines) // 6):
        (whis1, whis2, cap1, cap2, median, dunno) = ax.lines[i * 6 : i * 6 + 6]
        for l in (whis1, whis2, cap1, cap2, median):
            l.set_color(ax.patches[i].get_ec())


def setup(is_dark: bool, setup=True) -> Tuple[dict, List[str]]:
    """Sets up Matplotlib according to the given color scheme and pyplot module. Returns the theme and colors as a tuple, setting the theme and colormaps."""
    theme = rho_dark if is_dark else rho_light
    if setup:
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        from matplotlib.colors import LinearSegmentedColormap

        # this annoyingly requires a matplotlib object, so delay until
        # we're confident that matplotlib is installed
        rho_light["axes.prop_cycle"] = mpl.cycler(
            # remove # from color beginning
            color=[x[1:] for x in LIGHT_COLORS]
        )

        rho_dark["axes.prop_cycle"] = mpl.cycler(
            # remove # from color beginning
            color=[x[1:] for x in DARK_COLORS]
        )

        for name, palette in SEQUENTIAL.items():
            cmap = palette.as_mpl_cmap()
            try:
                plt.get_cmap("rho_" + name)
            except ValueError:
                plt.register_cmap(name="rho_" + name, cmap=cmap)

            try:
                plt.get_cmap("rho_" + name + "_r")
            except ValueError:
                plt.register_cmap(name="rho_" + name + "_r", cmap=cmap.reversed())

        # https://github.com/jupyter/notebook/issues/3691

        # Some IPython versions have a bug where Matplotlib styles don't take
        # effect until the plt module is used, not just when it first imports.
        # Clearing the figure is the least intrusive way I can find to trigger
        # this update so the theme will take effect without having to put this
        # in a separate cell from the import.
        plt.clf()

        plt.style.use(theme)

    return (theme, [x["color"] for x in theme["axes.prop_cycle"]])
