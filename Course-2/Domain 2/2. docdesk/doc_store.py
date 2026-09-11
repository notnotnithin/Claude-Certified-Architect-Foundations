"""
doc_store.py
-------------
DocDesk's document backend. In Demo 2 we make it able to FAIL in realistic
ways, so our tools can return proper structured errors (Task 2.2):

  - a RESTRICTED document (raises a permission problem),
  - a SLOW/flaky document that sometimes "times out" (a transient problem),
  - normal documents that read fine.

Only text files (.md/.txt) are treated as documents, so a stray binary file
can never crash us (fix carried over from Demo 1).
"""

import os
import random

DOCS_DIR = os.path.join(os.path.dirname(__file__), "documents")
TEXT_EXTENSIONS = (".md", ".txt")

# A document that exists but the user is NOT allowed to read -> permission error.
RESTRICTED_DOCS = {"internal_pricing.md"}

# A document that is "flaky": reading it sometimes times out -> transient error.
FLAKY_DOCS = {"returns_policy.md"}


class PermissionDenied(Exception):
    """Raised when a document exists but access is not allowed."""


class TransientTimeout(Exception):
    """Raised when a read temporarily fails (e.g. a network/timeout blip)."""


def list_documents() -> list:
    """Return the readable TEXT document names in ./documents."""
    if not os.path.isdir(DOCS_DIR):
        return []
    names = sorted(
        f for f in os.listdir(DOCS_DIR)
        if os.path.isfile(os.path.join(DOCS_DIR, f))
        and f.lower().endswith(TEXT_EXTENSIONS)
    )
    # The restricted doc is listed (it exists) but cannot be read.
    return names


def read_document(name: str, _fail_transient: bool = None) -> str:
    """
    Return the full text of one document.

    Raises:
      FileNotFoundError   -> no such document (a validation problem)
      PermissionDenied    -> document is restricted (a permission problem)
      TransientTimeout    -> a temporary read failure (a transient problem)

    `_fail_transient` lets the demo force the flaky behaviour on/off:
      None  -> random (realistic), True -> always time out, False -> never.
    """
    if not name.lower().endswith(TEXT_EXTENSIONS):
        raise FileNotFoundError(name)

    if name in RESTRICTED_DOCS:
        raise PermissionDenied(name)

    # Simulate a flaky document: ~40% of reads time out unless forced.
    if name in FLAKY_DOCS:
        should_fail = _fail_transient
        if should_fail is None:
            should_fail = random.random() < 0.4
        if should_fail:
            raise TransientTimeout(name)

    path = os.path.join(DOCS_DIR, name)
    if not os.path.isfile(path):
        raise FileNotFoundError(name)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def search_documents(query: str) -> list:
    """
    Simple keyword search across readable documents. Returns a list of
    {name, snippet}. An EMPTY list means "searched fine, found nothing" —
    that is a VALID EMPTY RESULT, not an error (important for Task 2.2).
    """
    query_low = query.lower()
    hits = []
    for name in list_documents():
        try:
            text = read_document(name, _fail_transient=False)  # search never flakes
        except (PermissionDenied, FileNotFoundError):
            continue  # skip docs we can't read during a search
        if query_low in text.lower():
            idx = text.lower().find(query_low)
            start = max(0, idx - 40)
            end = min(len(text), idx + 80)
            hits.append({"name": name,
                         "snippet": text[start:end].replace("\n", " ").strip()})
    return hits
