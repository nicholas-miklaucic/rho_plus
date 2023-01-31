import numpy as np
import matplotlib as mpl
import scipy.interpolate as interp
import warnings

def srgb2lin(x):
    x = np.array(x)
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', message='invalid value encountered in power')
        return np.where(
            x <= 0.04045,
            x / 12.92,
            ((x + 0.055) / 1.055) ** 2.4)

def lin2srgb(x):
    x = np.array(x)
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', message='invalid value encountered in power')
        return np.where(
            x <= 0.0031308,
            12.92 * x,
            1.055 * x ** (1 / 2.4) - 0.055
        )

m1 = np.array([
    [0.8189330101, 0.3618667424,-0.1288597137],
    [0.0329845436, 0.9293118715, 0.0361456387],
    [0.0482003018, 0.2643662691, 0.6338517070]])

m2 = np.array([
    [0.2104542553, 0.7936177850, -0.0040720468],
    [1.9779984951, -2.4285922050, 0.4505937099],
    [0.0259040371, 0.7827717662, -0.8086757660]])

srgb_m1 = np.array([
    [0.4124, 0.3576, 0.1805],
    [0.2126, 0.7152, 0.0722],
    [0.0193, 0.1192, 0.9505]
])

srgb_minv = np.array([
    [3.2406, -1.5372, -0.4986],
    [-0.9689, 1.8578, 0.0415],
    [0.0557, -0.204, 1.057]
])

lab_lms_m = np.array([
    [1, 0.3963377774, 0.2158037573],
    [1, -0.1055613458, -0.0638541728],
    [1, -0.0894841775, -1.2914855480]
])

lms_rgb_m = np.array([
    [4.0767416621, -3.3077115913, 0.2309699292],
    [-1.2684380046, 2.6097574011, -0.3413193965],
    [-0.0041960863, -0.7034186147, 1.7076147010]
])

def lch2lab(lch):
    l, c, h = np.array(lch).reshape(-1, 3).T
    a = c * np.cos(np.deg2rad(h))
    b = c * np.sin(np.deg2rad(h))
    return np.vstack([l, a, b]).T

def lab2lch(labs):
    l, a, b = np.array(labs).reshape(-1, 3).T
    c = np.hypot(a, b)
    h = np.rad2deg(np.arctan2(b, a)) % 360
    return np.vstack([l, c, h]).T

def lab2lrgb(lab):
    labs = np.array(lab).reshape(-1, 3).T
    lms = (lab_lms_m @ labs) ** 3
    return (lms_rgb_m @ lms).T

def lrgb2lab(lrgb):
    lrgb = np.array(lrgb).reshape(-1, 3).T
    lms = np.cbrt(np.linalg.inv(lms_rgb_m) @ lrgb)
    return (np.linalg.inv(lab_lms_m) @ lms).T

def lrgb2srgb(rgb):
    return lin2srgb(rgb)

def lch2lrgb(lch):
    return lab2lrgb(lch2lab(lch))

def lrgb2lch(lrgb):
    return lab2lch(lrgb2lab(lrgb))

def lch2rgb(lch):
    return lrgb2srgb(lch2lrgb(lch))

def rgb2lch(rgb):
    return lrgb2lch(srgb2lin(rgb))

def to_rgb(c):
    """Converts any matplotlib color to RGB."""
    return np.array(mpl.colors.to_rgb(c))

def to_hsluv(rgb):
    return np.array(hsluv.rgb_to_hsluv(rgb))

def lightness(c):
    """Returns lightness from 0-1"""
    return to_hsluv(to_rgb(c))[..., 2] / 100

def color_is_dark(c):
    return lightness(c) <= 0.5

def _max_c_inner(l, h, tol=0, n=10):
    if l == 1 or l == 0:
        return 0

    cc = np.linspace(0, 0.37, n)

    ll = l * np.ones_like(cc)
    hh = h * np.ones_like(cc)

    lch = np.vstack([ll, cc, hh]).T

    rgbs = lch2lrgb(lch)

    limits = []
    for channel in (0, 1, 2):
        spline = interp.CubicSpline(cc, rgbs[:, channel], bc_type='natural', extrapolate=False)
        zero_sols = spline.solve(tol)
        one_sols = spline.solve(1 - tol)

        diff = spline.derivative()
        zero_below = zero_sols[diff(zero_sols) < 0]
        one_above = one_sols[diff(one_sols) > 0]

        limit = np.concatenate([[np.max(cc)], zero_below, one_above]).min()
        limits.append(limit)

    return np.min(limits)


def max_c(l, h, **kwargs):
    ll, hh = np.broadcast_arrays(l, h)
    return np.array([_max_c_inner(l, h, **kwargs) for l, h in zip(ll.flatten(), hh.flatten())]).reshape(ll.shape)


def lightness_with_ratio(l_bg, l_c=75):
    phi = (1 + np.sqrt(5)) / 2
    # this will warn due to how np.where computes both, ignore
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        return np.where(
            l_bg < 0.5,
            ((l_bg * 100) ** phi + 2 ** (-phi / 2) * (l_c + 35) ** phi) ** (1 / phi),
            ((l_bg * 100) ** phi - 2 ** (-phi / 2) * (l_c + 35) ** phi) ** (1 / phi),
        ) / 100

def to_rgb_arr(colors):
    if isinstance(colors, str):
        return to_rgb(colors)
    elif len(np.array(colors).shape) == 1 and len(np.array(colors)) > 1:
        return to_rgb(colors)
    else:
        return np.array([to_rgb(color) for color in np.array(colors)]).reshape(-1, 3)

def lightness(colors):
    return rgb2lch(to_rgb_arr(colors))[:, 0]

def contrast_l(colors, l_c=75):
    return lightness_with_ratio(lightness(to_rgb_arr(colors)), l_c)

def contrast_with(fg, bg, l_c=75):
    fgs = to_rgb_arr(fg)
    bgs = to_rgb_arr(bg)
    bg_ls = lightness(bgs)

    fg_lch = rgb2lch(fgs)
    old_max_c = max_c(*fg_lch[:, [0, 2]].T)
    old_l = fg_lch[:, 0]
    new_l = contrast_l(bg, l_c)
    # print(old_l, new_l, bg_ls)
    fg_lch[:, 0] = np.where(
        # if background is dark, keep light elements unchanged
        # else, vice versa
        bg_ls < 0.5,
        np.maximum(old_l, new_l),
        np.minimum(old_l, new_l)
    ).clip(0, 1)
    fg_lch[:, 1] = np.clip(fg_lch[:, 1], 0, max_c(*fg_lch[:, [0, 2]].T))
    # fg_lch[:, 1] = fg_lch[:, 1] / old_max_c * max_c(*fg_lch[:, [0, 2]].T)

    rgb = lch2rgb(fg_lch).clip(0, 1).reshape(np.broadcast_shapes(fgs.shape, bgs.shape))
    return rgb
