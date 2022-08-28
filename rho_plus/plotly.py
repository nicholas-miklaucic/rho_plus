#!/usr/bin/env python3
"""Plotly theming."""

import json

import matplotlib as mpl

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

import plotly.graph_objects as go
import numpy as np

from .matplotlib import setup as mpl_setup

from .sequential_palettes import SEQUENTIAL


def register_themes():
    for theme_name, is_dark in zip(("rho_light", "rho_dark"), (False, True)):
        inherit = "plotly_dark" if is_dark else "plotly"
        default = pio.templates[inherit].layout

        templ: go.Layout = go.Layout(default)
        templ.colorscale.sequential = templ.colorscale.sequentialminus = SEQUENTIAL[
            "viridia"
        ].hex_colors()[::17]
        templ.colorscale.diverging = (
            SEQUENTIAL["div_icefire_shift" if is_dark else "div_coolwarm_shift"]
        ).hex_colors()[2:-1:18]

        _theme, cs = mpl_setup(is_dark=is_dark, setup=True)
        rc = mpl.rcParams

        templ.paper_bgcolor = rc["axes.facecolor"]
        templ.plot_bgcolor = rc["axes.facecolor"]
        templ.colorway = cs
        templ.margin = go.layout.Margin(b=20, l=20, r=20, t=30)
        for ax in (
            templ.xaxis,
            templ.yaxis,
            templ.scene.xaxis,
            templ.scene.yaxis,
            templ.scene.zaxis,
        ):
            ax.tickcolor = rc["xtick.color"]
            ax.linecolor = rc["axes.edgecolor"]

            ax.gridcolor = rc["axes.edgecolor"]
            ax.tickfont["color"] = rc["xtick.labelcolor"]
            ax.title.font["color"] = rc["axes.labelcolor"]
            ax.showline = True
            ax.showgrid = False
            ax.mirror = False

        for ax in (templ.scene.xaxis, templ.scene.yaxis, templ.scene.zaxis):
            ax.showgrid = True
            ax.backgroundcolor = rc["axes.facecolor"]

        templ.legend.bgcolor = rc["axes.facecolor"]
        templ.legend.bordercolor = rc["legend.edgecolor"]
        templ.legend.borderwidth = 2
        templ.legend.font.color = rc["legend.labelcolor"]
        templ.legend.title.font.color = rc["axes.labelcolor"]

        # I'm tempted to keep Plotly's default of using the color of the mark for the hover color, but ultimately
        # I think this is more minimal without being any harder to understand: if you hover, you're already
        # looking at the data, so the extra color cue isn't especially necessary
        templ.hoverlabel.bgcolor = rc["axes.facecolor"]
        templ.hoverlabel.bordercolor = rc["axes.edgecolor"]
        templ.hoverlabel.font.color = rc["text.color"]

        data = go.layout.template.Data(
            # https://github.com/plotly/plotly.py/issues/3404
            # I'd rather have filled box plots by default, but Plotly doesn't support altering the default of half-transparency fill color (God only knows why...)
            # so I can't make the fill color just the line color, so my choices are half transparency or transparent
            box=(
                go.Box(
                    marker_line_color=rc["axes.facecolor"],
                    notchwidth=0,
                    fillcolor="rgba(0,0,0,0)",
                ),
            ),
            # same issue as box plots with violin plots: here, we have the fill because otherwise it looks a little too empty
            # I'd rather have a solid meanline, but that's not an option
            violin=(go.Violin(meanline=dict(visible=True)),),
            scatter=(go.Scatter(marker=dict(line=dict(color=rc["axes.facecolor"]))),),
        )
        pio.templates[theme_name] = go.layout.Template(layout=templ, data=data)


def setup(is_dark):
    pio.templates.default = "rho_dark" if is_dark else "rho_light"
