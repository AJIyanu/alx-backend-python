#!/usr/bin/env python3
"""generate inatruction by yoirself"""


from typing import List, Tuple, Iterable, Sequence


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """This shit must be inclided"""
    return [(i, len(i)) for i in lst]
