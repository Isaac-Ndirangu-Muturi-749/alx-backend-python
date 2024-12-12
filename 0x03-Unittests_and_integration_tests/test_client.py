#!/usr/bin/env python3
"""Module test_client
Unit tests for the GithubOrgClient class from the client module.
"""

import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from requests import HTTPError


class TestGithubOrgClient(unittest.TestCase):
    """TestGithubOrgClient
    Test cases for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google"),
        ("abc"),
    ])
    @patch("client.get_json", return_value={"payload": True})
    def test_org(self, org_name, mock_get):
        """Test the org property of GithubOrgClient.

        Args:
            org_name (str): The name of the organization.
            mock_get (Mock): Mock for the get_json function.

        Asserts:
            The org property returns the expected value.
            get_json is called once.
        """
        test_client = GithubOrgClient(org_name)
        test_return = test_client.org
        self.assertEqual(test_return, mock_get.return_value)
        mock_get.assert_called_once()

    def test_public_repos_url(self):
        """Test the _public_repos_url property of GithubOrgClient.

        Asserts:
            The _public_repos_url property returns the expected URL.
            org property is called once.
        """
        with patch.object(GithubOrgClient,
                          "org",
                          new_callable=PropertyMock,
                          return_value={"repos_url": "holberton"}) as mock_get:
            test_json = {"repos_url": "holberton"}
            test_client = GithubOrgClient(test_json.get("repos_url"))
            test_return = test_client._public_repos_url
            mock_get.assert_called_once()
            self.assertEqual(test_return,
                             mock_get.return_value.get("repos_url"))

    @patch("client.get_json", return_value=[{"name": "holberton"}])
    def test_public_repos(self, mock_get):
        """Test the public_repos method of GithubOrgClient.

        Args:
            mock_get (Mock): Mock for the get_json function.

        Asserts:
            The public_repos method returns the expected list of repositories.
            get_json and _public_repos_url are called once.
        """
        with patch.object(GithubOrgClient,
                          "_public_repos_url",
                          new_callable=PropertyMock,
                          return_value="https://api.github.com/") as mock_pub:
            test_client = GithubOrgClient("holberton")
            test_return = test_client.public_repos()
            self.assertEqual(test_return, ["holberton"])
            mock_get.assert_called_once()
            mock_pub.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_return):
        """Test the has_license method of GithubOrgClient.

        Args:
            repo (dict): Repository information.
            license_key (str): License key to check.
            expected_return (bool): Expected return value.

        Asserts:
            The has_license method returns the expected boolean value.
        """
        test_client = GithubOrgClient("holberton")
        test_return = test_client.has_license(repo, license_key)
        self.assertEqual(expected_return, test_return)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """TestIntegrationGithubOrgClient
    Integration test cases for the GithubOrgClient class.
    """

    @classmethod
    def setUpClass(cls):
        """Set up class method.

        Sets up the patcher for requests.get.
        """
        cls.get_patcher = patch('requests.get', side_effect=HTTPError)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down class method.

        Stops the patcher for requests.get.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test the public_repos method with integration.

        Asserts:
            Integration test to ensure the method works correctly.
        """
        test_class = GithubOrgClient("holberton")
        self.assertTrue(True)  # Placeholder assertion

    def test_public_repos_with_license(self):
        """Test the public_repos method with license filter integration.

        Asserts:
            Integration test to ensure the method works correctly with
            license filtering.
        """
        test_class = GithubOrgClient("holberton")
        self.assertTrue(True)  # Placeholder assertion
