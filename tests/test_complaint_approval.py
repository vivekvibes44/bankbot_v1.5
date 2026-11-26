
import tempfile
from pathlib import Path
from unittest.mock import patch

from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.types import Command

import database.db as database_db
from tools.complaint_tools import register_complaint


def build_test_graph():

    graph = StateGraph(MessagesState)

    graph.add_node(
        "tools",
        ToolNode([register_complaint])
    )

    graph.add_edge(START, "tools")
    graph.add_edge("tools", END)

    checkpointer = InMemorySaver()

    return graph.compile(checkpointer=checkpointer)


def create_complaint_tool_call():

    return AIMessage(
        content="",
        tool_calls=[
            {
                "name": "register_complaint",
                "args": {
                    "category": "Digital Banking",
                    "description": "Unable to access mobile banking."
                },
                "id": "test_complaint_call",
                "type": "tool_call"
            }
        ]
    )


def get_complaint_records():

    connection = database_db.get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT *
            FROM complaints
        """)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


def test_complaint_approval():

    print("\n--- Complaint Approval Test ---")

    with tempfile.TemporaryDirectory() as temp_dir:

        test_db = Path(temp_dir) / "test_ready_bank.db"

        with patch.object(database_db, "DB_PATH", test_db):

            database_db.initialize_database()

            agent = build_test_graph()

            config = {
                "configurable": {
                    "thread_id": "approval_test"
                }
            }

            # Start graph execution.
            result = agent.invoke(
                {
                    "messages": [
                        create_complaint_tool_call()
                    ]
                },
                config=config
            )

            # Verify graph paused for approval.
            interrupts = result.get("__interrupt__", [])

            assert len(interrupts) == 1

            approval_data = interrupts[0].value

            assert approval_data["type"] == "complaint_registration"
            assert approval_data["category"] == "Digital Banking"

            # Complaint must not exist before approval.
            assert len(get_complaint_records()) == 0

            # Resume graph with explicit approval.
            result = agent.invoke(
                Command(
                    resume={"approved": True}
                ),
                config=config
            )

            assert not result.get("__interrupt__")

            records = get_complaint_records()

            assert len(records) == 1

            complaint = records[0]

            assert complaint["category"] == "Digital Banking"
            assert complaint["description"] == (
                "Unable to access mobile banking."
            )
            assert complaint["status"] == "Open"
            assert complaint["complaint_id"].startswith("RB-")

            print("PASS: Graph paused for approval")
            print("PASS: No insertion before approval")
            print("PASS: Complaint inserted after approval")
            print("PASS: Complaint ID and status verified")


def test_complaint_rejection():

    print("\n--- Complaint Rejection Test ---")

    with tempfile.TemporaryDirectory() as temp_dir:

        test_db = Path(temp_dir) / "test_ready_bank.db"

        with patch.object(database_db, "DB_PATH", test_db):

            database_db.initialize_database()

            agent = build_test_graph()

            config = {
                "configurable": {
                    "thread_id": "rejection_test"
                }
            }

            result = agent.invoke(
                {
                    "messages": [
                        create_complaint_tool_call()
                    ]
                },
                config=config
            )

            assert len(result.get("__interrupt__", [])) == 1

            # Resume graph with rejection.
            result = agent.invoke(
                Command(
                    resume={"approved": False}
                ),
                config=config
            )

            assert not result.get("__interrupt__")

            records = get_complaint_records()

            assert len(records) == 0

            tool_result = result["messages"][-1].content

            assert "cancelled" in str(tool_result)

            print("PASS: Complaint approval was rejected")
            print("PASS: No complaint inserted into database")


def test_unexpected_approval_response():

    print("\n--- Unexpected Approval Response Test ---")

    with tempfile.TemporaryDirectory() as temp_dir:

        test_db = Path(temp_dir) / "test_ready_bank.db"

        with patch.object(database_db, "DB_PATH", test_db):

            database_db.initialize_database()

            agent = build_test_graph()

            config = {
                "configurable": {
                    "thread_id": "unexpected_response_test"
                }
            }

            result = agent.invoke(
                {
                    "messages": [
                        create_complaint_tool_call()
                    ]
                },
                config=config
            )

            assert len(result.get("__interrupt__", [])) == 1

            # A non-boolean approval must not register a complaint.
            result = agent.invoke(
                Command(
                    resume={"approved": "yes"}
                ),
                config=config
            )

            assert not result.get("__interrupt__")

            records = get_complaint_records()

            assert len(records) == 0

            tool_result = result["messages"][-1].content

            assert "cancelled" in str(tool_result)

            print("PASS: Unexpected approval response rejected")
            print("PASS: No complaint inserted into database")


if __name__ == "__main__":

    print("\n========== COMPLAINT APPROVAL WORKFLOW TESTS ==========")

    test_complaint_approval()
    test_complaint_rejection()
    test_unexpected_approval_response()

    print("\n========== ALL TESTS PASSED ==========\n")
