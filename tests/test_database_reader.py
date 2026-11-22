
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
