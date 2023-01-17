#!/usr/bin/env python3
"""Reads a core set of sequential color scales."""

from importlib.resources import open_text
import json
from typing import Mapping
from .palettes import SequentialPalette

SEQUENTIAL_DATA = json.load(open_text("rho_plus.data", "sequential_palettes.json"))
SEQUENTIAL: Mapping[str, SequentialPalette] = {}

for name, colors in SEQUENTIAL_DATA.items():
    for namespace in (globals(), SEQUENTIAL):
        namespace[name] = SequentialPalette(name, colors)
        namespace["mpl_" + name] = SequentialPalette(name, colors).as_mpl_cmap()
        namespace["mpl_" + name + "_r"] = (
            SequentialPalette(name, colors).rev().as_mpl_cmap()
        )
        namespace["list_" + name] = SequentialPalette(name, colors).hex_colors()
        namespace["list_" + name + "_r"] = (
            SequentialPalette(name, colors).rev().hex_colors()
        )
