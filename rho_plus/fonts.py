#!/usr/bin/env python3
"""Provides infastructure for font selection in Rho+."""

from importlib.resources import path


def mpl_add_fonts():
    """Configures Matplotlib to add Source Sans 3."""
    import matplotlib.font_manager as fm

    fonts = ["SourceSans3-Regular.ttf", "SourceSans3-Bold.ttf"]
    for f in fonts:
        with path("rho_plus.data.fonts", f) as ttf:
            fm.fontManager.addfont(ttf)
