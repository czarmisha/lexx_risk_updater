from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # takion api
    API_BASE_URL: str = "https://api.github.com"
    API_TOKEN: str = "your_token_here"

    # google sheets
    SCOPE: list = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    CREDS_FILE: str = 'path_to_your_credentials.json'  # Путь к вашему JSON файлу с учетными данными
    SPREADSHEET_ID: str = 'your_spreadsheet_id'  # ID вашей Google таблицы
    RANGE_NAME: str = 'Sheet1!A1:Z1000'  # Диапазон данных


config = Config()
