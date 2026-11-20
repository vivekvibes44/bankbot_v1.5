
from langchain_core.messages import HumanMessage
from agents.graph import agent
from database.db import get_connection, initialize_database


def create_empty_test_account():

    initialize_database()
    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT OR IGNORE INTO customers
            (customer_id, customer_name)
            VALUES (?, ?)
            """,
            ("RB-CUST-TEST-EMPTY", "Synthetic Test Customer")
        )

        connection.execute(
            """
            INSERT OR IGNORE INTO accounts
            (account_ref, customer_id, account_type, status)
            VALUES (?, ?, ?, ?)
            """,
            (
                "RB-ACC-EMPTY-001",
                "RB-CUST-TEST-EMPTY",
                "Savings",
                "Active"
            )
        )

        connection.commit()

    finally:
        connection.close()


def run_test(test_name, question, thread_id):

    print("\n" + "=" * 70)
    print(f"TEST: {test_name}")
    print("=" * 70)
    print(f"\nUSER: {question}")
    print("\nASSISTANT:")

    response = agent.invoke(
        {
            "messages": [
                HumanMessage(content=question)
            ]
        },
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    print(response["messages"][-1].content)


if __name__ == "__main__":

    create_empty_test_account()

    test_cases = [

        # Existing five tests

        (
            "1. Missing account reference",
            "Show me my spending summary.",
            "edge-test-1"
        ),

        (
            "2. Invalid account reference",
            "Show me the spending summary for account RB-ACC-9999.",
            "edge-test-2"
        ),

        (
            "3. Date-range spending",
            (
                "Show me the spending summary for account RB-ACC-1002 "
                "between 2026-09-01 and 2026-09-30."
            ),
            "edge-test-3"
        ),

        (
            "4. Category-filtered transactions",
            "Show me all Shopping transactions for account RB-ACC-1002.",
            "edge-test-4"
        ),

        (
            "5. Account with no transactions",
            "Show me all transactions for account RB-ACC-EMPTY-001.",
            "edge-test-5"
        ),

        # New additional tests

        (
            "6. Pending and failed transaction retrieval",
            (
                "Show me all transactions for account RB-ACC-1002 "
                "including pending and failed transactions."
            ),
            "edge-test-6"
        ),

        (
            "7. Category with no matching transactions",
            (
                "Show me all Insurance transactions for account "
                "RB-ACC-1002."
            ),
            "edge-test-7"
        ),

        (
            "8. Invalid date format",
            (
                "Show me the spending summary for account RB-ACC-1002 "
                "from 2026-15-40 to 2026-11-30."
            ),
            "edge-test-8"
        ),

        (
            "9. Start date after end date",
            (
                "Show me the spending summary for account RB-ACC-1002 "
                "from 2026-11-30 to 2026-09-01."
            ),
            "edge-test-9"
        ),

        (
            "10. Date-filtered transaction retrieval",
            (
                "Show me all transactions for account RB-ACC-1002 "
                "between 2026-09-01 and 2026-09-30."
            ),
            "edge-test-10"
        ),

        (
            "11. Category spending within a date range",
            (
                "Show me the category-wise spending for account "
                "RB-ACC-1002 between 2026-09-01 and 2026-11-30."
            ),
            "edge-test-11"
        ),

        (
            "12. Monthly spending within a date range",
            (
                "Show me the monthly spending for account RB-ACC-1002 "
                "between 2026-09-01 and 2026-11-30."
            ),
            "edge-test-12"
        )
    ]

    for test_name, question, thread_id in test_cases:

        run_test(
            test_name=test_name,
            question=question,
            thread_id=thread_id
        )

    print("\n\n" + "=" * 70)
    print("ALL EDGE-CASE TESTS EXECUTED")
    print("=" * 70)
