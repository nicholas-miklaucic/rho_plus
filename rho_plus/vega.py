#!/usr/bin/env python3
"""Vega plot themes as config objects."""

import altair as alt

from .colors import LIGHT_SHADES, DARK_SHADES, LIGHT_COLORS, DARK_COLORS
from .matplotlib import rho_dark, rho_light
from .matplotlib import setup as mpl_setup
from .sequential_palettes import SEQUENTIAL
import matplotlib.colors


def color_values(theme):
    # more values is closer to the original LCH space, but more data
    return [
        matplotlib.colors.rgb2hex(x)
        for x in theme.as_mpl_cmap()([i / 15 for i in range(16)])
    ]


# define the theme by returning the dictionary of configurations
def rho(is_dark: bool):
    theme, colors = mpl_setup(is_dark, False)
    empty, lightest, light, medium, dark, darkest = (
        DARK_SHADES if is_dark else LIGHT_SHADES
    )

    def r():
        return {
            "config": {
                "background": "#" + theme["figure.facecolor"],
                "numberFormat": ".5~r",
                "range": {
                    "category": colors,
                    "heatmap": color_values(SEQUENTIAL["gouldia"]),
                    "diverging": color_values(
                        SEQUENTIAL[
                            "div_icefire_shift" if is_dark else "div_coolwarm_shift"
                        ]
                    ),
                    "ramp": color_values(SEQUENTIAL["viridia"]),
                },
                "circle": {"size": 100, "fill": colors[0],},
                "square": {"size": 100, "fill": colors[0],},
                "line": {"strokeWidth": 3,},
                "style": {
                    "guide-label": {"fill": dark, "fontWeight": 400, "fontSize": 16,},
                    "guide-title": {
                        "fill": darkest,
                        "fontSize": 20,
                        "fontWeight": 400,
                    },
                    "group-title": {
                        "fill": darkest,
                        "fontSize": 22,
                        "fontWeight": 700,
                    },
                },
                "axis": {
                    "tickFontWeight": 600,
                    "tickColor": dark,
                    "domainColor": dark,
                },
                "axisY": {"titleAngle": 0, "titleAlign": "right"},
                "axisXBand": {"labelAngle": -45},
                "axisQuantitative": {"grid": False},
                "legend": {
                    "labelColor": darkest,
                    "gradientHorizontalMinLength": 200,
                    "gradientHorizontalMaxLength": 1000,
                    "gradientVerticalMinLength": 200,
                    "gradientVerticalMaxLength": 1000,
                },
                "view": {
                    "background": "#" + theme["axes.facecolor"],
                    "stroke": "transparent",
                },
            }
        }

    return r


RHO_LIGHT = rho(False)()
RHO_DARK = rho(True)()


def _register_themes():
    alt.themes.register("rho_dark", rho(True))
    alt.themes.register("rho_light", rho(False))


def setup(is_dark: bool):
    """Sets up Altair according to the given color scheme."""
    alt.themes.enable("rho_dark" if is_dark else "rho_light")
