import streamlit as st
import uuid

from langchain_core.messages import HumanMessage
from langgraph.types import Command

from agents.graph import agent

from ui.common import (
    apply_theme,
    update_agent_activity,
    extract_structured_results,
    extract_rag_sources,
    render_structured_result,
    render_agent_activity,
)

from ui.dashboard import show_dashboard
from ui.assistant import show_ai_assistant

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


# 3. SIDEBAR AND NAVIGATION

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


# 4. PLACEHOLDER PAGES

def show_placeholder(title, description):

    st.title(title)
    st.info(description)

    st.caption(
        "This section will be implemented in a later milestone."
    )


# 5. PAGE ROUTING

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
