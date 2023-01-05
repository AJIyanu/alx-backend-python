#!/usr/bin/env python3
"""carry float, multiply by function"""


from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """muliply me inside me"""

    def mul(times: float) -> float:
        """i am the engine"""
        return multiplier * times
    return mul
