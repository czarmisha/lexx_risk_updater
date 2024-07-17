from sdk import *


def main():
    docs_api = DocsAPIClient()
    api_client = TakionAPIClient()

    sheet_data = docs_api.get_google_sheet_data()

    # for index, row in df.iterrows():
    #     data = row.to_dict()
    #     response = api_client.send_request(endpoint="your_endpoint", data=data)
    #     print(f"Response for row {index}: {response}")

if __name__ == "__main__":
    main()
