
from agents.graph import agent

result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "What services can Ready Bank help me with?"
        }
    ]
})

print("\nAgent Response:\n")
print(result["messages"][-1]["content"])
