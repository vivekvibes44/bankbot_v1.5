
from tools.transaction_tools import (
    get_account_transactions,
    get_spending_summary,
    get_category_spending,
    get_monthly_spending
)


account_ref = "RB-ACC-1002"

print("\n--- Transaction Retrieval Tool ---")
print(
    get_account_transactions.invoke({
        "account_ref": account_ref
    })
)

print("\n--- Spending Summary Tool ---")
print(
    get_spending_summary.invoke({
        "account_ref": account_ref
    })
)

print("\n--- Category Spending Tool ---")
print(
    get_category_spending.invoke({
        "account_ref": account_ref
    })
)

print("\n--- Monthly Spending Tool ---")
print(
    get_monthly_spending.invoke({
        "account_ref": account_ref
    })
)

print("\n--- Invalid Account Test ---")
print(
    get_spending_summary.invoke({
        "account_ref": "INVALID_ACCOUNT"
    })
)

print("\n--- Invalid Date Test ---")
print(
    get_spending_summary.invoke({
        "account_ref": account_ref,
        "start_date": "2026-15-40"
    })
)

print("\nTransaction tool testing completed.")
