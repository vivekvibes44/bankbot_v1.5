from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document

BASE_DIR = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


def load_pdf(file_path: Path) -> str:
    """Extract text from a PDF file."""

    reader = PdfReader(file_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append(
                f"Page {page_number}:\n{text}"
            )

    return "\n\n".join(pages)


def load_text_file(file_path: Path) -> str:
    """Read a TXT or Markdown file."""

    return file_path.read_text(encoding="utf-8")


def load_documents() -> list[Document]:
    """Load supported knowledge-base files as LangChain Documents."""

    documents = []

    for file_path in KNOWLEDGE_DIR.rglob("*"):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            if file_path.suffix.lower() == ".pdf":
                content = load_pdf(file_path)
            else:
                content = load_text_file(file_path)

            if not content.strip():
                print(f"Skipped empty document: {file_path.name}")
                continue

            category = file_path.parent.name

            document = Document(
                page_content=content,
                metadata={
                    "source": file_path.name,
                    "category": category,
                    "file_type": file_path.suffix.lower()
                }
            )

            documents.append(document)

            print(f"Loaded: {file_path.name}")

        except Exception as error:
            print(f"Failed to load {file_path.name}: {error}")

    print(f"\nTotal documents loaded: {len(documents)}")

    return documents
