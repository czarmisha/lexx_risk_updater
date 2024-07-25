import time
from datetime import datetime as dt

import schedule
from pydantic import ValidationError

from models.api import UpdateAccount
from sdk import DocsAPIClient, TakionAPIClient
from sdk.telegram import telegram


def main(number: int = 0):
    column_postfix = number + 1 if number == 0 else number
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
    sheet_data = list(filter(lambda x: x.get("Account"), sheet_data))

    for row in sheet_data:
        user_id = row.get("Account")
        user_id = str(user_id) if isinstance(user_id, int) else user_id

        account = api_client.get_account(accounts, user_id)
        if not account:
            message = f"Account with user_id {user_id} not found in the data from Takion API"
            print(message)
            telegram.send_message(message)
            continue

        new_constraints = {
            "max_loss": row.get(f"max_loss_{number}"),
            "max_loss_close": row.get(f"max_loss_close_{column_postfix}"),
            "buying_power": row.get(f"buying_power_{column_postfix}"),
        }

        to_delete = []
        for constraint, value in new_constraints.items():
            if number == 0 and constraint == "max_loss" and value == 0:
                new_constraints["max_loss"] = row.get(f"max_loss_{number+1}")
                value = row.get(f"max_loss_{number+1}")
            if value is None or value == "#N/A" or value == "":
                message = f"Invalid value for {constraint} in the row"
                print(message)
                to_delete.append(constraint)
                continue
            if value == account.get(constraint):
                message = f"Value for {constraint} is already set to {value}"
                print(message)
                to_delete.append(constraint)

        for constraint in to_delete:
            del new_constraints[constraint]

        try:
            data = UpdateAccount(**new_constraints)
            if not data.model_dump(exclude_none=True):
                message = f"Nothing to update for account {user_id}"
                print(message)
                continue
        except ValidationError as e:
            message = f"Error occurred: typing is wrong for account {user_id} {str(e)}"
            print(message)
            telegram.send_message(message)
            continue
        api_client.update_account(data, account.get("user", {}).get("id"))

        print(f"Account with user_id {user_id} updated successfully")


if __name__ == "__main__":
    try:
        # main()
        # TODO every day but not in holidays
        schedule.every().day.at("07:00", "America/New_York").do(main, number=0)
        schedule.every().day.at("12:23", "America/New_York").do(main, number=1)
        schedule.every().day.at("12:24", "America/New_York").do(main, number=2)

        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        message = f"Error occurred: {str(e)}"
        print(message)
        telegram.send_message(message)
