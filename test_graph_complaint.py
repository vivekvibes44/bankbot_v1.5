
from langchain_core.messages import HumanMessage
from agents.graph import agent

# Test 1: Track an existing complaint
print("\n--- Test 1: Existing complaint ---")

response = agent.invoke({
    "messages": [
        HumanMessage(
            content="Track complaint RB-063ED641 and tell me its current status."
        )
    ]
})

print(response["messages"][-1].content)


# Test 2: Missing complaint ID
print("\n--- Test 2: Missing complaint ID ---")

response = agent.invoke({
    "messages": [
        HumanMessage(content="Track my complaint.")
    ]
})

print(response["messages"][-1].content)
