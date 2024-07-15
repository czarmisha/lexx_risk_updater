import gspread
import pandas as pd
from settings import config
from oauth2client.service_account import ServiceAccountCredentials


class DocsAPIClient:
    def __init__(self):
        self.scope = config.SCOPE
        self.creds_file = config.CREDS_FILE
        self.spreadsheet_id = config.SPREADSHEET_ID
        self.range_name = config.RANGE_NAME

    def get_google_sheet_data(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.creds_file, self.scope)
        client = gspread.authorize(credentials)
        sheet = client.open_by_key(self.spreadsheet_id).sheet1
        data = sheet.get_all_records()
        return pd.DataFrame(data)
