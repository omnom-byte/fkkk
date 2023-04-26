python
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import config

class GoogleSheetsAPI:
    def __init__(self, credentials_file, spreadsheet_name):
        self.credentials_file = credentials_file
        self.spreadsheet_name = spreadsheet_name
        self.auth = self._authorize()
        self.gs = self.auth.open(self.spreadsheet_name)

    def _authorize(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
        auth = gspread.authorize(credentials)
        return auth

    def update_spreadsheet(self, data):
        sheet = self.gs.sheet1
        row = [data['timestamp'], data['symbol'], data['action'], data['price'], data['quantity'], data['fee'], data['balance']]
        sheet.append_row(row)
