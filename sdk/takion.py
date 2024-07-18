import requests
from settings.config import config
from models.api import UpdateAccount


class TakionAPIClient:
    def __init__(self):
        self.base_url = config.API_BASE_URL
        self.token = config.API_TOKEN

    def get_headers(self):
        return {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
        }

    def update_account(self, user_id: int, data: UpdateAccount):
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

    @classmethod
    def get_account(cls, accounts: list, user_id: str):
        for account in accounts:
            if account.get("user", {}).get("account") == user_id:
                return account
        return None


# example of account data
# {
#     "id":2108,
#     "user":{
#         "id":1175,
#         "username":"IAMB",
#         "first_name":"Yuriy",
#         "last_name":"Bogatov",
#         "account":"34506000",
#         "trainee":false,
#         "status":"M",
#         "trader_status":2,
#         "groups":[
#         {
#             "id":7,
#             "name":"Lexx International"
#         }
#         ]
#     },
#     "max_loss":100,
#     "max_loss_fixed":100,
#     "lock_gain":"None",
#     "max_loss_close":0,
#     "max_loss_close_fixed":0,
#     "lock_gain_auto_close":"None",
#     "pos_loss":0,
#     "pos_loss_fixed":0,
#     "max_loss_symb_close":0,
#     "max_loss_symb_close_fixed":0,
#     "buying_power":0,
#     "fixed_bp":0,
#     "intraday_equity_multiplier":1.0,
#     "day_pos_shares":100000,
#     "day_pos_shares_fixed":100000,
#     "max_pos_open":0,
#     "day_pos_investment":0,
#     "order_size":100000,
#     "order_size_fixed":100000,
#     "min_share_price":0,
#     "max_share_price":1000000,
#     "overnight_bp":0,
#     "max_shares_traded":0,
#     "max_shares_traded_fixed":0,
#     "max_order_investment":5000000,
#     "min_short_price":0.1,
#     "morning_bp":0,
#     "morning_long_inv":0,
#     "morning_short_inv":0,
#     "morning_pos_inv":0,
#     "morning_pos_shares":0,
#     "morning_max_loss":0,
#     "morning_max_loss_symbol":0,
#     "nite_long_inv":0,
#     "nite_short_inv":0,
#     "nite_max_loss":0,
#     "nite_max_loss_symbol":0,
#     "nite_pos_inv":0,
#     "nite_pos_shares":0,
#     "c_aggr_price":18,
#     "options_bp":1000,
#     "option_order_value":100,
#     "option_order_size":5,
#     "option_contracts_open":5,
#     "naked_option_sell":0,
#     "option_limit_price_tolerance":"None",
#     "reject_below_adv":0,
#     "total_house_margin":0,
#     "position_house_margin":0,
#     "max_shares_total":0,
#     "max_shares_total_fixed":0,
#     "options":false,
#     "api":"None"
# }
