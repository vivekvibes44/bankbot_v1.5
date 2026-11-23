
import uuid

from langchain_core.messages import HumanMessage
from agents.graph import agent


def test_emi_tool_routing():

    user_question = (
        "Calculate the EMI for a loan of ₹5,00,000 "
        "at an annual interest rate of 12.5% "
        "for a tenure of 5 years."
    )

    config = {
        "configurable": {
            "thread_id": str(uuid.uuid4())
        }
    }

    print("\nSending request to LangGraph...\n")

    result = agent.invoke(
        {
            "messages": [
                HumanMessage(content=user_question)
            ]
        },
        config=config
    )

    print("\n--- GRAPH EXECUTION TRACE ---\n")

    for message in result["messages"]:

        print(f"\nMessage type: {type(message).__name__}")

        # Check whether the LLM requested a tool.
        if hasattr(message, "tool_calls"):

            for tool_call in message.tool_calls:
                print("Tool requested:", tool_call["name"])
                print("Arguments:", tool_call["args"])

        # Check whether a tool actually executed.
        if hasattr(message, "tool_call_id"):

            print("Tool call ID:", message.tool_call_id)
            print("Tool result:", message.content)

    print("\n--- FINAL RESPONSE ---\n")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    test_emi_tool_routing()
