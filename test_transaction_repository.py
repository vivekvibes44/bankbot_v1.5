
from database.transaction_repository import (
    get_customers,
    get_customer_accounts,
    get_transactions,
    get_total_spending,
    get_category_spending,
    get_monthly_spending
)


print("\n--- Transaction Repository Verification ---")

# 1. Retrieve customers
customers = get_customers()
print("\nCustomers:", customers)

# 2. Retrieve accounts
accounts = get_customer_accounts("INVALID_CUSTOMER")
print("\nAccounts:", accounts)

# 3. Retrieve transactions
transactions = get_transactions("INVALID_ACCOUNT")
print("\nTransactions:", transactions)

# 4. Total spending
spending = get_total_spending("INVALID_ACCOUNT")
print("\nTotal Spending:", spending)

# 5. Category spending
categories = get_category_spending("INVALID_ACCOUNT")
print("\nCategory Spending:", categories)

# 6. Monthly spending
monthly = get_monthly_spending("INVALID_ACCOUNT")
print("\nMonthly Spending:", monthly)


print("\n--- Input Validation Tests ---")

try:
    get_transactions("INVALID_ACCOUNT", start_date="2026-15-40")
except ValueError as error:
    print("SUCCESS:", error)

try:
    get_total_spending("INVALID_ACCOUNT", start_date="2026-12-01", end_date="2026-01-01")
except ValueError as error:
    print("SUCCESS:", error)

print("\nRepository tests completed.")
