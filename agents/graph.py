
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from agents.llm import get_llm
from tools.loan_tools import calculate_emi


# 1. Define available tools
tools = [calculate_emi]


# 2. Initialize LLM with tools
llm = get_llm()
llm_with_tools = llm.bind_tools(tools)


# 3. System instructions
SYSTEM_PROMPT = """
You are the AI assistant for Ready Bank, a fictional banking
demonstration application.

You can help users with banking questions and loan calculations.

Rules:
1. Use calculate_emi whenever the user requests an EMI calculation.
2. Never calculate EMI mentally.
3. Ask for missing inputs before calling a tool.
4. Never invent Ready Bank products, policies, fees or interest rates.
5. Do not claim to access real bank accounts or perform real transactions.
6. Use tool results as the source of truth for calculations.
7. Communicate clearly and professionally.
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

    graph.add_node(
        "tools",
        ToolNode(tools)
    )

    # Starting point
    graph.add_edge(START, "assistant")

    # Decide whether to execute a tool or finish
    graph.add_conditional_edges(
        "assistant",
        tools_condition
    )

    # Return tool results to the LLM
    graph.add_edge("tools", "assistant")

    return graph.compile()


# 6. Create the agent
agent = build_agent()
