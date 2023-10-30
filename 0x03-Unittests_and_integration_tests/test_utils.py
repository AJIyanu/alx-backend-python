#!/usr/bin/env python3
"""unit test for utils.access_nested_map"""

from utils import access_nested_map
import unittest
from parameterized import parameterized
from typing import Mapping, Sequence, Any


class TestAccessNestedMap(unittest.TestCase):
    """unit test for utils.access_nested_map"""

    @parameterized.expand([
                            ({"a": 1}, ("a",), 1),
                            ({"a": {"b": 2}}, ("a",), {'b': 2}),
                            ({"a": {"b": 2}}, ("a", "b"), 2)
        ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence,
                               result: Any) -> None:
        """tests that a nested map returns right value"""
        self.assertEqual(access_nested_map(nested_map, path), result)

    @parameterized.expand([
            ({}, ("a",)),
            ({"a": 1}, ("a", "b"))
        ])
    def test_access_nested_map_exception(self, nest: Mapping, path: Sequence,
                                         err: Any) -> None:
        """tests that function raises assertion"""
        with self.assertRaises(KeyError):
            access_nested_map(nest, path)
