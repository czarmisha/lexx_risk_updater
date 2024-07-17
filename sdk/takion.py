import requests
from settings.config import config
from models.api import UpdateAccount


class TakionAPIClient:
    def __init__(self):
        self.base_url = config.API_BASE_URL
        self.token = config.API_TOKEN

    def get_headers(self):
        return {
            'Authorization': f"Token {self.token}",
            'Content-Type': 'application/json'
        }

    def update_account(self, user_id: str, data: UpdateAccount):
        url = f"{self.base_url}{user_id}/"
        headers = self.get_headers()
        response = requests.patch(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_accounts(self):
        url = f"{self.base_url}"
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()



# import requests
# import config as cfg


# def get_risk_list() -> list:
#     response: requests.Response = requests.request("GET", cfg.url, headers=cfg.header)
#     response_list: list = response.json()
#     return response_list


# def send_new_trade_level(user_id: int, new_constraints: dict):
#     response: requests.Response = requests.request("PATCH", f'{cfg.url}{user_id}/', headers=cfg.header,
#                                                    json=new_constraints)

#     print(response.text)


# def get_dict_by_account(risk_list: list, account: str) -> dict:
#     for trade_level in risk_list:
#         if trade_level['user']['account'] == account:
#             return trade_level

#     return {}


# def sample():
#     risk_list: list = get_risk_list()
#     my_account: str = '31206519'

#     my_dict: dict = get_dict_by_account(risk_list, my_account)

#     if my_dict == {}:
#         print('Account exists error', my_account)
#         return 0

#     user_id: int = my_dict['user']["id"]
#     new_constraints: dict = {"max_loss_close": 4300}

#     send_new_trade_level(user_id, new_constraints)


# if __name__ == '__main__':
#     sample()
