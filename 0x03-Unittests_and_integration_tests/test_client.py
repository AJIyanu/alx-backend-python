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
        (("google"), ({"Paylaod": True})),
        (("abc"), ({"Paylaod": False}))
        ])
    def test_org(self, orgname: str, jsonres: Dict) -> None:
        """test that GithubOrgClient.org returns correct output
           but never calls a real request
        """
        with patch.object(utils, "get_json", return_value=MagicMock()) as check:
            result = GithubOrgClient(orgname)
            result = result.org()
            check.assert_called_once()
            self.assertEqual(result, jsonres)



if __name__ == '__main__':
    unittest.main()
