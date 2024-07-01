#!/usr/bin/env python3
"""Module test_client
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch.object(GithubOrgClient, 'get_json', return_value={})
    def test_org(self, org_name, mock_get_json):
        client = GithubOrgClient(org_name)

        # Assert get_json is called once with the correct argument
        client.org

        mock_get_json.assert_called_once_with(
            f'https://api.github.com/orgs/{org_name}')

        # Assert org property returns the correct org name
        self.assertEqual(client.org, org_name)

    @parameterized.expand([
        ("google", "https://api.github.com/orgs/google/repos"),
        ("abc", "https://api.github.com/orgs/abc/repos"),
    ])
    @patch.object(GithubOrgClient, 'org', side_effect=lambda x: {"login": x})
    def test_public_repos_url(self, org_name, expected_url, mock_org):
        client = GithubOrgClient(org_name)
        self.assertEqual(client._public_repos_url, expected_url)


if __name__ == '__main__':
    unittest.main()
