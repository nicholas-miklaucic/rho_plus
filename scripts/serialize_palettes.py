"""Defines the color palettes and serializes them into lists of RGB hex codes
for use without heavyweight color library imports. Requires the dev
dependencies.

See the showcase for explanations of when using each palette is appropriate.
"""
from rho_plus.oklch_palettes import OklchPalette
from rho_plus.palettes import SequentialPaletteMixin
import json
from pathlib import Path


print("Serializing color palettes...")

# aesthetic colormaps: sacrifice resolution for harmony
solara = OklchPalette("solara", [(0.45, 0.2, 310), (0.75, 0.05, 120)], [True])
frutta = OklchPalette("frutta", [(0.45, 0.23, 312), (0.8, 0.14, 60)], [True])
glacia = OklchPalette("glacia", [(0.35, 0.15, 240), (0.65, 0.15, 140)], [False])
ignia = OklchPalette("ignia", [(0.4, 0.2, 35), (0.75, 0.2, 85)], [True])

# linear colormaps: workhorses for representing continuous ordinal data
# vetted for use in scatterplots against dark or light backgrounds
inferna = OklchPalette("inferna", [(0.34, 0.2, 260), (0.8, 0.2, 100)], [True])
viridia = OklchPalette("viridia", [(0.34, 0.15, 300), (0.8, 0.15, 100)], [False])

# spans a very large range of luminances: useful for heatmaps/as background
umbra = OklchPalette(
    "umbra", [[0.15, 0.089, 265], [0.565, 0.2, 318], [0.98, 0.089, 111]], [True, True]
)

gouldia = OklchPalette(
    "gouldia", [[0.16, 0.1, 300], [0.57, 0.2, 180], [0.98, 0.1, 60]], [False]
)

# diverging colormaps
div_spectra = OklchPalette(
    "div_spectra",
    [(0.4, 0.2, 330), (0.96, 0.2, 120), (0.4, 0.2, 27)],
    [False, False],
    correct="gauss",
)

div_coolwarm = OklchPalette(
    "div_coolwarm",
    [(0.4, 0.2, 15), (0.9, 0, 15), (0.9, 0, 270), (0.4, 0.29, 270)][::-1],
    [True, True, True],
    (0, 0.4999, 0.5001, 1),
    correct="gauss",
)

div_coolwarm_shift = OklchPalette(
    "div_coolwarm_shift",
    [(0.4, 0.2, 15), (0.9, 0, 75), (0.9, 0, 210), (0.4, 0.29, 270)][::-1],
    [False, False, False],
    (0, 0.4999, 0.5001, 1),
    correct="gauss",
)

div_icefire = OklchPalette(
    "div_icefire",
    [(0.7, 0.2, 15), (0.1, 0.07, 15), (0.1, 0.07, 270), (0.7, 0.2, 270)][::-1],
    [True, True, True],
    (0, 0.4999, 0.5001, 1),
    correct="gauss",
)

div_icefire_shift = OklchPalette(
    "div_icefire_shift",
    [(0.8, 0.2, 180), (0.2, 0.05, 270), (0.2, 0.05, 330), (0.8, 0.15, 60)],
    [True, True, True],
    (0, 0.4999, 0.5001, 1),
    correct="gauss",
)

# isoluminant colormap: the linear colormaps are already fine for scatterplots, so these aren't that necessary
# sacrifices a lot of resolution
# use for very large numbers of categories where visual prominence is an issue
iso_spectra = OklchPalette(
    "iso_spectra", [[0.65, 0.15, 330], [0.65, 0.15, 27]], [False]
)
iso_glacia = OklchPalette("iso_glacia", [(0.55, 0.1, 260), (0.55, 0.1, 130)], [False])
iso_frutta = OklchPalette("iso_frutta", [(0.65, 0.2, 312), (0.65, 0.2, 40)], [True])


# rainbow, because everyone needs one
# unlike the diverging version, the center is not the maximum lightness: this adjustment lets the hue gradient be more even
spectra = OklchPalette(
    "spectra",
    [(0.3, 0.2, 330), (0.96, 0.2, 120), (0.53, 0.2, 27)],
    [False, False],
    [0, 210, 300],
    correct="gauss",
)

SEQUENTIAL = []
for key in list(globals()):
    if isinstance(globals()[key], SequentialPaletteMixin):
        SEQUENTIAL.append(key)
        # globals()["cm_" + key] = globals()[key]
        # globals()["mpl_" + key] = globals()[key].as_mpl_cmap()

json_obj = {}
for key in sorted(SEQUENTIAL):
    json_obj[globals()[key].name()] = list(globals()[key].hex_colors())

with open(Path.cwd() / "rho_plus" / "data" / "sequential_palettes.json", "w") as f:
    json.dump(json_obj, f, indent=2)

print("Done!")
