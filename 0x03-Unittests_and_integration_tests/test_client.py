#!/usr/bin/env python3
"""Module test_client

This module contains the unit tests for the `access_nested_map` function
from the utils module.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test case for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns the correct value.

        Args:
            nested_map (dict): The nested dictionary to access.
            path (tuple): The sequence of keys to follow.
            expected (any): The expected value.

        Asserts:
            That the value returned by access_nested_map is equal to expected.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == '__main__':
    unittest.main()
