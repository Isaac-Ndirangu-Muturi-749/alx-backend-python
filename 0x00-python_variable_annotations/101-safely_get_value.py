#!/usr/bin/env python3
"""
Module 101-safely_get_value
"""


from typing import Mapping, Any, Union, TypeVar

T = TypeVar('T')

def safely_get_value(dct: Mapping, key: Any, default: T = None) -> Union[Any, T]:
    """
    Safely retrieves a value from a dictionary.

    Args:
        dct: The dictionary to search.
        key: The key to search for.
        default: The default value to return if the key is not found (defaults to None).

    Returns:
        The value associated with the key if found, otherwise the default value.
    """
    if key in dct:
        return dct[key]
    else:
        return default
