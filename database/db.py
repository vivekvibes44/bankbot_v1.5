
import sqlite3
from pathlib import Path


# Database location
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "ready_bank.db"


def get_connection():
    """
    Create and return a SQLite database connection.
    """

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """
    Create the complaints table if it does not already exist.
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS complaints (

                complaint_id TEXT PRIMARY KEY,

                category TEXT NOT NULL,

                description TEXT NOT NULL,

                status TEXT NOT NULL DEFAULT 'Open',

                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP

            )
        """)

        connection.commit()

    finally:
        connection.close()


if __name__ == "__main__":

    initialize_database()

    print("Ready Bank database initialized successfully!")
    print(f"Database location: {DB_PATH}")
