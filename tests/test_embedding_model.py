
import math

from rag.embeddings import get_embeddings


def main():
    print("\n========== EMBEDDING MODEL TEST ==========\n")

    embeddings = get_embeddings()

    # Test query embedding
    query = "What is the minimum balance required for a savings account?"
    query_vector = embeddings.embed_query(query)

    print("Query embedding:")
    print(f"Dimensions: {len(query_vector)}")
    print(f"Vector norm: {math.sqrt(sum(x * x for x in query_vector)):.6f}")

    # Test document embeddings
    documents = [
        "The minimum monthly average balance is ₹2,000.",
        "The debit card replacement fee is ₹200."
    ]

    document_vectors = embeddings.embed_documents(documents)

    print("\nDocument embeddings:")
    print(f"Number of documents: {len(document_vectors)}")

    for index, vector in enumerate(document_vectors):
        print(f"Document {index + 1} dimensions: {len(vector)}")

    # Validate dimensions
    assert len(query_vector) == 4096, "Unexpected query dimensions!"

    assert all(
        len(vector) == 4096 for vector in document_vectors
    ), "Unexpected document dimensions!"

    print("\nSUCCESS: All embeddings have 4096 dimensions.")


if __name__ == "__main__":
    main()
