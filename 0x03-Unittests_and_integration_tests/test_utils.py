#!/usr/bin/env python3
"""unit test for utils.access_nested_map"""

from utils import access_nested_map, get_json, memoize
import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized
from typing import Mapping, Sequence, Any, Dict

try:
    import requests
except ImportError:
    import collections.abc
    collections.MutableMapping = collections.abc.MutableMapping
    collections.Mapping = collections.abc.Mapping
    collections.Iterable = collections.abc.Iterable
    collections.MutableSet = collections.abc.MutableSet
    collections.Callable = collections.abc.Callable
    import requests


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
    def test_access_nested_map_exception(self, nest: Mapping,
                                         path: Sequence) -> None:
        """tests that function raises assertion"""
        with self.assertRaises(KeyError):
            access_nested_map(nest, path)


class TestGetJson(unittest.TestCase):
    """class test getjson function"""

    @parameterized.expand([
            (("http://example.com"), ({"payload": True})),
            (("http://holberton.io"), ({"payload": False}))
        ])
    def test_get_json(self, url: str, tpayload: Dict) -> None:
        """test function returns json payload"""
        with patch.object(requests, "get") as check:
            check.return_value.json.return_value = tpayload
            result = get_json(url)
            check.assert_called_once()
            self.assertEqual(result, tpayload)


class TestMemoize(unittest.TestCase):
    """ tests the memoize decorstor momorize """

    def test_memoize(self) -> None:
        """ calls a function twice but method called once """
        class TestClass:
            
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method",
                return_value=MagicMock(return_value=42)) as check:
            test = TestClass()
            self.assertEqual(test.a_property(), 42)
            self.assertEqual(test.a_property(), 42)
            check.assert_called_once()


if __name__ == '__main__':
    unittest.main()
