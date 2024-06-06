#!/usr/bin/env python3
"""
Module 8-make_multiplier
"""
from typing import Callable

def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    Returns a function that multiplies a float by the given multiplier.
    """
    def multiplier_func(x: float) -> float:
        """
        Multiplies a float by the given multiplier.
        """
        return x * multiplier
    return multiplier_func
