
from agents.llm import generate_response


messages = [
    {
        "role": "user",
        "content": "My name is Alex."
    },
    {
        "role": "assistant",
        "content": "Hello Alex! Nice to meet you."
    },
    {
        "role": "user",
        "content": "What is my name?"
    }
]

try:

    response = generate_response(messages)

    print("\nConversation Context Test:\n")
    print(response)

except Exception as e:

    print("\nLLM Test Failed:")
    print(e)
