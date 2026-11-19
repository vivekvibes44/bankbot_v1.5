from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from agents.llm import get_llm
from tools.loan_tools import (
    calculate_emi,
    check_loan_eligibility,
    compare_loans
)
from tools.complaint_tools import track_complaint
from langgraph.checkpoint.memory import InMemorySaver

from tools.complaint_tools import (
    register_complaint,
    track_complaint
)

# 1. Define available tools
tools = [calculate_emi, check_loan_eligibility, compare_loans, register_complaint, track_complaint]


# 2. Initialize LLM with tools
llm = get_llm()
llm_with_tools = llm.bind_tools(tools)


# 3. System instructions
SYSTEM_PROMPT = """
You are the AI assistant for Ready Bank, a fictional banking
demonstration application.

You can help users with banking questions and loan calculations.

Available tools:

1. calculate_emi:
   Use this whenever the user requests an EMI calculation.
   Required inputs:
   - principal
   - annual_interest_rate
   - tenure_months

2. check_loan_eligibility:
   Use this whenever the user requests a preliminary loan
   eligibility check.
   Required inputs:
   - loan_type
   - age
   - monthly_income

3. compare_loans:
Use this whenever the user wants to compare
available Ready Bank loan products.

4. register_complaint:
   Use this whenever the user explicitly wants to register
   a complaint.

   Required inputs:
   - category
   - description

   Ask for missing information before calling the tool.
   Never claim that a complaint has been registered until
   the tool returns a successful result.
   The tool will pause and request human approval.
   Never attempt to approve the registration yourself.

5. track_complaint:
   Use this whenever the user wants to check or track
   an existing complaint.

   Required input:
   - complaint_id

   Never invent a complaint ID.
   Ask the user for the ID if it is missing.

This tool requires no user inputs.

Rules:
1. Always use the appropriate tool for calculations and eligibility checks.
2. Never calculate EMI or determine eligibility mentally.
3. Ask the user for missing inputs before calling a tool.
4. Never invent Ready Bank products, policies, fees or interest rates.
5. Do not claim to access real bank accounts or perform real transactions.
6. Treat tool results as the source of truth.
7. Clearly explain eligibility results and their reasons.
8. Eligibility checks are preliminary simulations, not loan approvals.
9. Communicate clearly and professionally.
10. Never invent loan interest rates or eligibility criteria. Use the loan tools for all loan-related comparisons.
"""


# 4. LLM node
def assistant_node(state: MessagesState):

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"]
    ]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


# 5. Build the LangGraph workflow
def build_agent():
    graph = StateGraph(MessagesState)

    graph.add_node("assistant", assistant_node)
    graph.add_node("tools", ToolNode(tools))

    graph.add_edge(START, "assistant")
    graph.add_conditional_edges("assistant", tools_condition)
    graph.add_edge("tools", "assistant")

    checkpointer = InMemorySaver()

    return graph.compile(checkpointer=checkpointer)

agent = build_agent()
