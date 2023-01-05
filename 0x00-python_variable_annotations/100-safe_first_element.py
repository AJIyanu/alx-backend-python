#!/usr/bin/env python3
"""assign me safe annotation"""


from typing import Union, Sequence, Any


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """necessary is commentato"""
    if lst:
        return lst[0]
    else:
        return None
