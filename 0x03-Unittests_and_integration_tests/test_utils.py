#!/usr/bin/env python3
"""unit test for utils.access_nested_map"""

from utils import access_nested_map
import unittest
import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """unit test for utils.access_nested_map"""

    @parameterized.expand([
                            ({"a": 1}, ("a",), 1),
                            ({"a": {"b": 2}}, ("a",), {'b': 2}),
                            ({"a": {"b": 2}}, ("a", "b"), 2)
        ])
    def test_access_nested_map(self, nested_map, path, result):
        """tests that a nested map returns right value"""
        self.assertEqual(access_nested_map(nested_map=nested_map, path=path),
                         result)
