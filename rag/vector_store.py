from pathlib import Path
import time

from langchain_community.vectorstores import FAISS

from config import OPENROUTER_API_KEY
from rag.embeddings import get_embeddings


BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_STORE_DIR = BASE_DIR / "vector_store" / "faiss_index"


def create_vector_store(chunks):
    """
    Generate embeddings individually, create a FAISS index,
    and save it locally.
    """

    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is missing.")

    if not chunks:
        raise ValueError("No document chunks were supplied.")

    embeddings = get_embeddings()
    text_embeddings = []

    total_chunks = len(chunks)

    print(f"Creating FAISS index for {total_chunks} chunks...")

    MAX_RETRIES = 3

    for index, chunk in enumerate(chunks, start=1):
        print(f"\nEmbedding chunk {index}/{total_chunks}...")

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                vector = embeddings.embed_query(chunk.page_content)

                text_embeddings.append(
                    (chunk.page_content, vector)
                )

                print(f"Successfully embedded chunk {index}.")
                break

            except Exception as error:
                print(
                    f"Attempt {attempt}/{MAX_RETRIES} failed: {error}"
                )

                if attempt == MAX_RETRIES:
                    raise

                wait_time = 2 ** attempt

                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

    print("\nBuilding FAISS vector store...")

    vector_store = FAISS.from_embeddings(
        text_embeddings=text_embeddings,
        embedding=embeddings,
        metadatas=[chunk.metadata for chunk in chunks]
    )

    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

    vector_store.save_local(str(VECTOR_STORE_DIR))

    print("\nFAISS index saved successfully!")
    print(f"Location: {VECTOR_STORE_DIR}")

    return vector_store


def load_vector_store():
    """Load an existing FAISS index without generating embeddings."""

    index_file = VECTOR_STORE_DIR / "index.faiss"
    metadata_file = VECTOR_STORE_DIR / "index.pkl"

    if not index_file.exists() or not metadata_file.exists():
        raise FileNotFoundError(
            "FAISS index not found. Please run ingestion first."
        )

    embeddings = get_embeddings()

    vector_store = FAISS.load_local(
        str(VECTOR_STORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True
    )

    print("FAISS index loaded successfully.")

    return vector_store
