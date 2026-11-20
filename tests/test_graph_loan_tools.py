
from langchain_core.messages import HumanMessage
from agents.graph import agent


# Test 1: EMI calculation
emi_result = agent.invoke({
    "messages": [
        HumanMessage(
            content="Calculate EMI for 500000 rupees "
                    "at 10% annual interest for 5 years."
        )
    ]
})

print("\n--- EMI Calculation ---\n")
print(emi_result["messages"][-1].content)


# Test 2: Loan eligibility
eligibility_result = agent.invoke({
    "messages": [
        HumanMessage(
            content="Check my personal loan eligibility. "
                    "I am 25 years old and earn 35000 monthly."
        )
    ]
})

print("\n--- Loan Eligibility ---\n")
print(eligibility_result["messages"][-1].content)


# Test 3: Loan comparison
comparison_result = agent.invoke({
    "messages": [
        HumanMessage(
            content="Compare all available Ready Bank loans "
                    "and tell me which has the lowest interest rate."
        )
    ]
})

print("\n--- Loan Comparison ---\n")
print(comparison_result["messages"][-1].content)
