
import streamlit as st
import uuid
import json

from langchain_core.messages import HumanMessage
from langgraph.types import Command

from agents.graph import agent


# 1. PAGE CONFIGURATION

st.set_page_config(
    page_title="Ready Bank | AI Banking Assistant",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# 2. SESSION STATE

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if "navigation_radio" not in st.session_state:
    st.session_state.navigation_radio = "Dashboard"

if "agent_activity" not in st.session_state:
    st.session_state.agent_activity = []


def navigate_to(page):
    st.session_state.navigation_radio = page


# 3. AGENT ACTIVITY TRACKING

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


# 4. THEME STYLING

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
        .stApp {{
            background-color: {background};
            color: {text};
        }}

        [data-testid="stSidebar"] {{
            background-color: {surface};
            border-right: 1px solid {border};
        }}

        [data-testid="stHeader"] {{
            background-color: {background};
        }}

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

        div.stButton > button {{
            border-radius: 9px;
            border: 1px solid {border};
            min-height: 44px;
        }}

        div.stButton > button:hover {{
            border-color: {accent};
            color: {accent};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# 5. SIDEBAR AND NAVIGATION

with st.sidebar:

    st.markdown("# 🏦 Ready Bank")
    st.caption("AI-powered banking assistant")

    st.divider()

    st.markdown("### Navigation")

    pages = [
        "Dashboard",
        "AI Assistant",
        "Loans",
        "Transactions",
        "Support",
        "Activity",
        "Settings",
    ]

    selected_page = st.radio(
        "Go to",
        pages,
        key="navigation_radio",
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("### Appearance")

    selected_theme = st.toggle(
        "Dark mode",
        value=st.session_state.theme == "Dark",
    )

    st.session_state.theme = (
        "Dark" if selected_theme else "Light"
    )

    st.divider()

    st.caption("Ready Bank")

    st.caption(
        "Demo environment: No real bank accounts, transactions "
        "or financial operations are connected."
    )

# Apply selected theme
apply_theme(st.session_state.theme)


# 6. DASHBOARD HOMEPAGE

def show_dashboard():

    st.title("Dashboard")

    st.markdown(
        """
        <div class="welcome-card">
            <h2>Welcome to Ready Bank!</h2>
            <p>
                Your intelligent banking assistant.
                Explore banking information, calculate loan EMIs,
                and manage your simulated banking activities.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Demo Accounts", "Coming soon")
    col2.metric("Transactions", "Coming soon")
    col3.metric("Active Complaints", "Coming soon")

    st.divider()

    st.subheader("Ready Bank AI Assistant")

    st.write(
        "Ask banking questions, explore loan options, "
        "or get help with your simulated banking activities."
    )

    st.button(
        "💬 Open AI Assistant",
        use_container_width=True,
        on_click=navigate_to,
        args=("AI Assistant",),
    )

    st.divider()

    st.subheader("Quick Actions")

    col1, col2 = st.columns(2)

    with col1:

        st.button(
            "🧮 EMI Calculator",
            use_container_width=True,
            on_click=navigate_to,
            args=("Loans",),
        )

        st.button(
            "📊 Spending Analysis",
            use_container_width=True,
            on_click=navigate_to,
            args=("Transactions",),
        )

    with col2:

        st.button(
            "📋 Loan Eligibility",
            use_container_width=True,
            on_click=navigate_to,
            args=("Loans",),
        )

        st.button(
            "🎧 Register a Complaint",
            use_container_width=True,
            on_click=navigate_to,
            args=("Support",),
        )

    st.divider()

    st.caption(
        "Demo environment: No real bank accounts, transactions "
        "or financial operations are connected."
    )


# 7. PLACEHOLDER PAGES

def show_placeholder(title, description):

    st.title(title)
    st.info(description)

    st.caption(
        "This section will be implemented in a later milestone."
    )


# 8. AI ASSISTANT PAGE

def show_ai_assistant():

    st.title("Ready Bank AI Assistant")

    st.write(
        "Your virtual banking assistant. Ask questions about "
        "banking, loans, or your simulated banking activities."
    )

    st.divider()

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "assistant",
                "content": (
                    "Hello! Welcome to Ready Bank. 👋\n\n"
                    "I'm your virtual banking assistant. "
                    "How can I help you today?"
                ),
            }
        ]

    # Initialize LangGraph thread ID
    if "agent_thread_id" not in st.session_state:
        st.session_state.agent_thread_id = str(uuid.uuid4())

    # Initialize pending approval
    if "pending_approval" not in st.session_state:
        st.session_state.pending_approval = None

    # New Chat button
    col1, col2 = st.columns([5, 1])

    with col2:
        if st.button(
            "➕ New Chat",
            use_container_width=True
        ):

            st.session_state.chat_history = [
                {
                    "role": "assistant",
                    "content": (
                        "Hello! Welcome to Ready Bank. 👋\n\n"
                        "I'm your virtual banking assistant. "
                        "How can I help you today?"
                    ),
                }
            ]

            st.session_state.agent_thread_id = str(uuid.uuid4())

            st.session_state.pending_approval = None

            st.rerun()

    # Agent Activity panel
    with st.expander("🤖 Agent Activity", expanded=False):

        st.caption(
            "Actual LangGraph tool execution history."
        )

        render_agent_activity(limit=5)

    # Suggested prompts
    user_input = None

    if len(st.session_state.chat_history) == 1:

        st.subheader("Suggested questions")

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "🏦 What account options are available?",
                use_container_width=True,
            ):

                user_input = (
                    "What account options are available?"
                )

            if st.button(
                "🧮 Calculate my loan EMI",
                use_container_width=True,
            ):

                user_input = "Calculate my loan EMI."

        with col2:

            if st.button(
                "📋 What are the loan eligibility requirements?",
                use_container_width=True,
            ):

                user_input = (
                    "What are the loan eligibility requirements?"
                )

            if st.button(
                "📄 What documents are needed to open an account?",
                use_container_width=True,
            ):

                user_input = (
                    "What documents are needed to open an account?"
                )

    # Chat input
    typed_input = st.chat_input(
        "Ask Ready Bank something..."
    )

    if typed_input:
        user_input = typed_input

    # Process user message
    if user_input and not st.session_state.pending_approval:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        config = {
            "configurable": {
                "thread_id": st.session_state.agent_thread_id
            }
        }

        try:

            with st.spinner(
                "Ready Bank Assistant is thinking..."
            ):

                result = agent.invoke(
                    {
                        "messages": [
                            HumanMessage(content=user_input)
                        ]
                    },
                    config=config
                )

            # Check whether graph paused for approval.
            interrupts = result.get("__interrupt__", [])

            # Record actual tool calls and results.
            update_agent_activity(
                result.get("messages", []),
                pending_approval=bool(interrupts)
            )

            if interrupts:

                st.session_state.pending_approval = (
                    interrupts[0].value
                )

            else:

                assistant_response = (
                    result["messages"][-1].content
                )

                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": assistant_response,
                        "structured_results": extract_structured_results(
                            result.get("messages", [])
                        ),
                    }
                )

            # Refresh the page to display updated Agent Activity.
            st.rerun()

        except Exception as e:

            st.error(
                f"Something went wrong: {str(e)}"
            )

    # Display conversation history
    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if message["role"] == "assistant":

                # Sources section
                with st.expander("📚 Sources"):

                    st.caption(
                        "Source citations will appear here when RAG is integrated."
                    )

                # Structured Result

                with st.expander("📊 Structured Result"):

                    render_structured_result(
                        message.get("structured_results", [])
                    )

    # Complaint registration approval interface
    if st.session_state.pending_approval:

        approval_data = st.session_state.pending_approval

        st.divider()

        st.subheader("📋 Complaint Registration Review")

        st.warning(
            "Please review your complaint details before registration."
        )

        st.markdown(f"""
        **Complaint Category:** {approval_data["category"]}

        **Description:** {approval_data["description"]}
        """)

        st.caption(
            "Your complaint will only be saved after you approve it."
        )

        col1, col2 = st.columns(2)

        config = {
            "configurable": {
                "thread_id": st.session_state.agent_thread_id
            }
        }

        # Approve complaint
        with col1:

            if st.button(
                "✅ Approve & Register",
                use_container_width=True,
                type="primary",
                key="approve_complaint"
            ):

                try:

                    with st.spinner(
                        "Registering your complaint..."
                    ):

                        result = agent.invoke(
                            Command(
                                resume={"approved": True}
                            ),
                            config=config
                        )

                    # Update existing tool activity record.
                    update_agent_activity(
                        result.get("messages", [])
                    )

                    st.session_state.pending_approval = None

                    assistant_response = (
                        result["messages"][-1].content
                    )

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": assistant_response,
                            "structured_results": extract_structured_results(
                                result.get("messages", [])
                            ),
                        }
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Complaint registration failed: {str(e)}"
                    )

        # Reject complaint
        with col2:

            if st.button(
                "❌ Reject",
                use_container_width=True,
                key="reject_complaint"
            ):

                try:

                    with st.spinner(
                        "Cancelling complaint registration..."
                    ):

                        result = agent.invoke(
                            Command(
                                resume={"approved": False}
                            ),
                            config=config
                        )

                    # Update existing tool activity record.
                    update_agent_activity(
                        result.get("messages", [])
                    )

                    st.session_state.pending_approval = None

                    assistant_response = (
                        result["messages"][-1].content
                    )

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": assistant_response,
                            "structured_results": extract_structured_results(
                                result.get("messages", [])
                            ),
                        }
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Unable to cancel registration: {str(e)}"
                    )


# 9. PAGE ROUTING

if selected_page == "Dashboard":

    show_dashboard()

elif selected_page == "AI Assistant":

    show_ai_assistant()

elif selected_page == "Loans":

    show_placeholder(
        "Loan Services",
        "Explore loan eligibility, EMI calculations and loan comparisons.",
    )

elif selected_page == "Transactions":

    show_placeholder(
        "Transaction Analysis",
        "View synthetic transactions and spending insights.",
    )

elif selected_page == "Support":

    show_placeholder(
        "Customer Support",
        "Register and track simulated banking complaints.",
    )

elif selected_page == "Activity":

    st.title("Activity History")

    st.write(
        "Review the tools selected by the AI agent, "
        "their inputs, outputs and execution status."
    )

    st.divider()

    render_agent_activity()

elif selected_page == "Settings":

    st.title("Settings")

    st.subheader("Appearance")

    st.write(
        f"Current theme: **{st.session_state.theme}**"
    )

    st.caption(
        "Additional application settings will be added later."
    )
