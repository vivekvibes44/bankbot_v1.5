import json
import streamlit as st


# 1. AGENT ACTIVITY TRACKING

def update_agent_activity(messages, pending_approval=False):
    """
    Capture actual LangGraph tool calls and tool results.

    Tool calls are identified using tool_call_id to prevent
    duplicate activity records when graph state is returned
    multiple times.
    """

    activity = st.session_state.agent_activity

    for message in messages or []:

        # Capture LLM tool requests
        for tool_call in getattr(message, "tool_calls", []) or []:

            tool_name = tool_call.get("name", "Unknown tool")
            tool_call_id = tool_call.get("id")

            if not tool_call_id:
                continue

            existing = next(
                (
                    item for item in activity
                    if item["tool_call_id"] == tool_call_id
                ),
                None
            )

            if existing is None:

                activity.append({
                    "tool_call_id": tool_call_id,
                    "tool_name": tool_name,
                    "arguments": tool_call.get("args", {}),
                    "result": None,
                    "status": "Requested",
                })

        # Capture actual tool results
        tool_call_id = getattr(message, "tool_call_id", None)

        if tool_call_id:

            record = next(
                (
                    item for item in activity
                    if item["tool_call_id"] == tool_call_id
                ),
                None
            )

            if record is None:
                continue

            tool_result = getattr(message, "content", "")

            # Parse JSON-formatted results where possible.
            parsed_result = tool_result

            if isinstance(tool_result, str):

                try:
                    parsed_result = json.loads(tool_result)

                except (json.JSONDecodeError, TypeError):
                    pass

            record["result"] = parsed_result

            tool_status = getattr(message, "status", None)

            if tool_status == "error":

                record["status"] = "Failed"

            elif isinstance(parsed_result, dict):

                result_status = parsed_result.get("status")

                if result_status == "confirmation_required":

                    record["status"] = "Pending approval"

                elif result_status in ("rejected", "cancelled"):

                    record["status"] = "Cancelled"

                else:

                    record["status"] = "Completed"

            else:

                record["status"] = "Completed"

    # Mark tools awaiting human approval
    if pending_approval:

        for record in activity:

            if record["status"] == "Requested":
                record["status"] = "Pending approval"


# 2. STRUCTURED RESULT EXTRACTION

def extract_structured_results(messages):
    """
    Extract tool results generated during the latest user turn only.
    """

    structured_results = []

    messages = messages or []

    # Find the most recent user message.
    last_human_index = None

    for index, message in enumerate(messages):
        if getattr(message, "type", None) == "human":
            last_human_index = index

    # Ignore all messages from earlier turns.
    if last_human_index is not None:
        messages = messages[last_human_index:]

    # Map tool call IDs to their tool names.
    tool_names = {}

    for message in messages:

        for tool_call in getattr(message, "tool_calls", []) or []:
            tool_names[tool_call.get("id")] = tool_call.get("name")

        # Capture the corresponding tool result.
        tool_call_id = getattr(message, "tool_call_id", None)

        if not tool_call_id:
            continue

        tool_name = tool_names.get(tool_call_id)

        if not tool_name:
            continue

        if tool_name == "search_banking_knowledge":
            continue

        tool_result = getattr(message, "content", None)

        # Parse JSON results where possible.
        if isinstance(tool_result, str):
            try:
                tool_result = json.loads(tool_result)
            except (json.JSONDecodeError, TypeError):
                pass

        structured_results.append({
            "tool_name": tool_name,
            "result": tool_result,
        })

    return structured_results


# 3. RAG SOURCE EXTRACTION

def extract_rag_sources(messages):
    """
    Extract RAG sources generated during the latest user turn only.
    """

    messages = messages or []

    # Find the latest user message.
    last_human_index = None

    for index, message in enumerate(messages):
        if getattr(message, "type", None) == "human":
            last_human_index = index

    if last_human_index is not None:
        messages = messages[last_human_index:]

    # Map tool call IDs to tool names.
    tool_names = {}

    for message in messages:
        for tool_call in getattr(message, "tool_calls", []) or []:
            tool_names[tool_call.get("id")] = tool_call.get("name")

    sources = []
    seen_sources = set()

    # Extract results from the RAG tool only.
    for message in messages:

        tool_call_id = getattr(message, "tool_call_id", None)

        if not tool_call_id:
            continue

        if tool_names.get(tool_call_id) != "search_banking_knowledge":
            continue

        tool_result = getattr(message, "content", None)

        # Parse JSON-formatted tool results.
        if isinstance(tool_result, str):
            try:
                tool_result = json.loads(tool_result)
            except (json.JSONDecodeError, TypeError):
                continue

        if not isinstance(tool_result, dict):
            continue

        for source in tool_result.get("sources", []):

            if not isinstance(source, dict):
                continue

            source_name = source.get("source", "Unknown source")
            category = source.get("category", "Unknown category")

            # Avoid displaying duplicate source entries.
            source_key = (source_name, category)

            if source_key in seen_sources:
                continue

            seen_sources.add(source_key)

            sources.append({
                "source": source_name,
                "category": category
            })

    return sources


# 4. STRUCTURED RESULT RENDERING

def render_structured_result(structured_results):

    if not structured_results:
        st.caption("No structured result available for this response.")
        return

    for item in structured_results:

        tool_name = item.get("tool_name")
        result = item.get("result")

        if not isinstance(result, dict):
            st.write(result)
            continue

        # 1. EMI Calculation
        if tool_name == "calculate_emi":

            st.markdown("### 🧮 Loan EMI Breakdown")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Loan Amount",
                f"₹{result.get('loan_amount', 0):,.2f}"
            )

            col2.metric(
                "Annual Interest Rate",
                f"{result.get('annual_interest_rate', 0)}%"
            )

            col3.metric(
                "Tenure",
                f"{result.get('tenure_months', 0)} months"
            )

            st.divider()

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Monthly EMI",
                f"₹{result.get('monthly_emi', 0):,.2f}"
            )

            col2.metric(
                "Total Interest",
                f"₹{result.get('total_interest', 0):,.2f}"
            )

            col3.metric(
                "Total Repayment",
                f"₹{result.get('total_payment', 0):,.2f}"
            )

        # 2. Loan Comparison
        elif tool_name == "compare_loans":

            st.markdown("### 📊 Ready Bank Loan Comparison")

            available_loans = result.get("available_loans", [])

            if available_loans:
                st.table(available_loans)
            else:
                st.info("No loan comparison data is available.")

            if result.get("comparison_basis"):
                st.caption(
                    f"Comparison basis: {result['comparison_basis']}"
                )

            if result.get("disclaimer"):
                st.caption(result["disclaimer"])

        # 3. Loan Eligibility
        elif tool_name == "check_loan_eligibility":

            st.markdown("### 📋 Loan Eligibility Assessment")

            loan_type = result.get("loan_type", "Loan")
            status = result.get("status", "Not available")
            eligibility = result.get("preliminary_eligibility")

            if eligibility is True:
                eligibility_label = "Eligible"
            elif eligibility is False:
                eligibility_label = "Not eligible"
            else:
                eligibility_label = "Not available"

            st.write(f"**Loan Type:** {loan_type}")

            col1, col2 = st.columns(2)

            col1.metric("Status", str(status))

            col2.metric(
                "Preliminary Eligibility",
                eligibility_label
            )

            reasons = result.get("reasons", [])

            if reasons:

                st.markdown("**Assessment Details**")

                for reason in reasons:
                    st.write(f"- {reason}")

            if result.get("disclaimer"):
                st.caption(result["disclaimer"])

            with st.expander("View Complete Eligibility Details"):
                st.json(result)

        # 4. Account Transaction History
        elif tool_name == "get_account_transactions":

            st.subheader("💳 Account Transaction History")

            if result.get("status") != "success":
                st.warning(
                    result.get("message", "Unable to retrieve transactions.")
                )

            else:
                st.caption(
                    f"Account Reference: {result.get('account_ref')}"
                )

                st.metric(
                    "Total Transactions",
                    result.get("transaction_count", 0)
                )

                transactions = result.get("transactions", [])

                if transactions:
                    st.table(transactions)
                else:
                    st.info("No transactions found for the selected criteria.")

        # 5. Account Spending Summary
        elif tool_name == "get_spending_summary":

            st.subheader("📊 Account Spending Summary")

            if result.get("status") != "success":
                st.warning(
                    result.get("message", "Unable to retrieve spending summary.")
                )

            else:
                st.caption(
                    f"Account Reference: {result.get('account_ref')}"
                )

                col1, col2 = st.columns(2)

                col1.metric(
                    "Total Successful Spending",
                    f"₹{result.get('total_spending', 0):,.2f}"
                )

                col2.metric(
                    "Successful Debit Transactions",
                    result.get("transaction_count", 0)
                )

                st.caption(
                    "Only successful debit transactions are included."
                )

        # 6. Category-wise Spending
        elif tool_name == "get_category_spending":

            st.subheader("📊 Category-wise Spending")

            if result.get("status") != "success":
                st.warning(
                    result.get("message", "Unable to retrieve category spending.")
                )

            else:
                st.caption(
                    f"Account Reference: {result.get('account_ref')}"
                )

                categories = result.get("categories", [])

                if categories:
                    st.table(categories)
                else:
                    st.info("No category-wise spending found.")

                st.caption(
                    "Only successful debit transactions are included."
                )

        # 7. Monthly Spending
        elif tool_name == "get_monthly_spending":

            st.subheader("📅 Monthly Spending")

            if result.get("status") != "success":
                st.warning(
                    result.get("message", "Unable to retrieve monthly spending.")
                )

            else:
                st.caption(
                    f"Account Reference: {result.get('account_ref')}"
                )

                monthly_spending = result.get("monthly_spending", [])

                if monthly_spending:
                    st.table(monthly_spending)
                else:
                    st.info("No monthly spending data found.")

                st.caption(
                    "Only successful debit transactions are included."
                )

        # 8. Other Tools
        else:
            st.json(result)


# 5. AGENT ACTIVITY RENDERING

def render_agent_activity(limit=None):

    activity = st.session_state.get("agent_activity", [])

    if not activity:
        st.info("No agent tool executions recorded yet.")
        return

    # Display newest activity first.
    records = list(reversed(activity))

    if limit is not None:
        records = records[:limit]

    for record in records:

        title = (
            f"{record['tool_name']} — {record['status']}"
        )

        with st.expander(title, expanded=False):

            st.markdown("**Input Arguments**")
            st.json(record["arguments"])

            st.markdown("**Tool Result**")

            if record["result"] is None:
                st.caption(
                    "The tool has not returned a result yet."
                )

            elif isinstance(record["result"], (dict, list)):
                st.json(record["result"])

            else:
                st.write(record["result"])


# 6. THEME STYLING


def apply_theme(theme):

    if theme == "Dark":

        background = "#101827"
        surface = "#1B293B"
        text = "#5FABF7"
        muted = "#AEB6C0"
        border = "#34445A"
        accent = "#60A5FA"

    else:

        background = "#F5F7FB"
        surface = "#FFFFFF"
        text = "#172B4D"
        muted = "#64748B"
        border = "#E2E8F0"
        accent = "#2563EB"

    st.markdown(
        f"""
        <style>

        /* --------------------------------
           STREAMLIT THEME VARIABLES
        -------------------------------- */

        .stApp {{
            --background-color: {background};
            --secondary-background-color: {surface};
            --text-color: {text};
            --primary-color: {accent};

            background-color: {background} !important;
            color: {text} !important;
        }}

        /* --------------------------------
           MAIN APPLICATION
        -------------------------------- */

        [data-testid="stAppViewContainer"] {{
            background-color: {background} !important;
        }}

        [data-testid="stHeader"] {{
            background-color: {background} !important;
        }}

        [data-testid="stSidebar"] {{
            background-color: {surface} !important;
            border-right: 1px solid {border};
        }}

        /* --------------------------------
           TEXT AND METRICS
        -------------------------------- */

        h1, h2, h3, p, label {{
            color: {text};
        }}

        [data-testid="stMetric"] {{
            background-color: {surface};
            border: 1px solid {border};
            padding: 18px;
            border-radius: 12px;
        }}

        [data-testid="stMetricLabel"] {{
            color: {muted};
        }}

        /* --------------------------------
           DASHBOARD COMPONENTS
        -------------------------------- */

        .welcome-card {{
            background-color: {surface};
            border: 1px solid {border};
            border-radius: 14px;
            padding: 24px;
            margin-bottom: 20px;
        }}

        .welcome-card h2 {{
            color: {text};
            margin-top: 0;
        }}

        .welcome-card p {{
            color: {muted};
        }}

        .section-caption {{
            color: {muted};
            font-size: 13px;
        }}

        /* --------------------------------
           BUTTONS
        -------------------------------- */

        div.stButton > button {{
            border-radius: 9px;
            border: 1px solid {border};
            min-height: 44px;
        }}

        div.stButton > button:hover {{
            border-color: {accent};
            color: {accent};
        }}

        /* --------------------------------
           CHAT INPUT BOTTOM CONTAINER
        -------------------------------- */

        [data-testid="stBottom"] {{
            background: {background} !important;
            background-image: none !important;
        }}

        [data-testid="stBottom"] > div {{
            background: {background} !important;
            background-image: none !important;
        }}

        [data-testid="stBottom"]::before {{
            background: {background} !important;
        }}

        /* --------------------------------
           CHAT INPUT BOX
        -------------------------------- */

        [data-testid="stChatInput"],
        [data-testid="stChatInput"] > div,
        [data-testid="stChatInput"] > div > div {{
            background-color: {surface} !important;
            border-color: {border} !important;
        }}

        [data-testid="stChatInput"] {{
            border: 1px solid {border} !important;
            border-radius: 12px !important;
        }}

        [data-testid="stChatInput"] textarea {{
            background-color: {surface} !important;
            color: {text} !important;
            caret-color: {text} !important;
        }}

        [data-testid="stChatInput"] textarea::placeholder {{
            color: {muted} !important;
            opacity: 1 !important;
        }}

        [data-testid="stChatInput"] button {{
            background-color: {surface} !important;
            color: {text} !important;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )
