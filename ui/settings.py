import streamlit as st


def show_settings():

    st.title("Settings")

    st.subheader("Appearance")

    st.write(
        f"Current theme: **{st.session_state.theme}**"
    )

    st.caption(
        "Additional application settings will be added later."
    )
