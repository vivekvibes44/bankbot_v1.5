from langchain_openai import OpenAIEmbeddings

from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    EMBEDDING_MODEL
)


def get_embeddings(model_name=None):
    """Initialize and return the selected OpenRouter embedding model."""

    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is missing.")

    selected_model = model_name or EMBEDDING_MODEL

    if not selected_model:
        raise ValueError("Embedding model is missing.")

    return OpenAIEmbeddings(
        api_key=OPENROUTER_API_KEY,
        base_url=OPENROUTER_BASE_URL,
        model=selected_model,
        check_embedding_ctx_length=False
    )
