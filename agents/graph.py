
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from agents.llm import generate_response


# 1. Define the graph state
class AgentState(TypedDict):
    messages: list


# 2. Define the LLM node
def generate_response_node(state: AgentState):

    response = generate_response(state["messages"])

    return {
        "messages": [
            *state["messages"],
            {
                "role": "assistant",
                "content": response
            }
        ]
    }


# 3. Build the graph
def build_agent():

    graph = StateGraph(AgentState)

    graph.add_node("generate_response", generate_response_node)

    graph.add_edge(START, "generate_response")
    graph.add_edge("generate_response", END)

    return graph.compile()


# 4. Create the agent
agent = build_agent()
