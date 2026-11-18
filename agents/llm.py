
from langchain_groq import ChatGroq

from config import GROQ_API_KEY, LLM_MODEL


# Ready Bank assistant instructions

SYSTEM_PROMPT = """
You are the AI assistant for Ready Bank, a fictional banking
demonstration application.

Your responsibilities:
1. Help users understand general banking concepts.
2. Assist with questions about loans and banking services.
3. Communicate clearly and professionally.
4. Ask for clarification when a request is unclear.

Important rules:
- Do not invent Ready Bank policies, fees, interest rates or products.
- Do not claim to have accessed real bank accounts.
- Do not claim to have completed real financial transactions.
- If you do not have sufficient information, clearly say so.
- Actual financial calculations will be handled by dedicated
  Python tools in later development stages.
"""


def get_llm():

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing from the .env file.")

    if not LLM_MODEL:
        raise ValueError("LLM_MODEL is missing from the .env file.")

    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=LLM_MODEL,
        temperature=0.2,
        max_tokens=1024,
    )

    return llm


def generate_response(messages):

    llm = get_llm()

    formatted_messages = [
        ("system", SYSTEM_PROMPT)
    ]

    for message in messages:

        role = message["role"]
        content = message["content"]

        if role in ["user", "assistant"]:
            formatted_messages.append((role, content))

    response = llm.invoke(formatted_messages)

    return response.content
