from tools.loan_tools import check_loan_eligibility


result = check_loan_eligibility.invoke({
    "loan_type": "personal loan",
    "age": 19,
    "monthly_income": 20000
})

print("\nLoan Eligibility Result:\n")

for key, value in result.items():
    print(f"{key}: {value}")
