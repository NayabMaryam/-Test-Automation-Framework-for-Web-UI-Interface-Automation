
import sqlite3
from pathlib import Path


class DatabaseReader:

    def __init__(self, database_path):

        self.database_path = Path(database_path)

    def get_connection(self):

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
