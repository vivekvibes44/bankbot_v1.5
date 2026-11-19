
from tools.loan_tools import calculate_emi


result = calculate_emi(
    principal=500000,
    annual_interest_rate=10,
    tenure_months=60
)

print("\nEMI Calculation Result:\n")

for key, value in result.items():
    print(f"{key}: {value}")
