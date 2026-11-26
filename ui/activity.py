import streamlit as st

from ui.common import render_agent_activity


def show_activity():

    st.title("Activity History")

    st.write(
        "Review the tools selected by the AI agent, "
        "their inputs, outputs and execution status."
    )

    st.divider()

    render_agent_activity()
