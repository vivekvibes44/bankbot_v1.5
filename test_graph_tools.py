
from langchain_core.messages import HumanMessage
from agents.graph import agent


# Test 1: EMI calculation
emi_result = agent.invoke({
    "messages": [
        HumanMessage(
            content=(
                "Calculate the EMI for a loan of 500000 rupees "
                "at an annual interest rate of 10% for 5 years."
            )
        )
    ]
})

print("\n--- EMI Calculation ---\n")
print(emi_result["messages"][-1].content)


# Test 2: Loan eligibility
eligibility_result = agent.invoke({
    "messages": [
        HumanMessage(
            content=(
                "Check whether I qualify for a personal loan. "
                "I am 25 years old and earn 35000 rupees per month."
            )
        )
    ]
})

print("\n--- Loan Eligibility ---\n")
print(eligibility_result["messages"][-1].content)

# Test 3: Missing EMI information
missing_emi_result = agent.invoke({
    "messages": [
        HumanMessage(
            content="Calculate the EMI for a loan of 500000 rupees."
        )
    ]
})

print("\n--- Missing EMI Information ---\n")
print(missing_emi_result["messages"][-1].content)


# Test 4: Missing eligibility information
missing_eligibility_result = agent.invoke({
    "messages": [
        HumanMessage(
            content="Check my personal loan eligibility."
        )
    ]
})

print("\n--- Missing Eligibility Information ---\n")
print(missing_eligibility_result["messages"][-1].content)