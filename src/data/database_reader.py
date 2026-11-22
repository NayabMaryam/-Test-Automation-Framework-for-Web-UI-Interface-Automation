
import sqlite3
from pathlib import Path


class DatabaseReader:

    def __init__(self, database_path):

        self.database_path = Path(database_path)

    def get_connection(self):

        # Create the database directory if it does not exist
        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        return sqlite3.connect(self.database_path)

    def execute_query(self, query, parameters=()):

        connection = self.get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(query, parameters)

            if cursor.description is None:
                connection.commit()
                return []

            columns = [
                description[0]
                for description in cursor.description
            ]

            rows = cursor.fetchall()

            return [
                dict(zip(columns, row))
                for row in rows
            ]

        finally:
            connection.close()

    def initialize_database(self):

        connection = self.get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS test_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_case TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    expected TEXT NOT NULL
                )
            """)

            connection.commit()

        finally:
            connection.close()

    def insert_test_data(
        self,
        test_case,
        username,
        password,
        expected
    ):

        query = """
            INSERT INTO test_data (
                test_case,
                username,
                password,
                expected
            )
            VALUES (?, ?, ?, ?)
        """

        connection = self.get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                query,
                (test_case, username, password, expected)
            )

            connection.commit()

            return cursor.lastrowid

        finally:
            connection.close()  