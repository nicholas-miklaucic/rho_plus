#!/usr/bin/env python3
"""Reads a core set of sequential color scales."""

from importlib.resources import open_text
import json
from typing import Mapping
from .palettes import SequentialPalette

SEQUENTIAL_DATA = json.load(open_text("rho_plus.data", "sequential_palettes.json"))
SEQUENTIAL: Mapping[str, SequentialPalette] = {}


def setup_cmaps(data):
    """Creates all of the necessary colormaps."""
    for name, colors in data.items():
        for namespace in (globals(), SEQUENTIAL):
            namespace[name] = SequentialPalette(name, colors)
            namespace[name + '_r'] = SequentialPalette(name, colors).rev()

            namespace["mpl_" + name] = SequentialPalette(name, colors).as_mpl_cmap()
            namespace["mpl_" + name + "_r"] = (
                SequentialPalette(name, colors).rev().as_mpl_cmap()
            )
            namespace["list_" + name] = SequentialPalette(name, colors).hex_colors()
            namespace["list_" + name + "_r"] = (
                SequentialPalette(name, colors).rev().hex_colors()
            )

setup_cmaps(SEQUENTIAL_DATA)

ALIASES = ['sequential', 'diverging', 'heatmap']
def setup_cmap_aliases(is_dark: bool):
    """Sets up theme-agnostic colormap names that map to existing colormaps."""
    if is_dark:
        colormaps = {
            'sequential': SEQUENTIAL_DATA['inferna'],
            'diverging': SEQUENTIAL_DATA['div_icefire_shift'],
            'heatmap': SEQUENTIAL_DATA['candela']
        }
    else:
        colormaps = {
            'sequential': SEQUENTIAL_DATA['inferna'][::-1],
            'diverging': SEQUENTIAL_DATA['div_coolwarm_shift'],
            'heatmap': SEQUENTIAL_DATA['lava']
        }

    setup_cmaps(colormaps)
    return SEQUENTIAL