
from tools.transaction_tools import (
    get_spending_summary,
    get_account_transactions
)


def run_test(name, result):

    print("\n" + "=" * 65)
    print(name)
    print("=" * 65)
    print(result)


# Test 1: Invalid calendar date
run_test(
    "Invalid date format",
    get_spending_summary.invoke({
        "account_ref": "RB-ACC-1002",
        "start_date": "2026-15-40",
        "end_date": "2026-11-30"
    })
)


# Test 2: Start date later than end date
run_test(
    "Reversed date range",
    get_spending_summary.invoke({
        "account_ref": "RB-ACC-1002",
        "start_date": "2026-11-30",
        "end_date": "2026-09-01"
    })
)


# Test 3: Invalid date in transaction retrieval
run_test(
    "Invalid date in transaction retrieval",
    get_account_transactions.invoke({
        "account_ref": "RB-ACC-1002",
        "start_date": "2026-09-40",
        "end_date": "2026-11-30"
    })
)


# Test 4: Reversed date range in transaction retrieval
run_test(
    "Reversed transaction date range",
    get_account_transactions.invoke({
        "account_ref": "RB-ACC-1002",
        "start_date": "2026-11-30",
        "end_date": "2026-09-01"
    })
)


print("\nAll direct validation tests executed.")
