import os

import smartsheet
from dotenv import load_dotenv

load_dotenv()

class SheetAPI:
    def __init__(self):
        self.smart = smartsheet.Smartsheet(os.getenv('SMARTSHEET_TOKEN'))
        self.sheet_id = int(os.getenv('SMARTSHEET_SHEET_ID'))

    def get_row_ids(self) -> list:
        sheet = self.smart.Sheets.get_sheet(self.sheet_id, page_size=1)
        total_rows = sheet.total_row_count
        paged_result = self.smart.Sheets.list_rows(self.sheet_id, page_size=total_rows)
        row_ids = [row.id for row in paged_result.data]
        return row_ids

    def add_row(self, values: list) -> None:
         new_row = smartsheet.models.Row()
        new_row.to_top = True
        new_row.cells.append(smartsheet.models.Cell(value=values[0]))
        new_row.cells.append(smartsheet.models.Cell(value=values[1]))
        new_row.cells.append(smartsheet.models.Cell(value=values[2]))
        self.smart.Sheets.add_rows(self.sheet_id, [new_row])
