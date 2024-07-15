import requests
from settings import config
from models.api import UpdateAccount


class TakionAPIClient:
    def __init__(self):
        self.base_url = config.API_BASE_URL
        self.token = config.API_TOKEN

    def get_headers(self):
        return {
            'Authorization': f"Bearer {self.token}",
            'Content-Type': 'application/json'
        }

    def update_account(self, data: UpdateAccount):
        url = f"{self.base_url}/your_endpoint"
        headers = self.get_headers()
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    
    def get_account(self, account_id: int):
        url = f"{self.base_url}/your_endpoint"
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        return response.json()
