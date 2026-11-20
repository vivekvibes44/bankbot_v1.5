from rag.document_loader import load_documents
from rag.text_splitter import split_documents


documents = load_documents()

chunks = split_documents(documents)

print("\n--- Chunking Summary ---")

for index, chunk in enumerate(chunks, start=1):
    print(f"\nChunk {index}")
    print("Metadata:", chunk.metadata)
    print("Characters:", len(chunk.page_content))
    print("Preview:", chunk.page_content[:200])
    print("-" * 60)
