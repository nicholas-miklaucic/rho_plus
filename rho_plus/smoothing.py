import scipy.interpolate as interp
from scipy.optimize import minimize_scalar
import numpy as np
from copy import deepcopy
from scipy.integrate import simpson
import matplotlib.pyplot as plt
import matplotlib as mpl

def overlap_area(pts, lw=1.5, dpi=plt.rcParams['figure.dpi']):
    # get times where the line doubles back on itself
    # double_back_inds = np.where(np.diff(np.sign(np.diff(pts[:, 1]))) > 0)[0]

    # just use all the angles, actually
    double_back_inds = np.arange(0, len(pts) - 2)
    # get triangles corresponding to those jumps
    abcs = pts[double_back_inds.reshape(-1, 1) + np.arange(3), :]
    # normalize so b = 0, doesn't affect anything
    abcs -= abcs[:, [1], :]
    # flip so it's up-down-up and not down-up-down
    # abcs[:, :, 1] *= np.sign(abcs[:, 0, 1]).reshape(-1, 1)
    # overlaps can only exist where both lines are
    # abcs[:, :, [1]] = np.clip(abcs[:, :, [1]], -np.inf, np.median(abcs[:, :, [1]], axis=1, keepdims=True))


    areas = np.abs(np.cross(abcs[:, 2], abcs[:, 0])) / 2
    a_angles = np.arctan2(abcs[:, 0, 1], abcs[:, 0, 0])
    c_angles = np.arctan2(abcs[:, 2, 1], abcs[:, 2, 0])
    angle_between = np.abs(a_angles - c_angles) / 2
    lw_pix = lw / 2  # we want 'radius', not 'diameter'
    lw_pix /= 72  # convert from points to inches
    lw_pix *= dpi  # convert from inches to pixels
    overlap_areas = lw_pix * (lw_pix / np.abs(np.tan(angle_between)))
    overlap_pct = (overlap_areas / areas).clip(0, 1)
    # curve = np.abs(np.diff(interp.CubicSpline(pts[:, 0], pts[:, 1]).derivative()(pts[:, 0]))).mean()
    return overlap_pct.mean()

def convolve_kaiser(pts, M, beta):
    xx = pts[:, 0]
    window = np.kaiser(M, beta)
    window /= np.sum(window)
    pad_start = (M - 1) // 2
    pad_end = (M - 1) // 2
    yy = np.convolve(np.pad(pts[:, 1], (pad_start, pad_end), 'edge'), window, mode='valid')
    return np.vstack([xx, yy]).T

def smooth_noisy_lines(ax=None, keep_old_line=True, max_attempts=50):
    """
    Applies a moving average to smooth out data. ax is the axis on which to do so, defaults to plt.gca().

    max_attempts: the maximum number of times to smooth before stopping. Shouldn't really matter, but
    if you're smoothing very large, very noisy datasets you may want to set this lower.
    """
    if ax is None:
        ax = plt.gca()

    for line in ax.lines:
        pts = line.get_transform().transform(line.get_xydata())

        if len(pts) <= 5:
            # no need to smooth small lines
            continue

        @np.vectorize
        def score_params(beta, window_len):
            """Get the overlap percentage for the choice of β."""
            return overlap_area(convolve_kaiser(pts, window_len, beta), line.get_linewidth(), ax.figure.get_dpi())

        scores = []
        prev_score = 100
        curr_pts = pts
        curr_score = overlap_area(curr_pts, line.get_linewidth(), ax.figure.get_dpi())
        beta_star = 14
        wl_star = int(round(np.sqrt(len(pts)))) + 1
        if wl_star % 2 == 0:
            wl_star -= 1

        while (prev_score - curr_score) >= 1e-3 * abs(prev_score) and len(scores) < max_attempts:
            scores.append(curr_score)
            prev_score = curr_score
            new_pts = convolve_kaiser(curr_pts, wl_star, beta_star)
            curr_score = overlap_area(new_pts, line.get_linewidth(), ax.figure.get_dpi())
            if curr_score < prev_score:
                curr_pts = new_pts
            wl_star += 2
            wl_star = min(wl_star, len(pts) - 3 - (len(pts) % 2))
            beta_star *= 1

        scores.append(curr_score)

        # new_x, new_y = line.get_transform().inverted().transform(convolve_kaiser(pts, wl_star, beta_star)).T
        new_x, new_y = line.get_transform().inverted().transform(curr_pts).T

        if keep_old_line:
            # set alpha low a la Tensorboard
            new_line = mpl.lines.Line2D(new_x, new_y)
            new_line.update_from(line)
            ax.add_line(new_line)
            line.set_alpha(0.2)
        else:
            line.set_xdata(new_x)
            line.set_ydata(new_y)

    return scores


def smooth_straight_lines(ax=None, resample_factor=10):
    """Smooths out lines by applying a spline.

    resample_factor (int): the number of points to plot for each segment of the original line.
    """
    if ax is None:
        ax = plt.gca()

    for line in ax.lines:
        pts = ax.transData.inverted().transform(line.get_xydata())

        xx = np.linspace(pts[:, 0].min(), pts[:, 0].max(), len(pts) * resample_factor)
        spl = interp.PchipInterpolator(pts[:, 0], pts[:, 1])
        yy = spl(xx)

        new_x, new_y = ax.transData.transform(np.vstack([xx, yy]).T).T

        line.set_xdata(new_x)
        line.set_ydata(new_y)

    return ax