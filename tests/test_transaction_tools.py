
import tempfile
from pathlib import Path
from unittest.mock import patch

from pydantic import ValidationError

import database.db as database

from database.db import initialize_database, get_connection

from tools.transaction_tools import (
    get_account_transactions,
    get_spending_summary,
    get_category_spending,
    get_monthly_spending
)


ACCOUNT_REF = "RB-ACC-1002"


def test_successful_transaction_tools():

    print("\n--- Successful Transaction Tool Tests ---")

    results = [
        get_account_transactions.invoke({
            "account_ref": ACCOUNT_REF
        }),
        get_spending_summary.invoke({
            "account_ref": ACCOUNT_REF
        }),
        get_category_spending.invoke({
            "account_ref": ACCOUNT_REF
        }),
        get_monthly_spending.invoke({
            "account_ref": ACCOUNT_REF
        })
    ]

    for result in results:
        assert result["status"] == "success", result

    assert "transactions" in results[0]
    assert "total_spending" in results[1]
    assert "categories" in results[2]
    assert "monthly_spending" in results[3]

    print("All four transaction tools passed.")


def test_invalid_account():

    print("\n--- Invalid Account Test ---")

    result = get_spending_summary.invoke({
        "account_ref": "RB-INVALID-9999"
    })

    assert result["status"] == "account_not_found"

    print("Invalid account handled correctly.")


def test_invalid_date():

    print("\n--- Invalid Date Test ---")

    result = get_spending_summary.invoke({
        "account_ref": ACCOUNT_REF,
        "start_date": "2026-15-40"
    })

    assert result["status"] == "invalid_input"

    print("Invalid date handled correctly.")


def test_inactive_account():

    print("\n--- Inactive Account Test ---")

    with tempfile.TemporaryDirectory() as temp_dir:

        temporary_db = Path(temp_dir) / "test_ready_bank.db"

        # Temporarily redirect database connections.
        with patch.object(database, "DB_PATH", temporary_db):

            initialize_database()

            connection = get_connection()

            try:
                cursor = connection.cursor()

                cursor.execute("""
                    INSERT INTO customers (
                        customer_id,
                        customer_name
                    )
                    VALUES (?, ?)
                """, ("TEST-CUST-001", "Test Customer"))

                cursor.execute("""
                    INSERT INTO accounts (
                        account_ref,
                        customer_id,
                        account_type,
                        status
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    "TEST-ACC-001",
                    "TEST-CUST-001",
                    "Savings",
                    "Inactive"
                ))

                connection.commit()

            finally:
                connection.close()

            result = get_spending_summary.invoke({
                "account_ref": "TEST-ACC-001"
            })

            assert result["status"] == "account_inactive"

    print("Inactive account handled correctly.")
    print("Main project database was not modified.")


def test_missing_account_reference():

    print("\n--- Missing Account Reference Test ---")

    try:
        get_spending_summary.invoke({})
    except ValidationError:
        print("Missing account reference rejected correctly.")
    else:
        raise AssertionError(
            "Missing account reference should fail validation."
        )


if __name__ == "__main__":

    test_successful_transaction_tools()
    test_invalid_account()
    test_invalid_date()
    test_inactive_account()
    test_missing_account_reference()

    print("\nAll transaction tool tests passed.")
