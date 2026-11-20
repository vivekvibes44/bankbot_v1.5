
import random
from datetime import date, timedelta

from database.db import get_connection


def generate_synthetic_data():

    rng = random.Random(42)
    today = date.today()
    start_date = today - timedelta(days=180)

    customers = [
        ("RB-CUST-001", "Ananya Sharma"),
        ("RB-CUST-002", "Rohan Mehta"),
        ("RB-CUST-003", "Priya Nair"),
        ("RB-CUST-004", "Arjun Rao"),
        ("RB-CUST-005", "Neha Kapoor"),
    ]

    accounts = [
        ("RB-ACC-1001", "RB-CUST-001", "Savings"),
        ("RB-ACC-1002", "RB-CUST-001", "Salary"),
        ("RB-ACC-2001", "RB-CUST-002", "Savings"),
        ("RB-ACC-3001", "RB-CUST-003", "Savings"),
        ("RB-ACC-3002", "RB-CUST-003", "Salary"),
        ("RB-ACC-4001", "RB-CUST-004", "Savings"),
        ("RB-ACC-5001", "RB-CUST-005", "Savings"),
    ]

    # Category: (merchant names, minimum amount, maximum amount)
    spending_categories = {
        "Groceries": (
            ["Reliance Fresh", "DMart", "BigBasket"],
            200, 3000
        ),
        "Dining": (
            ["Swiggy", "Zomato", "Local Restaurant"],
            150, 1500
        ),
        "Transport": (
            ["Uber", "Ola", "Indian Oil"],
            50, 1200
        ),
        "Shopping": (
            ["Amazon", "Flipkart", "Myntra"],
            300, 8000
        ),
        "Utilities": (
            ["Electricity Board", "Airtel", "Water Services"],
            300, 3000
        ),
        "Entertainment": (
            ["BookMyShow", "Netflix", "PVR Cinemas"],
            150, 2500
        ),
        "Healthcare": (
            ["Apollo Pharmacy", "MedPlus", "Local Clinic"],
            100, 5000
        ),
        "Travel": (
            ["IRCTC", "MakeMyTrip", "RedBus"],
            500, 12000
        ),
    }

    payment_methods = [
        "UPI",
        "Debit Card",
        "Net Banking",
        "ATM"
    ]

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # 1. Insert customers
        cursor.executemany("""
            INSERT OR IGNORE INTO customers
                (customer_id, customer_name)
            VALUES (?, ?)
        """, customers)

        # 2. Insert accounts
        cursor.executemany("""
            INSERT OR IGNORE INTO accounts
                (account_ref, customer_id, account_type)
            VALUES (?, ?, ?)
        """, accounts)

        transaction_records = []

        # 3. Generate debit transactions for each account
        for account_ref, customer_id, account_type in accounts:

            for number in range(1, 31):

                category = rng.choice(list(spending_categories.keys()))

                merchants, minimum_amount, maximum_amount = (
                    spending_categories[category]
                )

                merchant = rng.choice(merchants)
                amount = round(
                    rng.uniform(minimum_amount, maximum_amount), 2
                )

                transaction_date = start_date + timedelta(
                    days=rng.randint(0, (today - start_date).days)
                )

                status = rng.choices(
                    ["Success", "Pending", "Failed"],
                    weights=[85, 10, 5],
                    k=1
                )[0]

                transaction_records.append((
                    f"TXN-{account_ref}-{number:03d}",
                    account_ref,
                    transaction_date.strftime("%Y-%m-%d"),
                    f"Payment at {merchant}",
                    merchant,
                    category,
                    "Debit",
                    amount,
                    rng.choice(payment_methods),
                    status
                ))

        # 4. Generate monthly salary credits for salary accounts
        salary_amounts = {
            "RB-ACC-1002": 65000,
            "RB-ACC-3002": 58000
        }

        for account_ref, salary_amount in salary_amounts.items():

            month_cursor = date(today.year, today.month, 1)

            while month_cursor >= start_date:

                transaction_records.append((
                    f"TXN-{account_ref}-SAL-{month_cursor.strftime('%Y%m')}",
                    account_ref,
                    month_cursor.strftime("%Y-%m-%d"),
                    "Monthly salary credit",
                    "Ready Bank Payroll",
                    "Income",
                    "Credit",
                    salary_amount,
                    "Net Banking",
                    "Success"
                ))

                # Move to the first day of the previous month
                if month_cursor.month == 1:
                    month_cursor = date(month_cursor.year - 1, 12, 1)
                else:
                    month_cursor = date(
                        month_cursor.year,
                        month_cursor.month - 1,
                        1
                    )

        # 5. Insert transactions
        cursor.executemany("""
            INSERT OR IGNORE INTO transactions (
                transaction_id,
                account_ref,
                transaction_date,
                description,
                merchant,
                category,
                transaction_type,
                amount,
                payment_method,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, transaction_records)

        connection.commit()

        # 6. Display database record counts
        print("\n--- Synthetic Data Generation Complete ---")

        for table in ["customers", "accounts", "transactions"]:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"{table.capitalize()}: {count} records")

        print("\nSynthetic data inserted successfully.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    generate_synthetic_data()
