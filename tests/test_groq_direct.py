from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL


def test_groq_direct():

    print("Initializing Groq SDK directly...")

    client = Groq(
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com"
    )

    print("Base URL:", client.base_url)
    print("Model:", LLM_MODEL)

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": "Reply with: Groq connection successful."
            }
        ],
        temperature=0
    )

    print("\nGroq Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    test_groq_direct()
