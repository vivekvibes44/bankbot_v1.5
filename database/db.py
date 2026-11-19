
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "ready_bank.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    # Enable foreign key enforcement for this connection.
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # 1. Existing complaints table
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

        # 2. Customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY,
                customer_name TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 3. Accounts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_ref TEXT PRIMARY KEY,
                customer_id TEXT NOT NULL,
                account_type TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Active',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (customer_id)
                    REFERENCES customers(customer_id)
            )
        """)

        # 4. Transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id TEXT PRIMARY KEY,
                account_ref TEXT NOT NULL,
                transaction_date TEXT NOT NULL,
                description TEXT NOT NULL,
                merchant TEXT,
                category TEXT NOT NULL,

                transaction_type TEXT NOT NULL
                    CHECK (
                        transaction_type IN ('Debit', 'Credit')
                    ),

                amount REAL NOT NULL CHECK (amount > 0),

                payment_method TEXT NOT NULL,

                status TEXT NOT NULL
                    CHECK (
                        status IN ('Success', 'Pending', 'Failed')
                    ),

                FOREIGN KEY (account_ref)
                    REFERENCES accounts(account_ref)
            )
        """)

        # 5. Indexes for efficient transaction queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_transactions_account_date
            ON transactions(account_ref, transaction_date)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_transactions_account_category
            ON transactions(account_ref, category)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_accounts_customer
            ON accounts(customer_id)
        """)

        connection.commit()

    finally:
        connection.close()


if __name__ == "__main__":

    initialize_database()

    print("Ready Bank database initialized successfully!")
    print(f"Database location: {DB_PATH}")
