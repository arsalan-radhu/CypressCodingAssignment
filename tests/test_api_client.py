import unittest
from unittest.mock import patch, Mock
import requests
from src.api_client import APIClient

class TestAPIClient(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment before each test method.
        Initialize APIClient with mock URL and headers.
        """
        self.url = "https://api.example.com"
        self.headers = {"Authorization": "Bearer token"}
        self.client = APIClient(self.url, self.headers)

    @patch('src.api_client.requests.post')
    def test_successful_api_query(self, mock_post):
        """
        Test the query_api method with a successful API response.
        
        Mock the requests.post method to return a predefined response.
        Verify that the method returns the expected data.
        """
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {"employees": []}
        mock_post.return_value = mock_response

        # Act
        result = self.client.query_api({})

        # Assert
        self.assertEqual(result, {"employees": []})
        mock_post.assert_called_once_with(self.url, json={}, headers=self.headers)

    @patch('src.api_client.requests.post')
    def test_api_query_http_error(self, mock_post):
        """
        Test the query_api method when an HTTP error occurs.
        
        Mock requests.post to raise an HTTPError.
        Verify that the method returns None and logs the error.
        """
        # Arrange
        mock_post.side_effect = requests.HTTPError("404 Client Error")

        # Act
        result = self.client.query_api({})

        # Assert
        self.assertIsNone(result)

    @patch('src.api_client.requests.post')
    def test_api_query_connection_error(self, mock_post):
        """
        Test the query_api method when a connection error occurs.
        
        Mock requests.post to raise a ConnectionError.
        Verify that the method returns None and logs the error.
        """
        # Arrange
        mock_post.side_effect = requests.ConnectionError("Connection failed")

        # Act
        result = self.client.query_api({})

        # Assert
        self.assertIsNone(result)

    @patch('src.api_client.requests.post')
    def test_api_query_timeout(self, mock_post):
        """
        Test the query_api method when a timeout occurs.
        
        Mock requests.post to raise a Timeout error.
        Verify that the method returns None and logs the error.
        """
        # Arrange
        mock_post.side_effect = requests.Timeout("Request timed out")

        # Act
        result = self.client.query_api({})

        # Assert
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()