#!/usr/bin/env python3
from .bokeh import rho_light, rho_dark
from .bokeh import setup as bokeh_setup
from .matplotlib import setup as mpl_setup
import param
import json
import panel as pn
import warnings
from .util import is_curr_dark_bokeh


def datagrid(df):
    """Renders a DataFrame as an interactive data grid using Perspective.
    Intelligently picks the color theme to use based on the current Matplotlib theme."""
    persp_theme = "material-dense-dark" if is_curr_dark_bokeh() else "material-dense"

    return pn.pane.Perspective(df, theme=persp_theme, sizing_mode="stretch_width")


def show_json(obj):
    """Render JSON (or a JSON-serializable object) as an interactive tree.

    Intelligently picks the color theme to use based on the current Matplotlib theme."""
    json_theme = "dark" if is_curr_dark_bokeh() else "light"

    json_obj = json.dumps(obj, default=lambda o: repr(o))

    return pn.Column(
        pn.pane.JSON(
            json_obj,
            theme=json_theme,
            height=600,
            sizing_mode="stretch_width",
            hover_preview=True,
        ),
        sizing_mode="stretch_width",
        background="#1E1E1E" if json_theme == "dark" else "#FFFFFF",
        scroll=True,
    )


def pn_setup_fonts():
    """Sets up Source Sans 3 in the CSS for Panel."""
    pn.config.raw_css.append(
        """
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,200..900;1,200..900&display=swap');
"""
    )


def pn_setup(is_dark: bool = True, **kwargs):
    """Set up everything for a notebook using Panel, given the color mode to use.
    Replaces a call to pn.extension: pass in kwargs to affect that"""
    try:
        import panel as pn

        pn.extension("perspective", "gridstack", **kwargs)
        pn_setup_fonts()
        bokeh_setup(is_dark)
    except Exception as e:
        warnings.warn("Could not set up Panel: " + str(e))


class ThemedPanel(param.Parameterized):
    colorMode = param.ObjectSelector("dark", ["dark", "light"], precedence=-1)

    def __init__(self):
        super().__init__()
        if "colorMode" in pn.state.session_args:
            self.colorMode = pn.state.session_args["colorMode"][0].decode().lower()
        else:
            try:
                self.colorMode = "dark" if IS_DARK else "light"
            except NameError:
                self.colorMode = "dark"

    @pn.depends("colorMode")
    def colors_theme(self):
        """Returns a (colors, theme) tuple indicating the categorical colors and Bokeh theme."""
        if self.colorMode == "light":
            _theme, colors = mpl_setup(False, False)
        else:
            _theme, colors = mpl_setup(True, False)

        theme = rho_light if self.colorMode == "light" else rho_dark
        return (colors, theme)
