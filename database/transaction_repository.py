from datetime import datetime
from database.db import get_connection


def _validate_date(date_value):
    """Validate a date in YYYY-MM-DD format."""
    if date_value is None:
        return

    try:
        datetime.strptime(date_value, "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            f"Invalid date: {date_value}. Expected format: YYYY-MM-DD."
        )


def _validate_date_range(start_date=None, end_date=None):
    """Validate optional start and end dates."""
    _validate_date(start_date)
    _validate_date(end_date)

    if start_date and end_date and start_date > end_date:
        raise ValueError("Start date cannot be later than end date.")


def get_customers():
    """Retrieve all simulated customers."""
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT customer_id, customer_name, created_at
            FROM customers
            ORDER BY customer_name
        """)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


def get_customer_accounts(customer_id):
    """Retrieve all accounts belonging to a specific customer."""

    if not customer_id or not customer_id.strip():
        raise ValueError("Customer ID is required.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                account_ref,
                customer_id,
                account_type,
                status,
                created_at
            FROM accounts
            WHERE customer_id = ?
            ORDER BY account_ref
        """, (customer_id.strip(),))

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


def get_transactions(
    account_ref,
    start_date=None,
    end_date=None,
    category=None,
    limit=100
):
    """
    Retrieve transactions for an account.

    Optional filters:
    - start_date: YYYY-MM-DD
    - end_date: YYYY-MM-DD
    - category: Transaction category
    - limit: Maximum number of records
    """

    if not account_ref or not account_ref.strip():
        raise ValueError("Account reference is required.")

    _validate_date_range(start_date, end_date)

    if not isinstance(limit, int) or isinstance(limit, bool) or limit <= 0:
        raise ValueError("Limit must be a positive integer.")

    query = """
        SELECT
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
        FROM transactions
        WHERE account_ref = ?
    """

    parameters = [account_ref.strip()]

    if start_date:
        query += " AND date(transaction_date) >= date(?)"
        parameters.append(start_date)

    if end_date:
        query += " AND date(transaction_date) <= date(?)"
        parameters.append(end_date)

    if category:
        query += " AND category = ?"
        parameters.append(category.strip())

    query += " ORDER BY transaction_date DESC LIMIT ?"
    parameters.append(limit)

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query, parameters)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


def get_total_spending(account_ref, start_date=None, end_date=None):
    """
    Calculate total successful debit spending
    for an account within an optional date range.
    """

    if not account_ref or not account_ref.strip():
        raise ValueError("Account reference is required.")

    _validate_date_range(start_date, end_date)

    query = """
        SELECT
            COALESCE(SUM(amount), 0) AS total_spending,
            COUNT(*) AS transaction_count
        FROM transactions
        WHERE account_ref = ?
          AND transaction_type = 'Debit'
          AND status = 'Success'
    """

    parameters = [account_ref.strip()]

    if start_date:
        query += " AND date(transaction_date) >= date(?)"
        parameters.append(start_date)

    if end_date:
        query += " AND date(transaction_date) <= date(?)"
        parameters.append(end_date)

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query, parameters)

        result = dict(cursor.fetchone())

        return {
            "account_ref": account_ref.strip(),
            "total_spending": round(result["total_spending"], 2),
            "transaction_count": result["transaction_count"],
            "currency": "INR"
        }

    finally:
        connection.close()


def get_category_spending(account_ref, start_date=None, end_date=None):
    """Calculate successful debit spending grouped by category."""

    if not account_ref or not account_ref.strip():
        raise ValueError("Account reference is required.")

    _validate_date_range(start_date, end_date)

    query = """
        SELECT
            category,
            ROUND(SUM(amount), 2) AS total_spending,
            COUNT(*) AS transaction_count
        FROM transactions
        WHERE account_ref = ?
          AND transaction_type = 'Debit'
          AND status = 'Success'
    """

    parameters = [account_ref.strip()]

    if start_date:
        query += " AND date(transaction_date) >= date(?)"
        parameters.append(start_date)

    if end_date:
        query += " AND date(transaction_date) <= date(?)"
        parameters.append(end_date)

    query += """
        GROUP BY category
        ORDER BY total_spending DESC
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query, parameters)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


def get_monthly_spending(account_ref, start_date=None, end_date=None):
    """Calculate successful debit spending grouped by month."""

    if not account_ref or not account_ref.strip():
        raise ValueError("Account reference is required.")

    _validate_date_range(start_date, end_date)

    query = """
        SELECT
            strftime('%Y-%m', transaction_date) AS month,
            ROUND(SUM(amount), 2) AS total_spending,
            COUNT(*) AS transaction_count
        FROM transactions
        WHERE account_ref = ?
          AND transaction_type = 'Debit'
          AND status = 'Success'
    """

    parameters = [account_ref.strip()]

    if start_date:
        query += " AND date(transaction_date) >= date(?)"
        parameters.append(start_date)

    if end_date:
        query += " AND date(transaction_date) <= date(?)"
        parameters.append(end_date)

    query += """
        GROUP BY strftime('%Y-%m', transaction_date)
        ORDER BY month
    """

    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(query, parameters)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


def get_account(account_ref):
    """Retrieve an account by its reference."""

    if not account_ref or not account_ref.strip():
        raise ValueError("Account reference is required.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                account_ref,
                customer_id,
                account_type,
                status
            FROM accounts
            WHERE account_ref = ?
        """, (account_ref.strip(),))

        result = cursor.fetchone()

        return dict(result) if result else None

    finally:
        connection.close()
