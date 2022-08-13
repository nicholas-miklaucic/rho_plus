#!/usr/bin/env python3
"""Reads a core set of sequential color scales."""

from importlib.resources import open_text
import json
from typing import Mapping
from .palettes import SequentialPalette

SEQUENTIAL_DATA = json.load(open_text("rho_plus.data", "sequential_palettes.json"))
SEQUENTIAL: Mapping[str, SequentialPalette] = {}

for name, colors in SEQUENTIAL_DATA.items():
    globals()[name] = SequentialPalette(name, colors)
    SEQUENTIAL[name] = SequentialPalette(name, colors)
