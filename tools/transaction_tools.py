
from langchain_core.tools import tool

from database.transaction_repository import (
    get_account,
    get_transactions,
    get_total_spending,
    get_category_spending as fetch_category_spending,
    get_monthly_spending as fetch_monthly_spending
)


def validate_account(account_ref):
    """Check whether an account exists and is active."""

    account = get_account(account_ref)

    if account is None:
        return {
            "status": "account_not_found",
            "message": "The supplied account reference does not exist."
        }

    if account["status"] != "Active":
        return {
            "status": "account_inactive",
            "message": "This account is not currently active."
        }

    return None


@tool
def get_account_transactions(
    account_ref: str,
    start_date: str = None,
    end_date: str = None,
    category: str = None
):
    """
    Retrieve transactions for a specified Ready Bank account.

    Dates must use YYYY-MM-DD format.
    """

    try:
        validation = validate_account(account_ref)

        if validation:
            return validation

        transactions = get_transactions(
            account_ref=account_ref,
            start_date=start_date,
            end_date=end_date,
            category=category,
            limit=100
        )

        return {
            "status": "success",
            "account_ref": account_ref,
            "transaction_count": len(transactions),
            "transactions": transactions
        }

    except ValueError as error:
        return {"status": "invalid_input", "message": str(error)}


@tool
def get_spending_summary(
    account_ref: str,
    start_date: str = None,
    end_date: str = None
):
    """
    Calculate total successful debit spending for an account.
    """

    try:
        validation = validate_account(account_ref)

        if validation:
            return validation

        result = get_total_spending(
            account_ref=account_ref,
            start_date=start_date,
            end_date=end_date
        )

        return {"status": "success", **result}

    except ValueError as error:
        return {"status": "invalid_input", "message": str(error)}


@tool
def get_category_spending(
    account_ref: str,
    start_date: str = None,
    end_date: str = None
):
    """
    Calculate successful debit spending grouped by category.
    """

    try:
        validation = validate_account(account_ref)

        if validation:
            return validation

        result = fetch_category_spending(
            account_ref=account_ref,
            start_date=start_date,
            end_date=end_date
        )

        return {
            "status": "success",
            "account_ref": account_ref,
            "categories": result
        }

    except ValueError as error:
        return {"status": "invalid_input", "message": str(error)}


@tool
def get_monthly_spending(
    account_ref: str,
    start_date: str = None,
    end_date: str = None
):
    """
    Calculate successful debit spending grouped by month.
    """

    try:
        validation = validate_account(account_ref)

        if validation:
            return validation

        result = fetch_monthly_spending(
            account_ref=account_ref,
            start_date=start_date,
            end_date=end_date
        )

        return {
            "status": "success",
            "account_ref": account_ref,
            "monthly_spending": result
        }

    except ValueError as error:
        return {"status": "invalid_input", "message": str(error)}
