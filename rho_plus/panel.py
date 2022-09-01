#!/usr/bin/env python3
from .bokeh import rho_light, rho_dark
from .matplotlib import setup as mpl_setup
import param
import panel as pn


def pn_setup_fonts():
    try:
        import panel as pn

        pn.config.raw_css.append(
            """
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');
"""
        )
    except ModuleNotFoundError:
        pass


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
        if self.colorMode == "light":
            _theme, colors = mpl_setup(False, False)
        else:
            _theme, colors = mpl_setup(True, False)

        theme = rho_light if self.colorMode == "light" else rho_dark
        return (colors, theme)
