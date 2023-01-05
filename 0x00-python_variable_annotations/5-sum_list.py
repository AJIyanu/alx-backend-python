#!/usr/bin/env python3
"""lets have sum list typed"""
from typing import List


def sum_list(input_list: List[float]) -> float:
    """takes list and return one float"""
    lsum: float = 0
    for i in range(len(input_list)):
        lsum = lsum + input_list[i]
    return lsum
