from rag.embeddings import get_embeddings
from config import EMBEDDING_MODEL

print("Initializing embedding model...")

embeddings = get_embeddings()

test_text = (
    "Ready Bank offers a fictional Smart Savings Account "
    "with a minimum monthly average balance of Rs. 2000."
)

print("Generating embedding...")

vector = embeddings.embed_query(test_text)

print("\n--- Embedding Test Results ---")
print("Model: ", EMBEDDING_MODEL)
print("Vector dimensions:", len(vector))
print("First 5 values:", vector[:5])

print("\nEmbedding generated successfully!")
