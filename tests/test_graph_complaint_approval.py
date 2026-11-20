from langchain_core.messages import HumanMessage
from langgraph.types import Command

from agents.graph import agent


def test_complaint_approval():

    config = {
        "configurable": {
            "thread_id": "complaint-approval-test"
        }
    }

    print("\n--- Test 1: Complaint Registration Approval ---")

    # Step 1: Ask the agent to register a complaint.
    result = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content=(
                        "I want to register a complaint. "
                        "Category: Digital Banking. "
                        "Description: Unable to log in to the mobile application."
                    )
                )
            ]
        },
        config=config
    )

    # Step 2: Check whether LangGraph paused for approval.
    interrupts = result.get("__interrupt__", [])

    if not interrupts:
        print("ERROR: Graph did not pause for approval.")
        print(result)
        return

    print("\nApproval Required:")
    for interruption in interrupts:
        print(interruption.value)

    # Step 3: Simulate the user's approval.
    print("\nUser Decision: APPROVED")

    approved_result = agent.invoke(
        Command(resume={"approved": True}),
        config=config
    )

    print("\nFinal Agent Response:")
    print(approved_result["messages"][-1].content)


def test_complaint_rejection():

    config = {
        "configurable": {
            "thread_id": "complaint-rejection-test"
        }
    }

    print("\n--- Test 2: Complaint Registration Rejection ---")

    # Step 1: Ask the agent to register another complaint.
    result = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content=(
                        "Register a complaint under Debit Card. "
                        "Description: My debit card is not working."
                    )
                )
            ]
        },
        config=config
    )

    # Step 2: Check whether LangGraph paused for approval.
    interrupts = result.get("__interrupt__", [])

    if not interrupts:
        print("ERROR: Graph did not pause for approval.")
        print(result)
        return

    print("\nApproval Required:")
    for interruption in interrupts:
        print(interruption.value)

    # Step 3: Simulate the user's rejection.
    print("\nUser Decision: REJECTED")

    rejected_result = agent.invoke(
        Command(resume={"approved": False}),
        config=config
    )

    print("\nFinal Agent Response:")
    print(rejected_result["messages"][-1].content)


if __name__ == "__main__":
    test_complaint_approval()
    test_complaint_rejection()