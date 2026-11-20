
from agents.tool_agent import run_tool_agent


response = run_tool_agent(
    "Calculate the EMI for a loan of 500000 rupees "
    "at an annual interest rate of 10% for 5 years."
)

print("\nReady Bank Agent Response:\n")
print(response)
