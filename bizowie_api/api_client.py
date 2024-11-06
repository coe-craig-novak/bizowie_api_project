import requests
import json
import os

# Module: api_client.py
class BizowieAPI:
    def __init__(self, base_url):
        """
        Initialize BizowieAPI with base URL.
        
        :param base_url: Base URL for the Bizowie API.
        """
        self.base_url = base_url
        self.api_key = os.getenv("bizowie_api_key")
        self.secret_key = os.getenv("bizowie_secret_key")
        self.headers = {
            'Content-Type': 'application/json'
        }
    
    def _post_request(self, endpoint, body):
        """
        Generic POST request for Bizowie API.
        
        :param endpoint: API endpoint to be appended to the base URL.
        :param body: Request body as a dictionary.
        :return: JSON response from the API.
        """
        url = f"{self.base_url}/{endpoint}"
        body.update({
            'api_key': self.api_key,
            'secret_key': self.secret_key
        })
        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(body))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error during {endpoint} request: {e}")
            return None