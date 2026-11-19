
from database.db import get_connection, initialize_database


def test_database_schema():

    initialize_database()

    connection = get_connection()

    try:
        cursor = connection.cursor()

        tables = [
            "complaints",
            "customers",
            "accounts",
            "transactions"
        ]

        print("\n--- Database Schema Verification ---")

        for table in tables:

            cursor.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type = 'table' AND name = ?
            """, (table,))

            result = cursor.fetchone()

            if result:
                print(f"SUCCESS: {table} table exists")

                cursor.execute(f"PRAGMA table_info({table})")

                columns = cursor.fetchall()

                print("Columns:")

                for column in columns:
                    print(f"  - {column['name']}")

            else:
                print(f"FAILED: {table} table not found")

        print("\n--- Index Verification ---")

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'index'
            AND name LIKE 'idx_%'
        """)

        for index in cursor.fetchall():
            print(f"SUCCESS: {index['name']}")

    finally:
        connection.close()


if __name__ == "__main__":
    test_database_schema()
