
import streamlit as st
import uuid

from langchain_core.messages import HumanMessage
from langgraph.types import Command

from agents.graph import agent

from ui.common import (
    update_agent_activity,
    extract_structured_results,
    extract_rag_sources,
    render_structured_result,
    render_agent_activity,
)


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

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": assistant_response,

                    "structured_results": extract_structured_results(
                        result.get("messages", [])
                    ),

                    "sources": extract_rag_sources(
                        result.get("messages", [])
                    ),
                })

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

                    sources = message.get("sources", [])

                    if sources:

                        st.caption(
                            "Retrieved documents from the Ready Bank knowledge base."
                        )

                        for source in sources:

                            st.markdown(
                                f"**{source.get('source', 'Unknown source')}**"
                            )

                            st.caption(
                                f"Category: {source.get('category', 'Unknown category')}"
                            )

                    else:

                        st.caption(
                            "No knowledge-base sources were retrieved for this response."
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
