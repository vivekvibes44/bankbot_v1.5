from agents.graph import agent

def test_agent_rag():

    config = {
        "configurable": {
            "thread_id": "rag-test-001"
        }
    }

    question = "Show me my spending summary."

    print("\nUser:", question)

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        },
        config=config
    )

    print("\nAssistant:")

    print(result["messages"][-1].content)


if __name__ == "__main__":
    test_agent_rag()
