from rag.vector_store import load_vector_store

print("Loading FAISS vector store...")

vector_store = load_vector_store()

query = "What is the minimum balance required for a savings account?"

print(f"\nQuery: {query}")

results = vector_store.similarity_search(query, k=3)

print("\n--- Retrieval Results ---")

for index, document in enumerate(results, start=1):
    print(f"\nResult {index}")
    print("Metadata:", document.metadata)
    print("Content:")
    print(document.page_content)
    print("-" * 60)
