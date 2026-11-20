
from rag.document_loader import load_documents


documents = load_documents()

print("\n--- Document Loading Summary ---")

for index, document in enumerate(documents, start=1):
    print(f"\nDocument {index}")
    print("Metadata:", document.metadata)
    print("Characters:", len(document.page_content))
    print("Preview:")
    print(document.page_content[:300])
    print("-" * 60)
