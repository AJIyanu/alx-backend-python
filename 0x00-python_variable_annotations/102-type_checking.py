#!/usr/bin/env python3
"""assign me safe annotation"""


from typing import List, Tuple


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """imoortant comment herr"""
    zoomed_in: Tuple = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in
