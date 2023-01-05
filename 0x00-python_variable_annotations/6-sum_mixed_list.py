#!/usr/bin/env python3
"""lets have sum list typed"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[float, int]]) -> float:
    """takes list and return one float"""
    lsum: float = 0
    for i in range(len(mxd_lst)):
        lsum = lsum + mxd_lst[i]
    return lsum
