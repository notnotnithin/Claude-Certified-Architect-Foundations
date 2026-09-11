"""
doc_store.py
-------------
A tiny "document backend" for DocDesk, our document Q&A assistant.

In a real app these documents might live in a database, an S3 bucket, or a
vector store. For this beginner demo we just read plain text/markdown files
from the ./documents folder, so you can focus on TOOL DESIGN, not storage.

This is the DocDesk equivalent of Domain 1's mock_data.py.
"""

import os

DOCS_DIR = os.path.join(os.path.dirname(__file__), "documents")

# Only treat these as readable documents. This prevents trying to read binary
# files (like PDFs or images) as text, which would crash with a decode error.
TEXT_EXTENSIONS = (".md", ".txt")


def list_documents() -> list:
    """Return the list of available TEXT document names in ./documents."""
    if not os.path.isdir(DOCS_DIR):
        return []
    return sorted(
        f for f in os.listdir(DOCS_DIR)
        if os.path.isfile(os.path.join(DOCS_DIR, f))
        and f.lower().endswith(TEXT_EXTENSIONS)
    )


def read_document(name: str) -> str | None:
    """Return the full text of one document, or None if it doesn't exist."""
    # Guard: only read supported text files.
    if not name.lower().endswith(TEXT_EXTENSIONS):
        return None
    path = os.path.join(DOCS_DIR, name)
    if not os.path.isfile(path):
        return None
    # errors="ignore" is a safety net so an odd character can never crash us.
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def search_documents(query: str) -> list:
    """
    Very simple keyword search across all text documents. Returns a list of
    {name, snippet} for documents whose text contains the query (case-
    insensitive). This is intentionally basic — real systems use embeddings.
    """
    query_low = query.lower()
    hits = []
    for name in list_documents():
        text = read_document(name) or ""
        if query_low in text.lower():
            idx = text.lower().find(query_low)
            start = max(0, idx - 40)
            end = min(len(text), idx + 80)
            snippet = text[start:end].replace("\n", " ").strip()
            hits.append({"name": name, "snippet": snippet})
    return hits
