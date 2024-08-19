import requests
from typing import Dict, Optional
import logging

class APIClient:
    """
    A client for interacting with the employee API.
    
    This class encapsulates the logic for making HTTP requests to the API endpoint.
    It handles authentication and request formatting.
    """

    def __init__(self, url: str, headers: Dict[str, str]):
        """
        Initialize the APIClient with the API URL and headers.

        Args:
            url (str): The base URL of the API endpoint.
            headers (Dict[str, str]): Headers to be sent with each request, typically including authentication tokens.
        """
        self.url = url
        self.headers = headers

    def query_api(self, payload: Dict) -> Optional[Dict]:
        """
        Send a POST request to the API with the given payload.

        This method handles the HTTP request, error checking, and response parsing.
        If the request fails, it logs the error and returns None.

        Args:
            payload (Dict): The request payload containing query parameters.

        Returns:
            Optional[Dict]: The JSON response from the API if successful, None otherwise.

        Raises:
            requests.RequestException: For any network-related errors during the request.
        """
        try:
            # Send POST request to the API
            response = requests.post(self.url, json=payload, headers=self.headers)
            
            # Raise an HTTPError for bad responses (4xx and 5xx status codes)
            response.raise_for_status()
            
            # Parse and return the JSON response
            return response.json()
        except requests.RequestException as e:
            # Log any request-related errors
            logging.error(f"API request failed: {e}")
            return None