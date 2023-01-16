#!/usr/bin/env python3
"""Bokeh theme."""

import rho_plus
import matplotlib.pyplot as plt
from bokeh.themes import Theme

themes = []
for is_dark in (True, False):
    _theme, cs = rho_plus.mpl_setup(is_dark)
    theme = plt.rcParams

    font = "'Source Sans 3', sans-serif"
    json = {
        "attrs": {
            "Figure": {
                "background_fill_color": theme["figure.facecolor"],
                "border_fill_color": theme["figure.facecolor"],
                # spine of axis
                "outline_line_color": theme["axes.facecolor"],
            },
            "Grid": {"grid_line_alpha": 0, "minor_grid_line_alpha": 0,},
            "Title": {
                "text_color": theme["axes.titlecolor"],
                "text_font": font,
                "align": "center",
                "text_font_size": "1.4em",
                "text_font_style": "normal",
            },
            "Axis": {
                "major_tick_line_color": theme["xtick.color"],
                "major_tick_line_width": 1,
                "major_tick_out": 10,
                "minor_tick_line_color": theme["xtick.color"],
                "major_label_text_color": theme["xtick.labelcolor"],
                "major_label_text_font": font,
                "major_label_text_font_size": "1.025em",
                "minor_tick_out": 0,
                "axis_label_standoff": 10,
                "axis_label_text_color": theme["axes.labelcolor"],
                "axis_label_text_font": font,
                "axis_label_text_font_size": "1.25em",
                "axis_label_text_font_style": "normal",
            },
            "YAxis": {"major_label_orientation": "horizontal"},
            "Legend": {
                "spacing": 8,
                "glyph_width": 15,
                "label_standoff": 8,
                "label_text_color": theme["legend.labelcolor"],
                "label_text_font_size": "1.025em",
                "border_line_alpha": 1,
                "border_line_color": theme["legend.edgecolor"],
                "background_fill_alpha": 0.25,
                "background_fill_color": theme["axes.facecolor"],
            },
            "ColorBar": {
                "title_text_color": theme["axes.titlecolor"],
                "title_text_font": font,
                "title_text_font_size": "1.025em",
                "background_fill_color": theme["axes.facecolor"],
                "bar_line_alpha": 0,
                "major_label_text_color": theme["xtick.labelcolor"],
                "major_label_text_font": font,
                "major_label_text_font_size": "1.025em",
                "major_tick_line_alpha": 0,
            },
            "Line": {"line_width": 4,},
        }
    }

    themes.append(Theme(json=json))

rho_dark, rho_light = themes


def setup(is_dark):
    theme = rho_dark if is_dark else rho_light
    try:
        import holoviews as hv

        hv.renderer("bokeh").theme = theme
    except ModuleNotFoundError:
        pass
