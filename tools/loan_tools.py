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


# Fictional Ready Bank loan eligibility criteria

LOAN_CRITERIA = {
    "personal loan": {
        "minimum_age": 21,
        "maximum_age": 60,
        "minimum_income": 25000
    },
    "home loan": {
        "minimum_age": 21,
        "maximum_age": 65,
        "minimum_income": 40000
    },
    "education loan": {
        "minimum_age": 18,
        "maximum_age": 35,
        "minimum_income": 15000
    }
}


from langchain_core.tools import tool


@tool
def check_loan_eligibility(
    loan_type: str,
    age: int,
    monthly_income: float
):
    """
    Check preliminary eligibility for a Ready Bank loan.

    Args:
        loan_type: Type of loan (personal loan, home loan,
                   or education loan).
        age: Applicant's age in years.
        monthly_income: Applicant's monthly income in INR.

    Returns:
        Eligibility result with reasons and loan requirements.
    """

    loan_type = loan_type.strip().lower()

    if loan_type not in LOAN_CRITERIA:
        return {
            "status": "invalid_loan_type",
            "message": (
                "Unsupported loan type. Available options: "
                "Personal Loan, Home Loan, Education Loan."
            )
        }

    if age <= 0:
        return {"status": "invalid_input", "message": "Age must be greater than zero."}

    if monthly_income < 0:
        return {"status": "invalid_input", "message": "Income cannot be negative."}

    criteria = LOAN_CRITERIA[loan_type]

    reasons = []

    if age < criteria["minimum_age"]:
        reasons.append("Applicant does not meet the minimum age requirement.")

    if age > criteria["maximum_age"]:
        reasons.append("Applicant exceeds the maximum age requirement.")

    if monthly_income < criteria["minimum_income"]:
        reasons.append("Monthly income is below the required minimum.")

    eligible = len(reasons) == 0

    return {
        "loan_type": loan_type.title(),
        "status": "eligible" if eligible else "not_eligible",
        "preliminary_eligibility": eligible,
        "applicant_age": age,
        "monthly_income": monthly_income,
        "minimum_age": criteria["minimum_age"],
        "maximum_age": criteria["maximum_age"],
        "minimum_income": criteria["minimum_income"],
        "reasons": reasons if reasons else ["All preliminary criteria are satisfied."],
        "disclaimer": (
            "This is a simulated preliminary eligibility check, "
            "not a loan approval or financial decision."
        )
    }

