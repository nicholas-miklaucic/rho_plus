from .matplotlib import setup as mpl_setup

try:
    import altair
    from .vega import setup as vega_setup
    from .vega import RHO_LIGHT as vega_rho_light
    from .vega import RHO_DARK as vega_rho_dark
except ModuleNotFoundError:
    pass

from .sequential_palettes import *
