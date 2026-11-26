
import streamlit as st

from tools.loan_tools import (
    calculate_emi,
    compare_loans,
    check_loan_eligibility,
)


def show_emi_result(result):

    st.subheader("EMI Calculation")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Monthly EMI",
        f"₹{result['monthly_emi']:,.2f}",
    )

    col2.metric(
        "Total Interest",
        f"₹{result['total_interest']:,.2f}",
    )

    col3.metric(
        "Total Repayment",
        f"₹{result['total_payment']:,.2f}",
    )

    st.divider()

    st.write("**Loan Details**")

    col1, col2, col3 = st.columns(3)

    col1.write(f"Loan Amount: ₹{result['loan_amount']:,.2f}")
    col2.write(f"Interest Rate: {result['annual_interest_rate']}%")
    col3.write(f"Tenure: {result['tenure_months']} months")


def show_comparison_result(result):

    if result.get("status") != "success":
        st.error(result.get("message", "Unable to compare loans."))
        return

    st.subheader("Loan Comparison")

    st.caption(result.get("comparison_basis", ""))

    loans = result.get("available_loans", [])

    if not loans:
        st.info("No loan products are currently available.")
        return

    st.dataframe(
        [
            {
                "Loan Type": loan["loan_type"],
                "Interest Rate (%)": loan["annual_interest_rate"],
                "Minimum Age": loan["minimum_age"],
                "Maximum Age": loan["maximum_age"],
                "Minimum Monthly Income (₹)": loan["minimum_monthly_income"],
                "Maximum Tenure (Years)": loan["maximum_tenure_years"],
            }
            for loan in loans
        ],
        use_container_width=True,
        hide_index=True,
    )

    if result.get("disclaimer"):
        st.caption(result["disclaimer"])


def show_eligibility_result(result):

    status = result.get("status")

    if status == "invalid_input" or status == "invalid_loan_type":
        st.error(result.get("message", "Invalid eligibility request."))
        return

    if status == "eligible":
        st.success("You meet the preliminary eligibility criteria.")
    elif status == "not_eligible":
        st.warning("You do not currently meet the preliminary eligibility criteria.")
    else:
        st.error("Unable to determine eligibility.")
        return

    st.subheader("Applicant Details")

    col1, col2, col3 = st.columns(3)

    col1.metric("Loan Type", result["loan_type"])
    col2.metric("Applicant Age", result["applicant_age"])
    col3.metric(
        "Monthly Income",
        f"₹{result['monthly_income']:,.2f}",
    )

    st.divider()

    st.subheader("Eligibility Criteria")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Minimum Age",
        f"{result['minimum_age']} years",
    )

    col2.metric(
        "Maximum Age",
        f"{result['maximum_age']} years",
    )

    col3.metric(
        "Minimum Monthly Income",
        f"₹{result['minimum_income']:,.0f}",
    )

    reasons = result.get("reasons", [])

    if reasons:
        st.subheader("Eligibility Assessment")

        for reason in reasons:
            if status == "eligible":
                st.write(f"✓ {reason}")
            else:
                st.write(f"• {reason}")

    if result.get("disclaimer"):
        st.caption(result["disclaimer"])


def show_loans():

    st.title("Loan Services")

    st.write(
        "Calculate loan EMIs, compare available loan products, "
        "and check your loan eligibility."
    )

    st.divider()

    emi_tab, compare_tab, eligibility_tab = st.tabs(
        [
            "EMI Calculator",
            "Compare Loans",
            "Loan Eligibility",
        ]
    )

    # EMI CALCULATOR

    with emi_tab:

        st.subheader("Loan EMI Calculator")

        with st.form("emi_calculator_form"):

            principal = st.number_input(
                "Loan Amount (₹)",
                min_value=1000.0,
                value=500000.0,
                step=10000.0,
            )

            annual_interest_rate = st.number_input(
                "Annual Interest Rate (%)",
                min_value=0.1,
                value=10.0,
                step=0.1,
            )

            tenure_months = st.number_input(
                "Loan Tenure (Months)",
                min_value=1,
                value=60,
                step=1,
            )

            calculate_button = st.form_submit_button(
                "Calculate EMI",
                use_container_width=True,
            )

        if calculate_button:

            try:
                result = calculate_emi.invoke({
                    "principal": principal,
                    "annual_interest_rate": annual_interest_rate,
                    "tenure_months": tenure_months,
                })

                show_emi_result(result)

            except Exception as error:
                st.error(f"Unable to calculate EMI: {error}")

    # LOAN COMPARISON

    with compare_tab:

        st.subheader("Available Loan Products")

        st.write(
            "Compare the interest rates and eligibility criteria "
            "of Ready Bank loan products."
        )

        if st.button(
            "Compare Loans",
            use_container_width=True,
        ):

            try:
                result = compare_loans.invoke({})
                show_comparison_result(result)

            except Exception as error:
                st.error(f"Unable to compare loans: {error}")

    # LOAN ELIGIBILITY

    with eligibility_tab:

        st.subheader("Check Loan Eligibility")

        with st.form("loan_eligibility_form"):

            loan_type = st.selectbox(
                "Loan Type",
                [
                    "Personal Loan",
                    "Home Loan",
                    "Education Loan",
                ],
            )

            age = st.number_input(
                "Age",
                min_value=18,
                max_value=100,
                value=30,
                step=1,
            )

            monthly_income = st.number_input(
                "Monthly Income (₹)",
                min_value=0.0,
                value=50000.0,
                step=5000.0,
            )

            check_button = st.form_submit_button(
                "Check Eligibility",
                use_container_width=True,
            )

        if check_button:

            try:
                result = check_loan_eligibility.invoke({
                    "loan_type": loan_type,
                    "age": age,
                    "monthly_income": monthly_income,
                })

                show_eligibility_result(result)

            except Exception as error:
                st.error(f"Unable to check eligibility: {error}")
