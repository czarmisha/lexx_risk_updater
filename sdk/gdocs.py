import gspread
from settings.config import config


class DocsAPIClient:
    def __init__(self):
        self.creds_file = config.creds_file
        self.spreadsheet_id = config.SPREADSHEET_ID

    def get_google_sheet_data(self):
        client = gspread.service_account(self.creds_file)
        sheet = client.open_by_key(self.spreadsheet_id).sheet1
        data = sheet.get_all_records()
        print(data, "\n")
        return data
