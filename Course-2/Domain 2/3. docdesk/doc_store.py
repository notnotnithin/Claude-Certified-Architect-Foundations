"""
doc_store.py
-------------
DocDesk's document backend. Reads plain text/markdown files from ./documents.
Only text files (.md/.txt) are treated as documents, so a stray binary file
can never crash us.
"""

import os

DOCS_DIR = os.path.join(os.path.dirname(__file__), "documents")
TEXT_EXTENSIONS = (".md", ".txt")


def list_documents() -> list:
    if not os.path.isdir(DOCS_DIR):
        return []
    return sorted(
        f for f in os.listdir(DOCS_DIR)
        if os.path.isfile(os.path.join(DOCS_DIR, f))
        and f.lower().endswith(TEXT_EXTENSIONS)
    )


def read_document(name: str) -> str | None:
    if not name.lower().endswith(TEXT_EXTENSIONS):
        return None
    path = os.path.join(DOCS_DIR, name)
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def search_documents(query: str) -> list:
    query_low = query.lower()
    hits = []
    for name in list_documents():
        text = read_document(name) or ""
        if query_low in text.lower():
            idx = text.lower().find(query_low)
            start = max(0, idx - 40)
            end = min(len(text), idx + 80)
            hits.append({"name": name,
                         "snippet": text[start:end].replace("\n", " ").strip()})
    return hits
