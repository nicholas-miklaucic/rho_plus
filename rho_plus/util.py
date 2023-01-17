#!/usr/bin/env python3
"""General utilities."""

import re
from typing import Iterable, Union
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors as mpl_colors


def pd_unique(arr):
    """Like pandas unique in that it preserves sort order.
    Saves having the pandas dependency."""
    idx = np.unique(arr, return_index=True)[1]
    return arr[np.sort(idx)]


def is_curr_dark_bokeh():
    """Determine if the current Bokeh theme is dark.

    Uses figure bgcolor and a simple luminance check."""
    # yadda yadda yadda this is not really correct, no one uses gray as their bgcolor

    import holoviews as hv

    try:
        bgcolor = hv.renderer("bokeh").theme._json["attrs"]["Figure"][
            "background_fill_color"
        ]
    except NameError as e:
        # default white
        bgcolor = "#FFFFFF"

    r, g, b = mpl_colors.to_rgb(bgcolor)
    return (0.2 * r + 0.6 * g + 0.2 * b) <= 0.5


def spread(x, dmin):
    x = np.array(x, copy=False).astype(np.float64)
    if len(x) <= 1:
        return x

    # we need to work on sorted x, but we also need to remember the indices so we can adjust the right ones
    sort_inds = np.argsort(x)
    x_sort = x.copy()[sort_inds]

    dmin = np.broadcast_to(dmin, x.shape)[sort_inds]

    # Minimizing the Total Movement for Movement to Independence Problem on a Line
    # Ghadiri, Yazdanbod 2016
    # https://www.researchgate.net/publication/304641457_Minimizing_the_Total_Movement_for_Movement_to_Independence_Problem_on_a_Line
    # this function does things a little differently, which I think results in clearer code

    slack = np.zeros_like(x_sort, dtype=np.float64)
    adj = np.zeros_like(x_sort, dtype=np.float64)
    for i in range(1, len(x_sort)):
        # previous element's new location is x_sort[i-1] + adj[i-1]
        # move to max(x_sort[i], prev + dmin)

        # dmin = max(dmin[i], dmin[i-1])

        local_dmin = dmin[i] + dmin[i - 1]
        prev = x_sort[i - 1] + adj[i - 1]
        new_x = max(x_sort[i], prev + local_dmin)
        slack[i] = new_x - (prev + local_dmin)
        adj[i] = new_x - x_sort[i]

    new_x = x_sort.copy()
    chains = np.ones_like(new_x)

    for i in range(1, len(new_x)):
        if slack[i] == 0:
            chains[i] = chains[i - 1]
        else:
            chains[i] = chains[i - 1] + 1

    # We break the elements into "chains", groups that are all the minimum distance apart.
    # To start out, we make chains as above, simply checking whether each element is tied
    # to the one before it (because that can be easily computed)

    # This produces incorrect results when some elements move left, thereby entangling more.
    # For example, with dmin = 3 the list [0, 4, 5, 6] is actually all connected, because
    # the chain [4, 5, 6] will become [2, 5, 8] which is within range of 0.

    # To adjust a single chain, we compute the median of the shifts if only rightward shifts
    # are allowed, and subtract that median from each of the shifts.

    # We repeat the following process until convergence:
    # - Adjust each chain independently
    # - If two chains are within the minimum distance of each other, merge them

    def adjust(chains):
        new_x = x_sort.copy()
        for c in np.unique(chains):
            chain_adj = adj[chains == c]
            # chain_adj -= np.max(chain_adj) / 2
            chain_adj -= np.mean(chain_adj)
            # chain_adj -= np.median(chain_adj)

            new_x[chains == c] += chain_adj
        return new_x

    def detach_chains(chains):
        # print(chains)
        for i in range(1, len(chains)):
            if chains[i] == chains[i - 1]:
                detached_chains = chains.copy()
                detached_chains[i] = np.max(detached_chains) + 1
                # print('detach', i, inds[i:], detached_chains)
                if not chain_overlaps(detached_chains).any():
                    # print('success')
                    return detach_chains(detached_chains)
        return chains

    def chain_overlaps(chains):
        adj_x = adjust(chains)

        intervals = []
        for c in pd_unique(chains):
            inds = np.nonzero(chains == c)[0]
            intervals.append(
                (
                    adj_x[inds[0]] - dmin[inds[0]],
                    adj_x[inds[0]],
                    adj_x[inds[-1]],
                    adj_x[inds[-1]] + dmin[inds[-1]],
                )
            )

        # print(intervals)
        overlaps = [False]
        for i in range(1, len(intervals)):
            (lo1, a1, b1, hi1), (lo2, a2, b2, hi2) = intervals[i - 1], intervals[i]
            # overlaps.append(b1 > lo2 or a2 < hi1)
            overlaps.append(hi1 > lo2 or lo2 < hi1)

        return np.array(overlaps)

    overlaps = chain_overlaps(chains)
    # print(chains)
    # print(overlaps)
    while overlaps.any():
        for i in range(1, len(overlaps)):
            if overlaps[i]:
                # print(i, overlaps)
                left, right = np.unique(chains)[i - 1 : i + 1]
                chains[chains == right] = left

        overlaps = chain_overlaps(chains)

    # print(chains)
    chains = detach_chains(chains)
    # print(chains)
    # print(adjust([1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 2, 2]).round(1))
    # print(x_sort.round(1))
    # print(adjust(chains).round(1))
    return adjust(chains)[np.argsort(sort_inds)]


def labelcase(text: Union[str, Iterable[str]]):
    """Converts text to a title case and adds spacing from camel case."""
    if isinstance(text, str):
        if "_" in text:
            # snake_case
            text = text.replace("_", " ")
        return re.sub(r"([^ ])([A-Z])", r"\1 \2", text).title().strip()
    else:
        return [labelcase(t) for t in text]
