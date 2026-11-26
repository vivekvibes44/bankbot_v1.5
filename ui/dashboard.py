import streamlit as st


def navigate_to(page):
    """
    Navigate to another page using the sidebar navigation radio.
    """
    st.session_state.navigation_radio = page


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
