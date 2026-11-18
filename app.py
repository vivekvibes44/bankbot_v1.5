import streamlit as st

# 1. Page configuration

st.set_page_config(
    page_title="Ready Bank | AI Banking Assistant",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# 2. Session state

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if "navigation_radio" not in st.session_state:
    st.session_state.navigation_radio = "Dashboard"


def navigate_to(page):
    st.session_state.navigation_radio = page


# 3. Theme styling

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


# 4. Sidebar and navigation

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

    st.session_state.theme = "Dark" if selected_theme else "Light"

    st.divider()

    st.caption("Ready Bank")
    st.caption(
        "Demo environment: No real bank accounts, transactions "
        "or financial operations are connected."
    )


# Apply the selected theme

apply_theme(st.session_state.theme)


# 5. Dashboard homepage

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


# 6. Placeholder pages

def show_placeholder(title, description):

    st.title(title)
    st.info(description)
    st.caption("This section will be implemented in a later milestone.")



# 7. AI Assistant page

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

    # New Chat button

    col1, col2 = st.columns([5, 1])

    with col2:
        if st.button("➕ New Chat", use_container_width=True):

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

            st.rerun()

    # Agent activity panel

    with st.expander("🤖 Agent Activity", expanded=False):

        st.caption(
            "Example workflow — live agent execution will be added later."
        )

        st.markdown(
            """
            1. **Understand request** — Identify the user's question.
            2. **Select capability** — Determine which tool or knowledge source is needed.
            3. **Process request** — Execute the required operation.
            4. **Prepare response** — Format the result for the user.
            """
        )

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
                user_input = "What account options are available?"

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
                user_input = "What are the loan eligibility requirements?"

            if st.button(
                "📄 What documents are needed to open an account?",
                use_container_width=True,
            ):
                user_input = "What documents are needed to open an account?"

    # Chat input

    typed_input = st.chat_input(
        "Ask Ready Bank something..."
    )

    if typed_input:
        user_input = typed_input

    # Process user message

    if user_input:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        # Temporary demo response

        demo_response = (
            "Thank you for your question!\n\n"
            "I'm currently running in **UI demo mode**. "
            "My banking knowledge, AI reasoning, and tools "
            "will be connected in a later development milestone."
        )

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": demo_response,
            }
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

                # Structured response preview

                with st.expander("📊 Structured Result"):

                    st.caption(
                        "Depending on your request, the assistant "
                        "will display structured results such as:"
                    )

                    st.markdown(
                        """
                        - **Banking information:** Details with source citations.
                        - **Loan calculations:** EMI, interest and repayment breakdown.
                        - **Loan eligibility:** Eligibility results and document checklists.
                        """
                    )

                    st.caption(
                        "These result types will be populated when the backend is integrated."
                    )


# 8. Page routing

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

    show_placeholder(
        "Activity History",
        "Review previous conversations and completed workflows.",
    )

elif selected_page == "Settings":

    st.title("Settings")
    st.subheader("Appearance")
    st.write(f"Current theme: **{st.session_state.theme}**")
    st.caption("Additional application settings will be added later.")
