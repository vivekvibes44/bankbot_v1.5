
import numpy as np

from rag.embeddings import get_embeddings


def cosine_similarity(vector_a, vector_b):
    a = np.array(vector_a)
    b = np.array(vector_b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def main():
    print("\n========== EMBEDDING SIMILARITY TEST ==========\n")

    embeddings = get_embeddings()

    texts = [
        "What is the minimum balance for a savings account?",
        "How much money must I maintain in my savings account?",
        "What is the fee for replacing a debit card?",
        "How can I reset my mobile banking password?"
    ]

    vectors = embeddings.embed_documents(texts)

    pairs = [
        (0, 1, "Related savings questions"),
        (0, 2, "Savings vs debit card fee"),
        (0, 3, "Savings vs mobile banking")
    ]

    for first, second, description in pairs:
        score = cosine_similarity(
            vectors[first],
            vectors[second]
        )

        print(f"{description}: {score:.4f}")

    print("\nSUCCESS: Similarity test completed.")


if __name__ == "__main__":
    main()
