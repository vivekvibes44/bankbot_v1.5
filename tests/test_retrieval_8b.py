from rag.vector_store import (
    load_vector_store,
    VECTOR_STORE_8B_DIR
)

from config import TEST_EMBEDDING_MODEL


def main():
    print("\n========== NEMOTRON 8B RETRIEVAL TEST ==========\n")

    vector_store = load_vector_store(
        vector_store_dir=VECTOR_STORE_8B_DIR,
        embedding_model=TEST_EMBEDDING_MODEL
    )

    test_questions = [
        "What is the minimum balance required for a savings account?",
        "What is the debit card replacement fee?",
        "How can I reset my mobile banking password?",
        "What documents are required for a personal loan?",
        "What happens if I forget my internet banking password?"
    ]

    for index, question in enumerate(test_questions, start=1):

        print(f"\nTest {index}: {question}")
        print("-" * 70)

        results = vector_store.similarity_search_with_score(
            question,
            k=3
        )

        for rank, (document, score) in enumerate(results, start=1):
            print(f"\nRank: {rank}")
            print(f"Source: {document.metadata.get('source')}")
            print(f"Category: {document.metadata.get('category')}")
            print(f"L2 Distance: {score:.4f}")
            print(f"Content: {document.page_content[:250]}...")


if __name__ == "__main__":
    main()
