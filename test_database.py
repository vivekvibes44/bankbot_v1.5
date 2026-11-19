
from database.db import initialize_database, get_connection, DB_PATH


# Initialize the database
initialize_database()

print("Database initialized successfully.")


# Verify that the complaints table exists
connection = get_connection()

cursor = connection.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
""")

tables = cursor.fetchall()

print("\nAvailable database tables:")

for table in tables:
    print(table["name"])

connection.close()

print(f"\nDatabase location: {DB_PATH}")
