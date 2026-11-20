from langchain_openai import OpenAIEmbeddings

from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    EMBEDDING_MODEL
)


def get_embeddings():
    """Initialize and return the OpenRouter embedding model."""

    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is missing.")

    return OpenAIEmbeddings(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
        model=EMBEDDING_MODEL,
        check_embedding_ctx_length=False
    )
