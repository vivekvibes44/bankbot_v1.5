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

if "page_navigation" not in st.session_state:
    st.session_state.page_navigation = "Dashboard"


def navigate_to(page):
    st.session_state.navigation_radio = page


# 3. Theme styling

def apply_theme(theme):
    if theme == "Dark":
        background = "#101827"
        surface = "#1B293B"
        text = "#F1F5F9"
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
    st.caption("Demo environment: No real bank accounts, transactions or financial operations are connected.")


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


# 7. Page routing

if selected_page == "Dashboard":
    show_dashboard()

elif selected_page == "AI Assistant":
    show_placeholder(
        "AI Banking Assistant",
        "Your conversational banking assistant will be built here.",
    )

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
