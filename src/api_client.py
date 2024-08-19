import requests 
from typing import Dict, Optional
import logging

class APIClient:
    def __init__(self, url: str, headers: Dict[str, str]):
        self.url = url
        self.headers = headers

    def query_api(self, payload: Dict) -> Optional[Dict]:
        """
        Query the API with the given payload.
        
        Args:
            payload (Dict): The request payload.
        
        Returns:
            Optional[Dict]: The API response as a dictionary, or None if the request failed.
        """
        try:
            response = requests.post(self.url, json=payload, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"API request failed: {e}")
            return None