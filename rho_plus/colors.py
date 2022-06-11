#!/usr/bin/env python3
"""Colors used across themes."""
# colors from https://blueprintjs.com/docs/#core/colors

# intended to approximate the standard ordering found in cat10 or similar. For
# my purposes, it's rare that you're using all of them and that you need maximum
# visual clarity. What's more common is using a couple colors or using them
# redundantly. If you want maximum discernability, use Glasbey from colorcet.

# An example of this tradeoff: blue and orange are the easiest pair to tell
# apart, which is why you see them in Rocket League or Splatoon or similar games
# with teams. But blue and green look much nicer as the only two colors in a
# plot, and they're still discernible with most forms of colorblindness. So blue
# and green are the first pair, and then orange is the third color.

LIGHT_COLORS = [
    "#215DB0",
    "#1C6E42",
    "#935610",
    "#B83211",
    "#7C327C",
    "#0F6894",
    "#634DBF",
    "#5A701A",
    "#C22762",
    "#866103",
]

DARK_COLORS = [
    "#4C90F0",
    "#32A467",
    "#EC9A3C",
    "#EB6847",
    "#BD6BBD",
    "#3FA6DA",
    "#9881F3",
    "#B6D94C",
    "#F5498B",
    "#F0B726",
]

# the neutrals are from https://elastic.github.io/eui/#/theming/colors
# the naming is from a light-scheme perspective

LIGHT_SHADES = [
    # empty shade: primary background
    "#FFFFFF",
    # lightest shade: secondary background
    "#F0F4FB",
    # light shade: borders and dividers
    "#D3DAE6",
    # medium shade: subdued text
    "#98A2B3",
    # dark shade: secondary foreground
    "#69707D",
    # darkest shade: primary foreground, text
    "#343741",
]

DARK_SHADES = [
    # empty shade: primary background
    "#1D1E24",
    # lightest shade: secondary background
    "#25262E",
    # light shade: borders and dividers
    "#343741",
    # medium shade: subdued text
    "#535966",
    # dark shade: secondary foreground
    "#98A2B3",
    # darkest shade: primary foreground, text
    "#D4DAE5",
]
