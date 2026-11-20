
from database.transaction_repository import (
    get_customers,
    get_customer_accounts,
    get_transactions,
    get_total_spending,
    get_category_spending,
    get_monthly_spending
)


print("\n--- Customer Verification ---")

customers = get_customers()
print("Total customers:", len(customers))

for customer in customers:
    print(customer)


print("\n--- Account Verification ---")

accounts = get_customer_accounts("RB-CUST-001")

for account in accounts:
    print(account)


account_ref = "RB-ACC-1002"

print("\n--- Transaction Retrieval ---")

transactions = get_transactions(account_ref, limit=10)

for transaction in transactions:
    print(transaction)


print("\n--- Total Spending ---")

spending = get_total_spending(account_ref)
print(spending)


print("\n--- Category Spending ---")

categories = get_category_spending(account_ref)

for category in categories:
    print(category)


print("\n--- Monthly Spending ---")

monthly = get_monthly_spending(account_ref)

for month in monthly:
    print(month)


print("\n--- Date Range Filter Test ---")

filtered_transactions = get_transactions(
    account_ref,
    start_date="2026-09-01",
    end_date="2026-11-30"
)

print("Filtered transaction count:", len(filtered_transactions))

print("\nRepository testing completed.")
