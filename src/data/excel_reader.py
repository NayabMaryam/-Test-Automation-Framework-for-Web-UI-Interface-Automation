
from pathlib import Path

from openpyxl import load_workbook


class ExcelReader:

    def __init__(self, file_path):

        self.file_path = Path(file_path)

    def read_data(self, sheet_name):

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Excel file not found: {self.file_path}"
            )

        workbook = load_workbook(
            self.file_path,
            data_only=True,
            read_only=True
        )

        try:
            if sheet_name not in workbook.sheetnames:
                raise ValueError(
                    f"Worksheet '{sheet_name}' not found"
                )

            sheet = workbook[sheet_name]

            rows = sheet.iter_rows(values_only=True)

            headers = next(rows, None)

            if not headers or all(header is None for header in headers):
                return []

            headers = [
                str(header).strip() if header is not None else ""
                for header in headers
            ]

            if any(not header for header in headers):
                raise ValueError(
                    "Excel contains an empty column header"
                )

            normalized_headers = [
                header.lower() for header in headers
            ]

            if len(set(normalized_headers)) != len(headers):
                raise ValueError(
                    "Excel contains duplicate column headers"
                )

            data = []

            for row in rows:

                if all(value is None for value in row):
                    continue

                record = dict(zip(headers, row))

                data.append(record)

            return data

        finally:
            workbook.close()
