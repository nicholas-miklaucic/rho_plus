"""Matplotlib tweaks to plots that enable more complicated customizations from Matplotlib."""

import textwrap

import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt


def remove_crowded(ax=None):
    """Given an axis, removes the second and penultimate ticks if
    the distance between the final ticks and those are less than half of the
    average distance."""
    if ax is None:
        ax = plt.gca()

    # check in view coordinates to adjust for log axes and the like
    ticks = [ax.get_xticks(), ax.get_yticks()]
    xticklocs = ax.transData.transform(
        np.vstack([ticks[0], np.ones_like(ticks[0]) * ticks[1][0]]).T
    )[:, 0]
    yticklocs = ax.transData.transform(
        np.vstack([np.ones_like(ticks[1]) * ticks[0][0], ticks[1]]).T
    )[:, 1]

    tick_locs_list = [xticklocs, yticklocs]
    for i, tick_locs in enumerate(tick_locs_list):
        meandist = np.diff(tick_locs).mean()
        if tick_locs[1] - tick_locs[0] < 0.5 * meandist:
            ticks[i] = np.array([ticks[i][0], *ticks[i][2:]])

        if tick_locs[-1] - tick_locs[-2] < 0.5 * meandist:
            ticks[i] = np.array([*ticks[i][:-2], ticks[i][-1]])

    ax.set_xticks(ticks[0])
    ax.set_yticks(ticks[1])


def smart_ticks(ax=None, xaxis=True, yaxis=True):
    """Sets the axis limits so they start and end at the minimum and maximum for each axis, a la Tufte."""
    if ax is None:
        ax = plt.gca()

    bboxes = []
    for child in ax.get_children():
        if isinstance(child, mpl.collections.Collection):
            bbox = child.get_datalim(ax.transData)
        elif isinstance(child, mpl.lines.Line2D):
            xdata, ydata = child.get_data()
            if len(xdata):
                bbox = mpl.transforms.Bbox.from_extents(
                    xdata.min(), ydata.min(), xdata.max(), ydata.max()
                )
            else:
                continue
        else:
            continue
        bboxes.append(bbox)

    if not len(bboxes):
        return None

    bbox = mpl.transforms.Bbox.union(bboxes)
    ax.spines["bottom"].set_bounds(bbox.xmin, bbox.xmax)
    ax.spines["left"].set_bounds(bbox.ymin, bbox.ymax)

    # ignore fixed locators, which are often not numeric
    if xaxis and not isinstance(ax.xaxis.get_major_locator(), mpl.ticker.FixedLocator):
        xlabels = ax.xaxis.get_major_formatter().format_ticks([bbox.xmin, bbox.xmax])
        xlabels = [
            xlabels[0],
            *ax.xaxis.get_major_formatter().format_ticks(ax.get_xticks()[1:-1]),
            xlabels[-1],
        ]
        xticks = [bbox.xmin, *ax.get_xticks()[1:-1], bbox.xmax]
        ax.set_xticks(xticks, xlabels)

    if yaxis and not isinstance(ax.yaxis.get_major_locator(), mpl.ticker.FixedLocator):
        ylabels = ax.yaxis.get_major_formatter().format_ticks([bbox.ymin, bbox.ymax])
        ylabels = [
            ylabels[0],
            *ax.yaxis.get_major_formatter().format_ticks(ax.get_yticks()[1:-1]),
            ylabels[-1],
        ]
        yticks = [bbox.ymin, *ax.get_yticks()[1:-1], bbox.ymax]
        ax.set_yticks(yticks, ylabels)

    remove_crowded(ax)


def spread(x, dmin):
    """Returns a shifted x' with minimum total shift such that no two points in x' are within dmin.
    If dmin is array-like, it must be the same shape as x, and notes the minimum space each element
    must have on either side."""
    x = np.array(x, copy=False)
    if len(x) <= 1:
        return x

    # we need to work on sorted x, but we also need to remember the indices so we can adjust the right ones
    sort_inds = np.argsort(x)
    x_sort = x.copy()[sort_inds]

    dmin = np.broadcast_to(dmin, x.shape)[sort_inds]

    # Algorithms for Minimizing the Movements of Spreading Points in Linear Domains
    # Li, Wang 2015
    # https://cccg.ca/proceedings/2015/08.pdf

    def adjust_rightward(x_sort):
        """Returns necessary adjustments if only addition is allowed."""
        adj = np.zeros_like(x_sort, dtype=np.float64)
        for i in range(1, len(x_sort)):
            # previous element's new location is x_sort[i-1] + adj[i-1]
            # move to max(x_sort[i], prev + dmin)

            # dmin = max(dmin[i], dmin[i-1])

            local_dmin = max(dmin[i], dmin[i - 1])
            prev = x_sort[i - 1] + adj[i - 1]
            new_x = max(x_sort[i], prev + local_dmin)
            adj[i] = new_x - x_sort[i]

        return adj

    # The algorithm in Li, Wang solves the problem given, but there's one tweak to the problem
    # specification that we want to make. Specifically, we'd like to add that, if there's no
    # need to move a particular value, we shouldn't.
    # We do this by simply doing adjustments rightward and leftward and seeing if any values
    # are zero in both. These values stay zero in the final adjustments
    adj1 = adjust_rightward(x_sort)
    adj2 = -adjust_rightward(-x_sort[::-1])[::-1]

    no_shift_required = (adj1 == 0) & (adj2 == 0)

    # Li, Wang now moves everything left by half the max movement
    # this produces the minimum maximum shift
    # alternatively, we subtract by the median, which tries to minimize the sum of absolute value of shifts
    # subtracting by mean tries to minimize the sum of squares of shifts

    adj1 -= np.max(adj1) / 2
    # adj1 -= np.median(adj1)
    # adj1 -= np.mean(adj1)

    adj1 = np.where(no_shift_required, 0, adj1)

    # now adjust, going back to indices of original matrix
    return x + adj1[np.argsort(sort_inds)]


def get_handles_labels(ax):
    """Gets a tuple (handles, labels). Accounts for Seaborn's use of phantom lines, so the lines
    will actually have data on the screen."""
    all_handles, labels = ax.get_legend_handles_labels()
    if len(ax.get_lines()) == 2 * len(all_handles):
        # Seaborn does line plots with a legend by first plotting all of the line data,
        # then making another list that same size of phantom lines without data
        handles = ax.get_lines()[: len(ax.get_lines()) // 2]
    else:
        # none of that weirdness
        handles = all_handles

    return handles, labels


def height(text, ax, **kwargs):
    t = ax.text(0.5, 0.5, text, transform=ax.transAxes, **kwargs)
    ax.figure.canvas.draw()
    bb = t.get_window_extent()
    t.remove()
    return bb.height


def line_labels(ax=None, remove_legend=True):
    """Does automatic line labeling, replacing a legend with side labels."""
    if ax is None:
        ax = plt.gca()

    handles, labels = get_handles_labels(ax)
    labels = ["\n".join(textwrap.wrap(label, width=15)) for label in labels]
    data_to_in = mpl.transforms.CompositeGenericTransform(
        ax.transData, ax.figure.dpi_scale_trans.inverted()
    )

    margin = np.array([height(label, ax) for label in labels])

    y_ends = np.array([handle.get_xydata()[-1] for handle in handles])

    spreaded_y_ends = ax.transData.transform(y_ends)
    spreaded_y_ends[:, 1] = spread(spreaded_y_ends[:, 1], margin)
    spreaded_y_ends = ax.transData.inverted().transform(spreaded_y_ends)

    xmax = ax.transData.inverted().transform(
        (ax.transData.transform((y_ends[:, 0].max(), 0))[0] * 1.05, 0)
    )[0]
    for y_end, spreaded, handle, label in zip(y_ends, spreaded_y_ends, handles, labels):
        color = handle.get_color()
        ax.plot([y_end[0], xmax], [y_end[1], spreaded[1]], ls="--", lw=1, c=color)

        ax.text(xmax, spreaded[1], label, ha="left", va="center", color=color)

    if remove_legend:
        ax.legend().remove()


def ylabel_top(ax=None):
    """Moves the y-axis label to the top, wrapping as necessary."""
    if ax is None:
        ax = plt.gca()

    texts = [
        text
        for text in ax.yaxis.get_children()
        if isinstance(text, mpl.text.Text) and text.get_text() == ax.get_ylabel()
    ]

    text = texts[0]
    text.set_visible(False)

    label_wrap = "\n".join(textwrap.wrap(ax.get_ylabel(), width=15))
    ax.text(
        0,
        1.03,
        label_wrap,
        transform=ax.transAxes,
        ha="right",
        va="baseline",
        color=text.get_color(),
        fontproperties=text.get_font_properties(),
    )
