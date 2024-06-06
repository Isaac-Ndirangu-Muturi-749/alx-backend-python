#!/usr/bin/env python3
"""
Module 102-type_checking
"""

from typing import Tuple, List


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """
    Zooms in on each element in the input tuple by repeating it 'factor' times.

    Args:
        lst: A tuple of integers.
        factor: An integer specifying the zoom factor (default is 2).

    Returns:
        A List containing each element from the input tuple
          repeated 'factor' times.
    """
    zoomed_in: List[int] = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in

if __name__ == "__main__":
    array = (12, 72, 91)

    zoom_2x = zoom_array(array)

    zoom_3x = zoom_array(array, 3)

    print(f"Array: {array}")
    print(zoom_2x)
    print(zoom_3x)
