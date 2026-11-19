
from tools.loan_tools import compare_loans

result = compare_loans.invoke({})

print("\nReady Bank Loan Comparison:\n")

for loan in result["available_loans"]:
    print(f"\nLoan Type: {loan['loan_type']}")
    print(f"Interest Rate: {loan['annual_interest_rate']}%")
    print(
        f"Age Range: {loan['minimum_age']} - "
        f"{loan['maximum_age']} years"
    )
    print(
        f"Minimum Monthly Income: "
        f"₹{loan['minimum_monthly_income']}"
    )
    print(
        f"Maximum Tenure: "
        f"{loan['maximum_tenure_years']} years"
    )

print("\nDisclaimer:")
print(result["disclaimer"])
