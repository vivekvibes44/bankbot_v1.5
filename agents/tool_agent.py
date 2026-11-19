
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from agents.llm import get_llm
from tools.loan_tools import calculate_emi


# Available tools
tools = [calculate_emi]


# Initialize LLM with tools
llm = get_llm()
llm_with_tools = llm.bind_tools(tools)


SYSTEM_PROMPT = """
You are the AI assistant for Ready Bank, a fictional banking
demonstration application.

You can help users with general banking questions and loan calculations.

Rules:
1. Use the calculate_emi tool whenever the user requests an EMI calculation.
2. Never calculate EMI mentally.
3. Use the exact inputs supplied by the user.
4. If an essential input is missing, ask the user for clarification.
5. Do not invent banking products, policies, fees or interest rates.
6. Clearly communicate when information is unavailable.
"""


def run_tool_agent(user_message):

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_message)
    ]

    # Ask LLM to decide whether a tool is required
    response = llm_with_tools.invoke(messages)

    # Check whether LLM requested a tool
    if response.tool_calls:

        for tool_call in response.tool_calls:

            if tool_call["name"] == "calculate_emi":

                tool_result = calculate_emi.invoke(
                    tool_call["args"]
                )

                messages.append(response)

                messages.append(
                    ToolMessage(
                        content=str(tool_result),
                        tool_call_id=tool_call["id"]
                    )
                )

        # Ask LLM to formulate the final response
        final_response = llm.invoke(messages)

        return final_response.content

    return response.content
