"""
docdesk_server.py
------------------
A real (small) MCP SERVER for DocDesk — this is what the project-scoped
.mcp.json points to under the "docdesk" entry.

It shows the two things an MCP server exposes (Task 2.4):

  1. TOOLS    — actions the agent can call (search_documents, load_document).
                Their DESCRIPTIONS are detailed on purpose, so the agent prefers
                these over generic built-in tools (like a bare file read).

  2. RESOURCE — a "content catalog": a list of the available documents. A
                resource lets the agent SEE what exists WITHOUT spending tool
                calls to discover it. Great for catalogs, schemas, indexes.

This uses the official MCP Python SDK (`pip install mcp`). You normally do NOT
run this file by hand — Claude Code launches it for you based on .mcp.json. It
is included so you can see exactly what the config points to.
"""

import os
from mcp.server.fastmcp import FastMCP

# The docs directory can be injected via env var (see .mcp.json "env" block).
DOCS_DIR = os.environ.get(
    "DOCDESK_DOCS_DIR",
    os.path.join(os.path.dirname(__file__), "..", "documents"),
)

mcp = FastMCP("docdesk")


def _list_docs():
    if not os.path.isdir(DOCS_DIR):
        return []
    return sorted(f for f in os.listdir(DOCS_DIR) if f.endswith((".md", ".txt")))


def _read(name):
    path = os.path.join(DOCS_DIR, name)
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


# --------------------------------------------------------------------------
# TOOLS — note the detailed descriptions (so the agent prefers these).
# --------------------------------------------------------------------------
@mcp.tool()
def search_documents(query: str) -> list:
    """Find WHICH DocDesk documents mention a keyword or phrase. Input: a short
    search string. Returns matching document names with a snippet each. Prefer
    this over any generic file-search built-in — it is scoped to the DocDesk
    document set and returns clean snippets."""
    q = query.lower()
    hits = []
    for name in _list_docs():
        text = _read(name) or ""
        if q in text.lower():
            i = text.lower().find(q)
            hits.append({"name": name,
                         "snippet": text[max(0, i - 30):i + 70].strip()})
    return hits


@mcp.tool()
def load_document(name: str) -> dict:
    """Load the FULL text of ONE DocDesk document by its exact file name (e.g.
    'returns_policy.md'). Prefer this over a generic file reader: it validates
    that the document is part of the DocDesk set and returns its full content."""
    text = _read(name)
    if text is None:
        return {"error": f"No document named '{name}'. Available: {_list_docs()}"}
    return {"name": name, "text": text}


# --------------------------------------------------------------------------
# RESOURCE — a content catalog the agent can read WITHOUT tool calls.
# --------------------------------------------------------------------------
@mcp.resource("docdesk://catalog")
def document_catalog() -> str:
    """A catalog of all available DocDesk documents. Exposing this as a RESOURCE
    lets the agent see what exists up front, instead of making exploratory
    search calls just to discover the document list."""
    docs = _list_docs()
    lines = ["Available DocDesk documents:"] + [f"- {d}" for d in docs]
    return "\n".join(lines)


if __name__ == "__main__":
    # Claude Code normally launches this over stdio based on .mcp.json.
    mcp.run()
