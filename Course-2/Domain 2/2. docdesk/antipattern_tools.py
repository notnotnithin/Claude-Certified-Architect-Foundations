"""
antipattern_tools.py
--------------------
TEACHING FILE — the BAD error design for DocDesk Demo 2 (Task 2.2).

This is the "BEFORE". Every failure returns the SAME flat, generic message:

    {"error": "Operation failed."}

WHY IT'S BAD
------------
The agent cannot tell WHAT went wrong or WHAT to do next:
  - Was it a temporary blip it should retry? (transient)
  - Was the document name wrong? (validation — fix the input)
  - Was it blocked by a rule? (business — explain, don't retry)
  - Was it restricted? (permission — stop, don't retry)

With one uniform message, the agent guesses. It often retries things that will
NEVER succeed (wasting calls) or gives up on things that WOULD succeed on retry.

It ALSO gets the empty-result case wrong: a search with no matches is reported
as an error here, even though "found nothing" is a perfectly valid success.

Run agent.py --bad and watch the agent flail on the same failures that the good
tools handle cleanly.
"""

from doc_store import (
    read_document, search_documents,
    PermissionDenied, TransientTimeout,
)


TOOL_SCHEMAS = [
    {
        "name": "search_documents",
        "description": "Search the documents for a query.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    {
        "name": "read_document",
        "description": "Read a document by name.",
        "input_schema": {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        },
    },
]


def tool_search_documents(query: str) -> dict:
    matches = search_documents(query)
    # ❌ Treats "no matches" as a failure — but it's a valid empty result!
    if not matches:
        return {"error": "Operation failed."}
    return {"matches": matches}


def tool_read_document(name: str) -> dict:
    # ❌ Every possible failure collapses into the SAME generic message.
    try:
        text = read_document(name)
        return {"name": name, "text": text}
    except (TransientTimeout, PermissionDenied, FileNotFoundError):
        return {"error": "Operation failed."}   # no category, no retry hint
    except Exception:
        return {"error": "Operation failed."}


TOOL_FUNCTIONS = {
    "search_documents": tool_search_documents,
    "read_document": tool_read_document,
}


def run_tool(tool_name: str, tool_input: dict) -> dict:
    func = TOOL_FUNCTIONS.get(tool_name)
    if func is None:
        return {"error": "Operation failed."}
    return func(**tool_input)
