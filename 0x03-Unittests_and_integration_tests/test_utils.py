#!/usr/bin/env python3
"""Module test_utils
"""

import unittest
from typing import Mapping, Any, Sequence
from parameterized import parameterized
from utils import access_nested_map

from unittest.mock import patch, Mock
from utils import get_json

from utils import memoize


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
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test case for the get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url: str, test_payload: dict) -> None:
        """
        Test that get_json returns the correct value.

        Args:
            test_url (str): The URL to be passed to get_json.
            test_payload (dict): The expected JSON payload.

        Asserts:
            That the value returned by get_json is equal to test_payload.
        """
        with patch('utils.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test case for the memoize decorator."""

    class TestClass:
        """Class to test the memoize decorator."""

        def a_method(self):
            """Returns a fixed value."""
            return 42

        @memoize
        def a_property(self):
            """Returns the result of a_method, but memoized."""
            return self.a_method()

    def test_memoize(self):
        """Test the memoize decorator."""
        with patch.object(self.TestClass,
                          'a_method') as mock_method:
            test_instance = self.TestClass()
            result1 = test_instance.a_property
            result2 = test_instance.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
