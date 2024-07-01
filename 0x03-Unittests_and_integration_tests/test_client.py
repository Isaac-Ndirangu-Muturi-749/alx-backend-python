#!/usr/bin/env python3
"""Module test_client
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized, parameterized_class
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
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

    @patch('client.get_json', return_value=[
           {"name": "repo1"}, {"name": "repo2"}])
    @patch.object(
        GithubOrgClient,
        '_public_repos_url',
        new_callable=unittest.mock.PropertyMock,
        return_value="https://api.github.com/orgs/testorg/repos")
    def test_public_repos(self, mock_url, mock_get_json):
        client = GithubOrgClient("testorg")
        repos = client.public_repos()

        # Assert the returned repositories match the mocked payload
        self.assertEqual(repos, [{"name": "repo1"}, {"name": "repo2"}])

        # Assert that _public_repos_url was called once
        mock_url.assert_called_once()

        # Assert that get_json was called once with the expected URL
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/testorg/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    @patch.object(GithubOrgClient, 'get_json')
    @patch.object(
        GithubOrgClient,
        '_public_repos_url',
        return_value="http://test-url.com")
    def test_has_license(
            self,
            repo,
            license_key,
            expected_result,
            mock_public_repos_url,
            mock_get_json):
        # Mock the get_json method to return a predefined payload
        mock_get_json.return_value = [repo]

        # Create an instance of GithubOrgClient
        client = GithubOrgClient("org_name")

        # Call the has_license method and assert the result
        self.assertEqual(client.has_license(license_key), expected_result)

        # Assert that get_json was called once
        mock_get_json.assert_called_once()


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'), [
        (org_payload, repos_payload, expected_repos, apache2_repos)])
class TestIntegrationGithubOrgClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = cls.mock_get_side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    @classmethod
    def mock_get_side_effect(cls, url):
        if url == 'https://api.github.com/orgs/example-org':
            return Mock(json=lambda: cls.org_payload)
        elif url == 'https://api.github.com/orgs/example-org/repos':
            return Mock(json=lambda: cls.repos_payload)
        else:
            raise ValueError(f"Unexpected URL: {url}")

    def test_public_repos(self):
        client = GithubOrgClient('example-org')
        repos = client.public_repos()

        # or self.apache2_repos, depending on the fixture
        self.assertEqual(repos, self.expected_repos)


if __name__ == '__main__':
    unittest.main()
