from rag.retriever import get_retriever


def test_retriever():

    print("Initializing retriever...")

    retriever = get_retriever()

    query = "What is the minimum balance required for a savings account?"

    print(f"\nQuery: {query}")

    results = retriever.invoke(query)

    print("\n--- Retriever Results ---")

    for index, document in enumerate(results, start=1):

        print(f"\nResult {index}")
        print("Source:", document.metadata.get("source"))
        print("Category:", document.metadata.get("category"))
        print("Content:")
        print(document.page_content)
        print("-" * 60)


if __name__ == "__main__":
    test_retriever()
