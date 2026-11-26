
from rag.vector_store import (
    load_vector_store,
    VECTOR_STORE_DIR,
    VECTOR_STORE_8B_DIR
)

from config import (
    EMBEDDING_MODEL,
    TEST_EMBEDDING_MODEL
)


test_questions = [
    "What is the minimum balance required for a savings account?",
    "What is the debit card replacement fee?",
    "How can I reset my mobile banking password?",
    "What documents are required for a personal loan?",
    "What happens if I forget my internet banking password?"
]



import time


def check_dimensions(label, vector_store):

    print(f"\n========== {label} DIMENSION CHECK ==========")

    index_dimension = vector_store.index.d
    print(f"FAISS index dimension: {index_dimension}")

    query = test_questions[0]

    for attempt in range(1, 4):
        try:
            query_vector = (
                vector_store.embedding_function.embed_query(query)
            )

            query_dimension = len(query_vector)

            print(f"Query embedding dimension: {query_dimension}")

            if index_dimension != query_dimension:
                print("ERROR: Dimension mismatch!")
                return False

            print("SUCCESS: Dimensions match.")
            return True

        except Exception as error:
            print(f"Attempt {attempt}/3 failed: {error}")

            if attempt < 3:
                wait_time = 2 ** attempt
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

    print("ERROR: Could not verify dimensions after 3 attempts.")
    return False



def display_results(label, vector_store):

    print(f"\n\n========== {label} RETRIEVAL RESULTS ==========")

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


def main():

    print("\n========== MODEL RETRIEVAL COMPARISON ==========\n")

    # Load 1B model index
    print("Loading Nemotron 3.5 Embed 1B index...")

    vector_store_1b = load_vector_store(
        vector_store_dir=VECTOR_STORE_DIR,
        embedding_model=EMBEDDING_MODEL
    )

    # Load 8B model index
    print("\nLoading Nemotron 3.5 Embed 8B index...")

    vector_store_8b = load_vector_store(
        vector_store_dir=VECTOR_STORE_8B_DIR,
        embedding_model=TEST_EMBEDDING_MODEL
    )

    # Verify dimensions
    result_1b = check_dimensions(
        "NEMOTRON 3.5 EMBED 1B",
        vector_store_1b
    )

    result_8b = check_dimensions(
        "NEMOTRON 3.5 EMBED 8B",
        vector_store_8b
    )

    # Run retrieval only if both dimensions match
    if result_1b and result_8b:

        display_results(
            "NEMOTRON 3.5 EMBED 1B",
            vector_store_1b
        )

        display_results(
            "NEMOTRON 3.5 EMBED 8B",
            vector_store_8b
        )

    else:
        print("\nRetrieval comparison skipped due to dimension mismatch.")


if __name__ == "__main__":
    main()
