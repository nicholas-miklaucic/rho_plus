#!/usr/bin/env python3

import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
import rho_plus
import json
from pathlib import Path

for theme_name in ("rho_dark", "rho_light"):
    pio.templates.default = theme_name
    fig = go.FigureWidget(px.scatter(x=[1, 2, 3], y=[2, 3, 4]))
    fig.layout.template = pio.templates[theme_name]
    with open(Path.cwd() / "rho_plus" / "data" / f"plotly_{theme_name}.json", "w") as f:
        json.dump(fig.to_plotly_json()["layout"]["template"], f, indent=2)

print("Done!")
