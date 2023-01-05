#!/usr/bin/env python3
"""General utilities."""

import re
from typing import Iterable, Union
import numpy as np


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

        local_dmin = max(dmin[i], dmin[i-1])
        prev = x_sort[i-1] + adj[i-1]
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
        for c in np.unique(chains):
            chain_adj = adj[chains == c]
            chain_adj -= np.max(chain_adj) / 2
            new_x = x_sort.copy()
            new_x[chains == c] += chain_adj
        return new_x

    def chain_overlaps(chains):
        adj_x = adjust(chains)
        intervals = []
        for c in np.unique(chains):
            inds = np.nonzero(chains == c)[0]            
            intervals.append((
                adj_x[inds[0]] - dmin[inds[0]],
                adj_x[inds[0]], 
                adj_x[inds[-1]],
                adj_x[inds[-1]] + dmin[inds[-1]]))

        # print(intervals)
        overlaps = [False]
        for i in range(1, len(intervals)):
            (lo1, a1, b1, hi1), (lo2, a2, b2, hi2) = intervals[i-1], intervals[i]            
            overlaps.append(b1 > lo2 or a2 < hi1)

        return np.array(overlaps)

    overlaps = chain_overlaps(chains)
    while overlaps.any():    
        # print(chains)
        # print(adjust(chains))
        # print(overlaps)
    
        for i in range(1, len(overlaps)):
            if overlaps[i]:
                print(i, overlaps)
                left, right = np.unique(chains)[i-1:i+1]
                chains[chains == right] = left

        overlaps = chain_overlaps(chains)

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
