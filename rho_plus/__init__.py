from .matplotlib import setup as mpl_setup
from .matplotlib import boxstyle as boxstyle
from .matplotlib import unfill_boxplot as unfill_boxplot
from .matplotlib_tweaks import smart_ticks, line_labels, ylabel_top
from .scatter_label import scatter_labels

try:
    import altair
    from .vega import setup as vega_setup
    from .vega import RHO_LIGHT as vega_rho_light
    from .vega import RHO_DARK as vega_rho_dark
    from .vega import _register_themes

    _register_themes()
except ModuleNotFoundError:
    pass

try:
    import bokeh

    from .bokeh import setup as bokeh_setup
    from .bokeh import rho_light as bokeh_rho_light
    from .bokeh import rho_dark as bokeh_rho_dark
except ModuleNotFoundError:
    pass

try:
    from .panel import ThemedPanel, datagrid, show_json
    from .panel import pn_setup as panel_setup


except ModuleNotFoundError:
    pass

try:
    import plotly
    from .plotly import setup as plotly_setup
    from .plotly import register_themes as _register_themes

    _register_themes()

except ModuleNotFoundError:
    pass

from .sequential_palettes import *
