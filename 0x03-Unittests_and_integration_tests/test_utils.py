#!/usr/bin/env python3
"""Module test_utils
"""

import unittest
from typing import Mapping, Any, Sequence
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test case for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self,
                               nested_map: Mapping[str, Any],
                               path: Sequence[str],
                               expected: Any) -> None:
        """
        Test that access_nested_map returns the correct value.

        Args:
            nested_map (Mapping): The nested dictionary to access.
            path (Sequence): The sequence of keys to follow.
            expected (Any): The expected value.

        Asserts:
            That the value returned by access_nested_map is equal to expected.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self,
                                         nested_map: Mapping[str, Any],
                                         path: Sequence[str]) -> None:
        """
        Test that access_nested_map raises a KeyError for invalid paths.

        Args:
            nested_map (Mapping): The nested dictionary to access.
            path (Sequence): The sequence of keys to follow.

        Asserts:
            That access_nested_map raises a KeyError for invalid paths.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), str(path[-1]))


if __name__ == '__main__':
    unittest.main()
