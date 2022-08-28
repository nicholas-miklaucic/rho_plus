#!/usr/bin/env python3

import json
from pathlib import Path
from rho_plus import vega_rho_dark, vega_rho_light

for theme, name in zip((vega_rho_dark, vega_rho_light), ("rho_dark", "rho_light")):
    with open(Path.cwd() / "rho_plus" / "data" / f"vega_{name}.json", "w") as f:
        json.dump(theme, f, indent=2)

print("Done!")
