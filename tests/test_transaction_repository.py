
import math

from database.transaction_repository import (
    get_customers,
    get_customer_accounts,
    get_transactions,
    get_total_spending,
    get_category_spending,
    get_monthly_spending
)


ACCOUNT_REF = "RB-ACC-1002"


def test_customer_and_account_retrieval():
    print("\n--- Customer and Account Verification ---")

    customers = get_customers()

    assert len(customers) > 0, "No customers found."

    accounts = get_customer_accounts("RB-CUST-001")

    assert len(accounts) > 0, "No accounts found for RB-CUST-001."

    print("Customers:", len(customers))
    print("Accounts:", len(accounts))


def test_transaction_retrieval():
    print("\n--- Transaction Retrieval ---")

    transactions = get_transactions(ACCOUNT_REF, limit=1000)

    assert len(transactions) > 0, "No transactions found."

    print("Total transactions:", len(transactions))

    # Verify transaction limit.
    limited_transactions = get_transactions(
        ACCOUNT_REF,
        limit=5
    )

    assert len(limited_transactions) <= 5
    assert len(limited_transactions) == min(5, len(transactions))

    print("Transaction limit test passed.")

    # Verify category filtering.
    category = transactions[0]["category"]

    category_transactions = get_transactions(
        ACCOUNT_REF,
        category=category,
        limit=1000
    )

    assert len(category_transactions) > 0
    assert all(
        transaction["category"] == category
        for transaction in category_transactions
    )

    print("Category filter test passed.")


def test_date_range_filter():
    print("\n--- Date Range Filtering ---")

    start_date = "2026-09-01"
    end_date = "2026-11-30"

    transactions = get_transactions(
        ACCOUNT_REF,
        start_date=start_date,
        end_date=end_date,
        limit=1000
    )

    assert all(
        start_date <= transaction["transaction_date"][:10] <= end_date
        for transaction in transactions
    ), "A transaction was returned outside the requested date range."

    print("Filtered transactions:", len(transactions))
    print("Date range test passed.")


def test_spending_calculations():
    print("\n--- Spending Calculation Verification ---")

    transactions = get_transactions(
        ACCOUNT_REF,
        limit=1000
    )

    spending = get_total_spending(ACCOUNT_REF)

    # Independently calculate expected spending from retrieved transactions.
    successful_debits = [
        transaction
        for transaction in transactions
        if transaction["transaction_type"] == "Debit"
        and transaction["status"] == "Success"
    ]

    expected_total = sum(
        transaction["amount"]
        for transaction in successful_debits
    )

    expected_count = len(successful_debits)

    assert math.isclose(
        spending["total_spending"],
        expected_total,
        abs_tol=0.01
    ), "Total spending does not match successful debit transactions."

    assert spending["transaction_count"] == expected_count, (
        "Spending transaction count does not match successful debits."
    )

    print("Total spending:", spending["total_spending"])
    print("Successful debit count:", spending["transaction_count"])
    print("Successful debit calculation test passed.")

    # Verify category-wise totals reconcile with overall spending.
    categories = get_category_spending(ACCOUNT_REF)

    category_total = sum(
        item["total_spending"]
        for item in categories
    )

    category_count = sum(
        item["transaction_count"]
        for item in categories
    )

    assert math.isclose(
        category_total,
        spending["total_spending"],
        abs_tol=0.02
    ), "Category totals do not reconcile with overall spending."

    assert category_count == spending["transaction_count"]

    print("Category reconciliation test passed.")

    # Verify monthly totals reconcile with overall spending.
    monthly = get_monthly_spending(ACCOUNT_REF)

    monthly_total = sum(
        item["total_spending"]
        for item in monthly
    )

    monthly_count = sum(
        item["transaction_count"]
        for item in monthly
    )

    assert math.isclose(
        monthly_total,
        spending["total_spending"],
        abs_tol=0.02
    ), "Monthly totals do not reconcile with overall spending."

    assert monthly_count == spending["transaction_count"]

    print("Monthly reconciliation test passed.")


def test_nonexistent_account():
    print("\n--- Nonexistent Account Verification ---")

    transactions = get_transactions(
        "RB-INVALID-9999",
        limit=100
    )

    spending = get_total_spending("RB-INVALID-9999")

    assert transactions == [], (
        "Nonexistent account should return an empty transaction list."
    )

    assert spending["total_spending"] == 0
    assert spending["transaction_count"] == 0

    print("Nonexistent account test passed.")


if __name__ == "__main__":

    test_customer_and_account_retrieval()
    test_transaction_retrieval()
    test_date_range_filter()
    test_spending_calculations()
    test_nonexistent_account()

    print("\nAll transaction repository tests passed.")
