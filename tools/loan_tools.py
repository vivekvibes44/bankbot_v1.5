from langchain_core.tools import tool

@tool
def calculate_emi(
    principal: float,
    annual_interest_rate: float,
    tenure_months: int
):
    """
    Calculate the monthly EMI for a loan.

    Args:
        principal: Loan amount.
        annual_interest_rate: Annual interest rate in percentage.
        tenure_months: Loan tenure in months.

    Returns:
        Dictionary containing EMI and loan breakdown.
    """

    # Validate inputs
    if principal <= 0:
        raise ValueError("Loan amount must be greater than zero.")

    if annual_interest_rate < 0:
        raise ValueError("Interest rate cannot be negative.")

    if tenure_months <= 0:
        raise ValueError("Loan tenure must be greater than zero.")

    # Convert annual interest rate to monthly rate
    monthly_rate = annual_interest_rate / (12 * 100)

    # Calculate EMI
    if monthly_rate == 0:
        emi = principal / tenure_months
    else:
        emi = (
            principal
            * monthly_rate
            * (1 + monthly_rate) ** tenure_months
            / ((1 + monthly_rate) ** tenure_months - 1)
        )

    # Calculate loan breakdown
    total_payment = emi * tenure_months
    total_interest = total_payment - principal

    return {
        "loan_amount": round(principal, 2),
        "annual_interest_rate": annual_interest_rate,
        "tenure_months": tenure_months,
        "monthly_emi": round(emi, 2),
        "total_interest": round(total_interest, 2),
        "total_payment": round(total_payment, 2)
    }
