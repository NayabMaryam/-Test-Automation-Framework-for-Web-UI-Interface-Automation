
import sqlite3

from pathlib import Path

from src.data.database_reader import DatabaseReader


def test_database_connection(tmp_path):

    database_path = tmp_path / "test_database.db"

    reader = DatabaseReader(database_path)

    connection = reader.get_connection()

    assert isinstance(connection, sqlite3.Connection)

    assert database_path.exists()

    connection.close()



def test_execute_query(tmp_path):

    database_path = tmp_path / "test_database.db"

    reader = DatabaseReader(database_path)

    reader.execute_query(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT
        )
        """
    )

    reader.execute_query(
        """
        INSERT INTO users (username, password)
        VALUES (?, ?)
        """,
        ("standard_user", "secret_sauce")
    )

    result = reader.execute_query(
        "SELECT * FROM users"
    )

    assert len(result) == 1

    assert result[0]["username"] == "standard_user"

    assert result[0]["password"] == "secret_sauce"


def test_initialize_database(tmp_path):

    database_path = tmp_path / "test_database.db"

    reader = DatabaseReader(database_path)

    reader.initialize_database()

    assert database_path.exists()

    connection = sqlite3.connect(database_path)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table' AND name='test_data'
    """)

    result = cursor.fetchone()

    connection.close()

    assert result is not None

def test_insert_test_data(database):

    record_id = database.insert_test_data(
        "valid_login",
        "standard_user",
        "secret_sauce",
        "success"
    )

    assert record_id == 1

    result = database.get_all_test_data()

    assert len(result) == 1
    assert result[0]["username"] == "standard_user"

def test_get_all_test_data(database):

    database.insert_test_data(
        "valid_login",
        "standard_user",
        "secret_sauce",
        "success"
    )

    database.insert_test_data(
        "invalid_login",
        "invalid_user",
        "wrong_password",
        "failure"
    )

    result = database.get_all_test_data()

    assert len(result) == 2

    assert result[0]["test_case"] == "valid_login"
    assert result[1]["test_case"] == "invalid_login"


def test_get_test_data_by_case(tmp_path):

    database_path = tmp_path / "test_database.db"

    reader = DatabaseReader(database_path)

    reader.initialize_database()

    reader.insert_test_data(
        "valid_login",
        "standard_user",
        "secret_sauce",
        "success"
    )

    result = reader.get_test_data_by_case("valid_login")

    assert len(result) == 1

    assert result[0]["username"] == "standard_user"

    assert result[0]["expected"] == "success"

def test_update_test_data(tmp_path):

    database_path = tmp_path / "test_database.db"

    reader = DatabaseReader(database_path)

    reader.initialize_database()

    reader.insert_test_data(
        "valid_login",
        "standard_user",
        "secret_sauce",
        "success"
    )

    result = reader.update_test_data(
        "valid_login",
        "locked_out_user",
        "secret_sauce",
        "failure"
    )

    assert result == 1

    updated_data = reader.get_test_data_by_case(
        "valid_login"
    )

    assert updated_data[0]["username"] == "locked_out_user"
    assert updated_data[0]["expected"] == "failure"

def test_delete_test_data(tmp_path):

    database_path = tmp_path / "test_database.db"

    reader = DatabaseReader(database_path)

    reader.initialize_database()

    record_id = reader.insert_test_data(
        "login_test",
        "standard_user",
        "secret_sauce",
        "success"
    )

    deleted_rows = reader.delete_test_data(record_id)

    assert deleted_rows == 1

    result = reader.get_all_test_data()

    assert len(result) == 0

def test_delete_nonexistent_test_data(tmp_path):

    database_path = tmp_path / "test_database.db"

    reader = DatabaseReader(database_path)

    reader.initialize_database()

    deleted_rows = reader.delete_test_data(999)

    assert deleted_rows == 0