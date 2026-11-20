from rag.vector_store import load_vector_store


def get_retriever(
    search_type: str = "similarity",
    search_kwargs: dict | None = None
):
    """
    Load the FAISS vector store and return a retriever.

    Args:
        search_type: Retrieval strategy.
        search_kwargs: Search configuration, such as the number
                       of documents to retrieve.

    Returns:
        A LangChain retriever.
    """

    vector_store = load_vector_store()

    if search_kwargs is None:
        search_kwargs = {"k": 3}

    retriever = vector_store.as_retriever(
        search_type=search_type,
        search_kwargs=search_kwargs
    )

    return retriever
