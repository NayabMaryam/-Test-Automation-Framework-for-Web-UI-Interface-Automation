import pytest

from pathlib import Path

from src.data.excel_reader import ExcelReader


PROJECT_ROOT = Path(__file__).resolve().parents[1]

EXCEL_FILE = PROJECT_ROOT / "test_data" / "test_data.xlsx"


def test_read_login_data():

    reader = ExcelReader(EXCEL_FILE)

    data = reader.read_data("LoginData")

    assert len(data) == 4

    assert data[0]["username"] == "standard_user"

    assert data[0]["expected"] == "success"


def test_read_all_login_records():

    reader = ExcelReader(EXCEL_FILE)

    data = reader.read_data("LoginData")

    for record in data:

        assert record["username"] is not None
        assert record["password"] is not None
        assert record["expected"] in ["success", "failure"]

def test_missing_excel_file():

    reader = ExcelReader("test_data/missing.xlsx")

    with pytest.raises(FileNotFoundError):
        reader.read_data("LoginData")


def test_missing_worksheet():

    reader = ExcelReader(EXCEL_FILE)

    with pytest.raises(ValueError, match="Worksheet"):
        reader.read_data("InvalidSheet")


def test_duplicate_headers():

    # Create a temporary workbook for this test.
    from openpyxl import Workbook

    workbook = Workbook()
    sheet = workbook.active

    sheet.append(["username", "Username"])
    sheet.append(["standard_user", "secret_sauce"])

    file_path = EXCEL_FILE.parent / "duplicate_test.xlsx"

    workbook.save(file_path)
    workbook.close()

    try:
        reader = ExcelReader(file_path)

        with pytest.raises(ValueError, match="duplicate"):
            reader.read_data("Sheet")

    finally:
        file_path.unlink(missing_ok=True)
