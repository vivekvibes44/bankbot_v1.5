
from tools.transaction_tools import (
    get_spending_summary,
    get_account_transactions
)


ACCOUNT_REF = "RB-ACC-1002"


def run_test(name, result):

    print("\n" + "=" * 65)
    print(name)
    print("=" * 65)

    print(result)

    assert result["status"] == "invalid_input", (
        f"{name} failed: expected invalid_input, got {result}"
    )

    print("PASSED")


def test_invalid_calendar_date():

    result = get_spending_summary.invoke({
        "account_ref": ACCOUNT_REF,
        "start_date": "2026-15-40",
        "end_date": "2026-11-30"
    })

    run_test("Invalid calendar date", result)


def test_reversed_date_range():

    result = get_spending_summary.invoke({
        "account_ref": ACCOUNT_REF,
        "start_date": "2026-11-30",
        "end_date": "2026-09-01"
    })

    run_test("Reversed date range", result)


def test_invalid_transaction_date():

    result = get_account_transactions.invoke({
        "account_ref": ACCOUNT_REF,
        "start_date": "2026-09-40",
        "end_date": "2026-11-30"
    })

    run_test("Invalid date in transaction retrieval", result)


def test_reversed_transaction_date_range():

    result = get_account_transactions.invoke({
        "account_ref": ACCOUNT_REF,
        "start_date": "2026-11-30",
        "end_date": "2026-09-01"
    })

    run_test("Reversed transaction date range", result)


if __name__ == "__main__":

    test_invalid_calendar_date()
    test_reversed_date_range()
    test_invalid_transaction_date()
    test_reversed_transaction_date_range()

    print("\nAll transaction validation tests passed.")
