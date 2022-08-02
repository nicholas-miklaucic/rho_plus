#!/usr/bin/env python3
"""Defines a core set of sequential color scales."""

from .palettes import OklchPalette, SequentialPaletteMixin

# aesthetic colormaps: sacrifice resolution for harmony
rosa = OklchPalette(
    "rosa", [(0.45, 0.2, 320), (0.6, 0.22, 350), (0.65, 0.2, 10)], [True, True]
)
frutta = OklchPalette("frutta", [(0.45, 0.23, 312), (0.8, 0.14, 50)], [True])
glacia = OklchPalette("glacia", [(0.35, 0.15, 240), (0.65, 0.15, 140)], [False])
ignia = OklchPalette("ignia", [(0.4, 0.2, 35), (0.75, 0.2, 85)], [True])

# linear colormaps: workhorses for representing continuous ordinal data
# vetted for use in scatterplots against dark or light backgrounds
inferna = OklchPalette("inferna", [(0.34, 0.2, 260), (0.8, 0.2, 100)], [True])
viridia = OklchPalette("viridia", [(0.34, 0.15, 300), (0.8, 0.15, 100)], [False])

# spans a very large range of luminances: useful for heatmaps/as background
umbra = OklchPalette("umbra", [[0.15, 0.25, 260], [0.98, 0.1, 80]], [True])
gouldia = OklchPalette(
    "gouldia", [[0.16, 0.1, 300], [0.57, 0.2, 180], [0.98, 0.1, 60]], [False]
)

# diverging colormaps
spectra_diverge = OklchPalette(
    "spectra_diverge",
    [(0.4, 0.15, 20), (0.96, 0.23, 112), (0.4, 0.15, 330)],
    [True, True],
)
coolwarm = OklchPalette(
    "rho_coolwarm",
    [(0.4, 0.2, 15), (0.9, 0, 15), (0.9, 0, 270), (0.4, 0.29, 270)][::-1],
    [True, True, True],
    (0, 0.4999, 0.5001, 1),
)
icefire = OklchPalette(
    "rho_icefire",
    [(0.7, 0.2, 15), (0.1, 0.07, 15), (0.1, 0.07, 270), (0.7, 0.2, 270)][::-1],
    [True, True, True],
    (0, 0.4999, 0.5001, 1),
)

# isoluminant colormap: the linear colormaps are already fine for scatterplots, so these aren't that necessary
# sacrifices a lot of resolution
# use for very large numbers of categories where visual prominence is an issue
iso_spectra = OklchPalette("iso_spectra", [[0.65, 0.15, 10], [0.65, 0.15, 320]], [True])
iso_glacia = OklchPalette("iso_glacia", [(0.55, 0.1, 260), (0.55, 0.1, 130)], [False])
iso_frutta = OklchPalette("iso_frutta", [(0.65, 0.2, 312), (0.65, 0.2, 40)], [True])


# rainbow, because everyone needs one
# unlike the diverging version, the center is not the maximum lightness: this adjustment lets the hue gradient be more even
spectra = OklchPalette(
    "spectra", [(0.65, 0.2, 10), (0.96, 0.2, 120), (0.4, 0.2, 315)], [True, True]
)

for key in list(globals()):
    if isinstance(globals()[key], SequentialPaletteMixin):
        globals()["cm_" + key] = globals()[key]
        globals()["mpl_" + key] = globals()[key].as_mpl_cmap()
