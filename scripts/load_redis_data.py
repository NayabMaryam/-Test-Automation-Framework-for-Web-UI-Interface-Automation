
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.core.config_reader import ConfigReader
from src.data.excel_reader import ExcelReader
from src.data.redis_reader import RedisReader


config = ConfigReader()

excel_reader = ExcelReader(
    PROJECT_ROOT / "test_data" / "test_data.xlsx"
)

redis = RedisReader(
    config.get("redis", "host"),
    config.get("redis", "port"),
    config.get("redis", "db")
)

try:

    login_records = excel_reader.read_data("LoginData")

    for record in login_records:

        key = f"login_{record['username']}"

        redis.store_test_data(key, record)

        print(f"Stored: {key}")

    checkout_records = excel_reader.read_data("CheckoutData")

    for record in checkout_records:

        key = f"checkout_{record['test_case']}"

        redis.store_test_data(key, record)

        print(f"Stored: {key}")

finally:

    redis.close_connection()
