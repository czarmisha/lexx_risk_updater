import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='settings/.env', env_file_encoding='utf-8')

    ROOT_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # takion api
    API_BASE_URL: str = "https://api.github.com"
    API_TOKEN: str = "your_token_here"

    # google sheets
    CREDS_FILE_PATH: str = 'path to your creds file'
    SPREADSHEET_ID: str = 'spreadsheet_id_here'

    @property
    def creds_file(self):
        return os.path.join(self.ROOT_DIR, self.CREDS_FILE_PATH)


config = Config()
