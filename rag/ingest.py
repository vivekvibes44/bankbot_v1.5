from rag.document_loader import load_documents
from rag.text_splitter import split_documents
from rag.vector_store import create_vector_store


def ingest_knowledge_base(
    vector_store_dir=None,
    embedding_model=None
):
    """Load, split, embed and index the knowledge base."""

    print("\n========== READY BANK RAG INGESTION ==========\n")

    # 1. Load documents
    print("Step 1: Loading documents...")
    documents = load_documents()

    if not documents:
        raise ValueError("No documents were loaded.")

    # 2. Split documents
    print("\nStep 2: Splitting documents...")
    chunks = split_documents(documents)

    if not chunks:
        raise ValueError("No chunks were generated.")

    # 3. Generate embeddings and create FAISS index
    print("\nStep 3: Creating vector store...")

    if vector_store_dir is None:
        vector_store = create_vector_store(chunks)
    else:
        vector_store = create_vector_store(
            chunks,
            vector_store_dir=vector_store_dir,
            embedding_model=embedding_model
        )

    print("\n========== INGESTION COMPLETED ==========")

    return vector_store


if __name__ == "__main__":
    ingest_knowledge_base()
