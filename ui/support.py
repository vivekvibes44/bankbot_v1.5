
import streamlit as st
import uuid

from langchain_core.messages import HumanMessage
from langgraph.types import Command

from agents.graph import agent

from tools.complaint_tools import track_complaint
from database.complaint_repository import VALID_CATEGORIES

from ui.common import (
    update_agent_activity,
    extract_structured_results,
    render_structured_result,
)


def render_complaint_result(result):

    if not isinstance(result, dict):
        st.write(result)
        return

    status = result.get("status", "")

    if status in ["success", "registered", "found"]:
        st.success(result.get("message", "Request completed successfully."))
    elif status in ["not_found", "invalid_input", "error"]:
        st.error(result.get("message", "Unable to complete the request."))
    elif result.get("message"):
        st.info(result["message"])

    # Display important complaint details.
    display_fields = [
        ("Complaint ID", "complaint_id"),
        ("Category", "category"),
        ("Description", "description"),
        ("Current Status", "complaint_status"),
        ("Status", "status"),
        ("Created At", "created_at"),
        ("Updated At", "updated_at"),
    ]

    displayed_keys = set()

    st.divider()

    for label, key in display_fields:

        value = result.get(key)

        if value is not None and key != "status":
            st.write(f"**{label}:** {value}")
            displayed_keys.add(key)

    # Display any additional fields returned by the repository.
    excluded_keys = displayed_keys | {"status", "message"}

    for key, value in result.items():

        if key not in excluded_keys:
            formatted_label = key.replace("_", " ").title()
            st.write(f"**{formatted_label}:** {value}")


def show_support():

    st.title("Customer Support")

    st.write(
        "Register a complaint or track the progress "
        "of an existing complaint."
    )

    st.divider()

    # Initialize independent Support state.
    if "support_thread_id" not in st.session_state:
        st.session_state.support_thread_id = str(uuid.uuid4())

    if "support_pending_approval" not in st.session_state:
        st.session_state.support_pending_approval = None

    if "support_registration_result" not in st.session_state:
        st.session_state.support_registration_result = None

    if "support_assistant_response" not in st.session_state:
        st.session_state.support_assistant_response = None

    register_tab, track_tab = st.tabs(
        [
            "Register Complaint",
            "Track Complaint",
        ]
    )

    # REGISTER COMPLAINT

    with register_tab:

        st.subheader("Register a New Complaint")

        st.write(
            "Provide the details of your issue. "
            "You will be asked to approve the registration "
            "before it is saved."
        )

        if not st.session_state.support_pending_approval:

            with st.form("support_complaint_form"):

                category = st.selectbox(
                    "Complaint Category",
                    VALID_CATEGORIES,
                )

                description = st.text_area(
                    "Complaint Description",
                    placeholder=(
                        "Describe your issue in detail..."
                    ),
                    height=150,
                )

                submit_button = st.form_submit_button(
                    "Submit Complaint",
                    use_container_width=True,
                    type="primary",
                )

            if submit_button:

                if not description.strip():

                    st.error(
                        "Please provide a complaint description."
                    )

                else:

                    user_message = (
                        "Please register a complaint with the "
                        f"category '{category}' and the following "
                        f"description: {description.strip()}"
                    )

                    config = {
                        "configurable": {
                            "thread_id": st.session_state.support_thread_id
                        }
                    }

                    try:

                        with st.spinner(
                            "Submitting your complaint for review..."
                        ):

                            result = agent.invoke(
                                {
                                    "messages": [
                                        HumanMessage(content=user_message)
                                    ]
                                },
                                config=config,
                            )

                        interrupts = result.get("__interrupt__", [])

                        update_agent_activity(
                            result.get("messages", []),
                            pending_approval=bool(interrupts),
                        )

                        if interrupts:

                            st.session_state.support_pending_approval = (
                                interrupts[0].value
                            )

                        else:

                            st.session_state.support_assistant_response = (
                                result["messages"][-1].content
                            )

                            st.session_state.support_registration_result = (
                                extract_structured_results(
                                    result.get("messages", [])
                                )
                            )

                        st.rerun()

                    except Exception as error:

                        st.error(
                            f"Unable to submit complaint: {error}"
                        )

        # APPROVAL REVIEW

        if st.session_state.support_pending_approval:

            approval_data = (
                st.session_state.support_pending_approval
            )

            st.divider()

            st.subheader("Complaint Registration Review")

            st.warning(
                "Please review the complaint details carefully. "
                "The complaint will only be saved after your approval."
            )

            st.write(
                f"**Category:** {approval_data['category']}"
            )

            st.write(
                f"**Description:** {approval_data['description']}"
            )

            st.caption(
                "Approving this request will save the complaint "
                "in the simulated Ready Bank database."
            )

            col1, col2 = st.columns(2)

            config = {
                "configurable": {
                    "thread_id": st.session_state.support_thread_id
                }
            }

            with col1:

                if st.button(
                    "Approve & Register",
                    use_container_width=True,
                    type="primary",
                    key="support_approve_complaint",
                ):

                    try:

                        with st.spinner(
                            "Registering your complaint..."
                        ):

                            result = agent.invoke(
                                Command(
                                    resume={"approved": True}
                                ),
                                config=config,
                            )

                        update_agent_activity(
                            result.get("messages", [])
                        )

                        st.session_state.support_pending_approval = None

                        st.session_state.support_assistant_response = (
                            result["messages"][-1].content
                        )

                        st.session_state.support_registration_result = (
                            extract_structured_results(
                                result.get("messages", [])
                            )
                        )

                        st.rerun()

                    except Exception as error:

                        st.error(
                            f"Complaint registration failed: {error}"
                        )

            with col2:

                if st.button(
                    "Reject",
                    use_container_width=True,
                    key="support_reject_complaint",
                ):

                    try:

                        with st.spinner(
                            "Cancelling complaint registration..."
                        ):

                            result = agent.invoke(
                                Command(
                                    resume={"approved": False}
                                ),
                                config=config,
                            )

                        update_agent_activity(
                            result.get("messages", [])
                        )

                        st.session_state.support_pending_approval = None

                        st.session_state.support_assistant_response = (
                            result["messages"][-1].content
                        )

                        st.session_state.support_registration_result = (
                            extract_structured_results(
                                result.get("messages", [])
                            )
                        )

                        st.rerun()

                    except Exception as error:

                        st.error(
                            f"Unable to cancel registration: {error}"
                        )

        # REGISTRATION RESPONSE

        if st.session_state.support_assistant_response:

            st.divider()

            st.subheader("Registration Response")

            st.markdown(
                st.session_state.support_assistant_response
            )

            structured_results = (
                st.session_state.support_registration_result
            )

            if structured_results:

                with st.expander(
                    "Complaint Details",
                    expanded=True,
                ):

                    render_structured_result(
                        structured_results
                    )

    # TRACK COMPLAINT

    with track_tab:

        st.subheader("Track an Existing Complaint")

        st.write(
            "Enter the complaint ID provided when "
            "your complaint was registered."
        )

        with st.form("track_complaint_form"):

            complaint_id = st.text_input(
                "Complaint ID",
                placeholder="Example: RB-XXXXXXXX",
            )

            track_button = st.form_submit_button(
                "Track Complaint",
                use_container_width=True,
                type="primary",
            )

        if track_button:

            if not complaint_id.strip():

                st.error("Please enter a complaint ID.")

            else:

                try:

                    with st.spinner(
                        "Retrieving complaint details..."
                    ):

                        result = track_complaint.invoke({
                            "complaint_id": complaint_id.strip()
                        })

                    st.session_state.support_tracking_result = result

                except Exception as error:

                    st.error(
                        f"Unable to track complaint: {error}"
                    )

        if st.session_state.get("support_tracking_result") is not None:

            st.divider()

            st.subheader("Complaint Tracking Result")

            render_complaint_result(
                st.session_state.support_tracking_result
            )
