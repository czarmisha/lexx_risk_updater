import time
from datetime import datetime as dt

import schedule

from models.api import UpdateAccount
from sdk import DocsAPIClient, TakionAPIClient
from sdk.telegram import telegram


def main(number: int = 1):
    print(f"Running the main function for the {number} time at {dt.now().strftime('%Y-%m-%d %H:%M:%S')}")
    docs_api = DocsAPIClient()
    api_client = TakionAPIClient()

    accounts = api_client.get_accounts()
    if not accounts:
        message = "No accounts fetched from the Takion API"
        print(message)
        telegram.send_message(message)
        return

    sheet_data = docs_api.get_google_sheet_data()
    if not sheet_data:
        message = "No data fetched from the Google Sheet"
        print(message)
        telegram.send_message(message)
        return

    for row in sheet_data:
        user_id = row.get("Account")
        if not user_id:
            message = "No Account found in the Google Sheet row"
            print(message)
            telegram.send_message(message)
            continue

        account = api_client.get_account(accounts, user_id)
        if not account:
            message = f"Account with user_id {user_id} not found in the data from Takion API"
            print(message)
            telegram.send_message(message)
            continue

        new_constraints = {
            "max_loss_close": row.get(f"max_loss_close_{number}"),
            "max_loss_open": row.get(f"max_loss_open_{number}"),
            "max_profit_close": row.get(f"max_profit_close_{number}"),
            "max_profit_open": row.get(f"max_profit_open_{number}"),
        }

        for constraint, value in new_constraints.items():
            if value is None:
                message = f"Invalid value for {constraint} in the row"
                print(message)
                telegram.send_message(message)
                continue
            if value == account.get(constraint):  # TODO: check types
                message = f"Value for {constraint} is already set to {value}"
                print(message)
                del new_constraints[constraint]

        data = UpdateAccount(**new_constraints)
        api_client.update_account(account.get("user_id"), data)

        print(f"Account with user_id {user_id} updated successfully")


if __name__ == "__main__":
    schedule.every().day.at("12:22", "America/New_York").do(main, number=1)
    schedule.every().day.at("12:23", "America/New_York").do(main, number=2)
    schedule.every().day.at("12:24", "America/New_York").do(main, number=3)

    while True:
        schedule.run_pending()
        time.sleep(1)
