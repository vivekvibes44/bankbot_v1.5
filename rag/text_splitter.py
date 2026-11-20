from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def split_documents(
    documents: list[Document],
    chunk_size: int = 800,
    chunk_overlap: int = 120
) -> list[Document]:
    """
    Split loaded documents into smaller chunks.

    Metadata from the original documents is preserved.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_documents(documents)

    print(f"Original documents: {len(documents)}")
    print(f"Generated chunks: {len(chunks)}")

    return chunks
