from sdk import *


def main():
    docs_api = DocsAPIClient()
    api_client = TakionAPIClient()

    accounts = api_client.get_accounts()  # TODO: Try except
    if not accounts:
        print("No accounts found")
        # TODO: Send to telegram
        return
    
    sheet_data = docs_api.get_google_sheet_data()


if __name__ == "__main__":
    main()
