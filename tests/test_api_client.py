import unittest
from unittest.mock import patch, Mock

import requests
from src.api_client import APIClient

class TestAPIClient(unittest.TestCase):
    def setUp(self):
        self.url = "https://api.example.com"
        self.headers = {"Authorization": "Bearer token"}
        self.client = APIClient(self.url, self.headers)

    @patch('src.api_client.requests.post')
    def test_successful_api_query(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"employees": []}
        mock_post.return_value = mock_response

        result = self.client.query_api({})
        self.assertEqual(result, {"employees": []})

    @patch('src.api_client.requests.post')
    def test_api_query_http_error(self, mock_post):
        mock_post.side_effect = requests.HTTPError("404 Client Error")
        result = self.client.query_api({})
        self.assertIsNone(result)

    @patch('src.api_client.requests.post')
    def test_api_query_connection_error(self, mock_post):
        mock_post.side_effect = requests.ConnectionError("Connection failed")
        result = self.client.query_api({})
        self.assertIsNone(result)

    @patch('src.api_client.requests.post')
    def test_api_query_timeout(self, mock_post):
        mock_post.side_effect = requests.Timeout("Request timed out")
        result = self.client.query_api({})
        self.assertIsNone(result)