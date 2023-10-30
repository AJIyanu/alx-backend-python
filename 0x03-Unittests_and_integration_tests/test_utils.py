#!/usr/bin/env python3
"""unit test for utils.access_nested_map"""

from utils import access_nested_map
import  unittest
import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """unit test for utils.access_nested_map"""

    @parameterized.expand
    def test_access_nested_map(self):
        """tests that a nested map returns right value"""
