
import streamlit as st
import pandas as pd

from datetime import date

from database.transaction_repository import (
    get_customers,
    get_customer_accounts,
)

from tools.transaction_tools import (
    get_account_transactions,
    get_spending_summary,
    get_category_spending,
    get_monthly_spending,
)


def get_selected_account():

    customers = get_customers()

    if not customers:
        st.warning("No customers are currently available.")
        return None

    customer_options = {
        f"{customer['customer_name']} ({customer['customer_id']})":
            customer["customer_id"]
        for customer in customers
    }

    selected_customer = st.selectbox(
        "Select Customer",
        list(customer_options.keys()),
    )

    customer_id = customer_options[selected_customer]

    accounts = get_customer_accounts(customer_id)

    active_accounts = [
        account
        for account in accounts
        if account["status"].lower() == "active"
    ]

    if not active_accounts:
        st.warning("This customer has no active accounts.")
        return None

    account_options = {
        (
            f"{account['account_ref']} — "
            f"{account['account_type']}"
        ): account["account_ref"]
        for account in active_accounts
    }

    selected_account = st.selectbox(
        "Select Account",
        list(account_options.keys()),
    )

    return account_options[selected_account]


def get_date_filters():

    apply_date_filter = st.checkbox(
        "Filter by date range",
        value=False,
    )

    if not apply_date_filter:
        return {}

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Start Date",
            value=date.today().replace(day=1),
        )

    with col2:
        end_date = st.date_input(
            "End Date",
            value=date.today(),
        )

    if start_date > end_date:
        st.error("Start date cannot be later than end date.")
        return None

    return {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
    }


def show_transaction_history(account_ref, date_filters):

    result = get_account_transactions.invoke({
        "account_ref": account_ref,
        **date_filters,
    })

    if result.get("status") != "success":
        st.error(result.get("message", "Unable to retrieve transactions."))
        return

    transactions = result.get("transactions", [])

    st.subheader("Transaction History")

    st.metric(
        "Total Transactions",
        result.get("transaction_count", len(transactions)),
    )

    if not transactions:
        st.info("No transactions found for the selected account and date range.")
        return

    transaction_df = pd.DataFrame(transactions)

    display_columns = [
        "transaction_id",
        "transaction_date",
        "description",
        "merchant",
        "category",
        "transaction_type",
        "amount",
        "payment_method",
        "status",
    ]

    transaction_df = transaction_df[
        [
            column
            for column in display_columns
            if column in transaction_df.columns
        ]
    ]

    st.dataframe(
        transaction_df,
        use_container_width=True,
        hide_index=True,
    )


def show_spending_summary(account_ref, date_filters):

    result = get_spending_summary.invoke({
        "account_ref": account_ref,
        **date_filters,
    })

    if result.get("status") != "success":
        st.error(result.get("message", "Unable to retrieve spending summary."))
        return

    st.subheader("Spending Summary")

    col1, col2 = st.columns(2)

    currency = result.get("currency", "INR")
    total_spending = result.get("total_spending", 0)

    currency_symbol = "₹" if currency == "INR" else f"{currency} "

    col1.metric(
        "Total Spending",
        f"{currency_symbol}{total_spending:,.2f}",
    )

    col2.metric(
        "Successful Debit Transactions",
        result.get("transaction_count", 0),
    )

    st.caption(
        "Spending includes successful debit transactions only."
    )


def show_category_analysis(account_ref, date_filters):

    result = get_category_spending.invoke({
        "account_ref": account_ref,
        **date_filters,
    })

    if result.get("status") != "success":
        st.error(result.get("message", "Unable to retrieve category spending."))
        return

    categories = result.get("categories", [])

    st.subheader("Category-wise Spending")

    if not categories:
        st.info("No category spending data is available.")
        return

    category_df = pd.DataFrame(categories)

    st.dataframe(
        category_df,
        use_container_width=True,
        hide_index=True,
    )

    if "category" in category_df.columns and "total_spending" in category_df.columns:
        chart_df = category_df.set_index("category")[
            "total_spending"
        ]

        st.subheader("Spending by Category")
        st.bar_chart(chart_df)


def show_monthly_analysis(account_ref, date_filters):

    result = get_monthly_spending.invoke({
        "account_ref": account_ref,
        **date_filters,
    })

    if result.get("status") != "success":
        st.error(result.get("message", "Unable to retrieve monthly spending."))
        return

    monthly_data = result.get("monthly_spending", [])

    st.subheader("Monthly Spending")

    if not monthly_data:
        st.info("No monthly spending data is available.")
        return

    monthly_df = pd.DataFrame(monthly_data)

    st.dataframe(
        monthly_df,
        use_container_width=True,
        hide_index=True,
    )

    if "month" in monthly_df.columns and "total_spending" in monthly_df.columns:
        chart_df = monthly_df.set_index("month")[
            "total_spending"
        ]

        st.subheader("Monthly Spending Trend")
        st.line_chart(chart_df)


def show_transactions():

    st.title("Transactions & Spending")

    st.write(
        "Review account transactions and understand spending "
        "patterns using transaction data."
    )

    st.divider()

    account_ref = get_selected_account()

    if not account_ref:
        return

    st.caption(f"Selected Account: **{account_ref}**")

    st.divider()

    date_filters = get_date_filters()

    if date_filters is None:
        return

    st.divider()

    history_tab, summary_tab, category_tab, monthly_tab = st.tabs(
        [
            "Transaction History",
            "Spending Summary",
            "Category Analysis",
            "Monthly Analysis",
        ]
    )

    with history_tab:

        if st.button(
            "Load Transactions",
            key="load_transactions",
            use_container_width=True,
        ):
            try:
                show_transaction_history(account_ref, date_filters)
            except Exception as error:
                st.error(f"Unable to load transactions: {error}")

    with summary_tab:

        if st.button(
            "View Spending Summary",
            key="view_spending_summary",
            use_container_width=True,
        ):
            try:
                show_spending_summary(account_ref, date_filters)
            except Exception as error:
                st.error(f"Unable to load spending summary: {error}")

    with category_tab:

        if st.button(
            "Analyze Categories",
            key="analyze_categories",
            use_container_width=True,
        ):
            try:
                show_category_analysis(account_ref, date_filters)
            except Exception as error:
                st.error(f"Unable to load category analysis: {error}")

    with monthly_tab:

        if st.button(
            "View Monthly Trends",
            key="view_monthly_trends",
            use_container_width=True,
        ):
            try:
                show_monthly_analysis(account_ref, date_filters)
            except Exception as error:
                st.error(f"Unable to load monthly spending: {error}")
