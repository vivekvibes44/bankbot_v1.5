
from langchain_core.messages import HumanMessage
from agents.graph import agent


# First request
result = agent.invoke({
    "messages": [
        HumanMessage(
            content=(
                "Calculate the EMI for a loan of 500000 rupees "
                "at an annual interest rate of 10% for 5 years."
            )
        )
    ]
})


print("\nReady Bank Agent Response:\n")
print(result["messages"][-1].content)


# Second request using previous conversation messages
result = agent.invoke({
    "messages": result["messages"] + [
        HumanMessage(
            content="What is the total interest I will pay?"
        )
    ]
})


print("\nFollow-up Response:\n")
print(result["messages"][-1].content)
