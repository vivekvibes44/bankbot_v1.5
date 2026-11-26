from config import TEST_EMBEDDING_MODEL
from rag.ingest import ingest_knowledge_base
from rag.vector_store import VECTOR_STORE_8B_DIR


def main():
    if not TEST_EMBEDDING_MODEL:
        raise ValueError("TEST_EMBEDDING_MODEL is missing from .env")

    print("\n========== NEMOTRON 8B INGESTION TEST ==========\n")

    vector_store = ingest_knowledge_base(
        vector_store_dir=VECTOR_STORE_8B_DIR,
        embedding_model=TEST_EMBEDDING_MODEL
    )

    print("\n========== INDEX VERIFICATION ==========")

    print(f"Index location: {VECTOR_STORE_8B_DIR}")
    print(f"Vector dimension: {vector_store.index.d}")

    assert vector_store.index.d == 4096, (
        "Expected a 4096-dimensional FAISS index."
    )

    print("\nSUCCESS: Separate 8B FAISS index created.")


if __name__ == "__main__":
    main()
