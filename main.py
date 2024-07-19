import time
from datetime import datetime as dt

import schedule

from models.api import UpdateAccount
from sdk import DocsAPIClient, TakionAPIClient
from sdk.telegram import telegram


def main(number: int = 1):
    message = f"Running updates for the {number} time at {dt.now().strftime('%Y-%m-%d %H:%M:%S')}"
    print(message)
    telegram.send_message(message)
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

    for row in sheet_data[:2]:
        user_id = row.get("Account")

        if not user_id:
            message = "No Account found in the Google Sheet row"
            print(message)
            telegram.send_message(message)
            continue

        user_id = str(user_id) if isinstance(user_id, int) else user_id

        account = api_client.get_account(accounts, user_id)
        if not account:
            message = f"Account with user_id {user_id} not found in the data from Takion API"
            print(message)
            telegram.send_message(message)
            continue

        new_constraints = {
            "max_loss": row.get(f"max_loss_{number}"),
            "max_loss_close": row.get(f"max_loss_close_{number}"),
            "buying_power": row.get(f"buying_power_{number}"),
        }

        to_delete = []
        for constraint, value in new_constraints.items():
            if value is None:
                message = f"Invalid value for {constraint} in the row"
                print(message)
                telegram.send_message(message)
                continue
            if value == account.get(constraint):
                message = f"Value for {constraint} is already set to {value}"
                print(message)
                to_delete.append(constraint)

        for constraint in to_delete:
            del new_constraints[constraint]

        data = UpdateAccount(**new_constraints)
        api_client.update_account(data, account.get("user", {}).get("id"))

        print(f"Account with user_id {user_id} updated successfully")


if __name__ == "__main__":
    try:
        main()
        # schedule.every().day.at("12:22", "America/New_York").do(main, number=1)
        # schedule.every().day.at("12:23", "America/New_York").do(main, number=2)
        # schedule.every().day.at("12:24", "America/New_York").do(main, number=3)

        # while True:
        #     schedule.run_pending()
        #     time.sleep(1)
    except Exception as e:
        message = f"Error occurred: {str(e)}"
        print(message)
        telegram.send_message(message)
