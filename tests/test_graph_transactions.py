
from langchain_core.messages import HumanMessage

from agents.graph import agent


config = {
    "configurable": {
        "thread_id": "transaction-analysis-test"
    }
}


questions = [
    "Show me the spending summary for account RB-ACC-1002.",
    "Break down the spending by category for account RB-ACC-1002.",
    "Show me the monthly spending for account RB-ACC-1002.",
    "Show me the transactions for account RB-ACC-1002."
]


for question in questions:

    print("\n" + "=" * 60)
    print("USER:", question)

    result = agent.invoke(
        {
            "messages": [
                HumanMessage(content=question)
            ]
        },
        config=config
    )

    print("\nASSISTANT:")
    print(result["messages"][-1].content)
