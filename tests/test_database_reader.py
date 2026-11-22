
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

def test_insert_test_data(tmp_path):

    database_path = tmp_path / "test_database.db"

    reader = DatabaseReader(database_path)

    reader.initialize_database()

    record_id = reader.insert_test_data(
        "valid_login",
        "standard_user",
        "secret_sauce",
        "success"
    )

    assert record_id == 1