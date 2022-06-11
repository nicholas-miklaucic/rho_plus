#!/usr/bin/env python3
"""Vega plot themes as config objects."""

import altair as alt

from .colors import LIGHT_SHADES, DARK_SHADES, LIGHT_COLORS, DARK_COLORS
import colorcet as cc

# define the theme by returning the dictionary of configurations
def rho(is_dark: bool):
    empty, lightest, light, medium, dark, darkest = (
        DARK_SHADES if is_dark else LIGHT_SHADES
    )

    def r():
        return {
            "config": {
                "background": empty,
                "view": {"stroke": "transparent", "autosize": "fit",},
                "axis": {
                    "domain": False,
                    "grid": False,
                    "gridColor": light,
                    "tickColor": medium,
                    "gridWidth": 1,
                    "gridOpacity": 0.7,
                    "labelFont": "sans-serif",
                    "labelFontWeight": 300,
                    "labelFontSize": 14,
                    "labelColor": dark,
                    "titleAnchor": "middle",
                    "titleColor": dark,
                    "titleFont": "sans-serif",
                    "titleFontSize": 16,
                    "titleFontWeight": 400,
                    "titlePadding": 10,
                    "zindex": 0,
                },
                "axisBottom": {"domain": True,},
                "axisLeft": {"titleAngle": 0, "titleAlign": "right", "domain": True,},
                "axisQuantitative": {"tickCount": 6,},
                "legend": {
                    "labelColor": dark,
                    "labelFontWeight": 300,
                    "labelFontSize": 14,
                    "titleColor": darkest,
                    "titleFontWeight": 400,
                    "titleFontSize": 16,
                    "titlePadding": 10,
                    "gridLayout": "all",
                    "fillColor": lightest,
                    "padding": 10,
                    "cornerRadius": 6,
                    "rowPadding": 10,
                },
                "title": {
                    "color": darkest,
                    "font": "sans-serif",
                    "fontSize": 24,
                    "fontWeight": 700,
                    "subtitleColor": darkest,
                    "subtitleFont": "sans-serif",
                    "offset": 20,
                    "anchor": "middle",
                },
                "range": {
                    "category": DARK_COLORS,
                    "diverging": cc.coolwarm,
                    "heatmap": cc.CET_L17,
                    "ordinal": {"scheme": "darkmulti" if is_dark else "lightmulti"},
                    "ramp": cc.CET_L17[-30:30:-1] if is_dark else cc.CET_L17[:60:-1],
                },
            }
        }

    return r


RHO_LIGHT = rho(False)()
RHO_DARK = rho(True)()


def setup(is_dark: bool):
    """Sets up Altair according to the given color scheme."""
    alt.themes.register("rho", rho(is_dark))
    alt.themes.enable("rho")
