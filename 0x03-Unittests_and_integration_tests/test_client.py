#!/usr/bin/env python3
"""unit test for client module"""

import utils
from client import GithubOrgClient
import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized
from typing import Mapping, Sequence, Any, Dict
import requests



class TestGithubOrgClient(unittest.TestCase):
    """This class tests the client module
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test the org method of GithubOrgClient"""
        expected_result = {"org": org_name}
        mock_get_json.return_value = expected_result

        client = GithubOrgClient(org_name)
        result = client.org()

        self.assertEqual(result, expected_result)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")



if __name__ == '__main__':
    unittest.main()
