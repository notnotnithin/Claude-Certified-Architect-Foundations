"""
tools.py
---------
The GOOD tool design for DocDesk Demo 2 (Task 2.2): tools return STRUCTURED
errors so the agent can decide what to do.

Each tool maps a real failure to the right category:
  - no such document name       -> validation error (isRetryable: false)
  - restricted document         -> permission error (isRetryable: false)
  - temporary read timeout      -> transient error (isRetryable: true)
  - a rule blocks the request   -> business error  (isRetryable: false)

It also shows LOCAL RECOVERY: read_document retries a transient timeout ONCE
inside the tool before giving up, so small blips don't even reach the agent.

And it shows the EMPTY-RESULT distinction: search returns an empty list as a
SUCCESS (isError: false), never as an error.
"""

from doc_store import (
    list_documents, read_document, search_documents,
    PermissionDenied, TransientTimeout,
)
from errors import (
    ok, transient_error, validation_error, business_error, permission_error,
)

# A tiny business rule for the demo: DocDesk only answers about PUBLIC docs.
# Asking to read the internal pricing doc is blocked by policy (business rule)
# BEFORE we even hit the permission layer — to show a business error cleanly.
BLOCKED_BY_POLICY = {"internal_costs.md"}


# ==========================================================================
# TOOL SCHEMAS  (same clear descriptions style as Demo 1)
# ==========================================================================
TOOL_SCHEMAS = [
    {
        "name": "search_documents",
        "description": (
            "Find WHICH documents mention a keyword or phrase. Input: a short "
            "search string. Returns a list of matching document names with a "
            "snippet each. An empty list means 'searched successfully, found "
            "nothing' — that is NOT an error."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    {
        "name": "read_document",
        "description": (
            "Return the FULL text of ONE document by its exact file name "
            "(e.g. 'returns_policy.md'). If the document is missing, restricted, "
            "or temporarily unavailable, this returns a STRUCTURED error telling "
            "you the category and whether it is worth retrying."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        },
    },
]


# ==========================================================================
# TOOL IMPLEMENTATIONS
# ==========================================================================
def tool_search_documents(query: str) -> dict:
    """Search never fails hard here; empty results are a SUCCESS, not an error."""
    matches = search_documents(query)
    # NOTE: even with zero matches, this is ok() (isError: false).
    return ok(matches=matches, count=len(matches))


def tool_read_document(name: str) -> dict:
    """
    Read one document, returning a STRUCTURED error on failure.

    Order of checks:
      1. business rule  (blocked by policy)      -> business_error
      2. try to read, with ONE local retry on a transient timeout
      3. map remaining failures to their category
    """
    # 1) BUSINESS rule: some docs are off-limits by policy (not an outage).
    if name in BLOCKED_BY_POLICY:
        return business_error(
            f"'{name}' is internal and cannot be shared with customers. "
            "Please ask about a public document instead."
        )

    # 2) LOCAL RECOVERY: try up to 2 times for a transient timeout.
    attempts = 2
    for attempt in range(1, attempts + 1):
        try:
            text = read_document(name)
            return ok(name=name, text=text)

        except TransientTimeout:
            print(f"     [tool] transient timeout on '{name}' "
                  f"(attempt {attempt}/{attempts})")
            if attempt < attempts:
                continue  # local recovery: try once more before reporting
            # Out of local retries -> report a transient error the AGENT can retry.
            return transient_error(
                f"Reading '{name}' timed out after {attempts} attempts. "
                "This is usually temporary — retrying may succeed."
            )

        except PermissionDenied:
            # 3a) PERMISSION: exists but not allowed. Retrying won't help.
            return permission_error(
                f"Access to '{name}' is restricted. DocDesk is not permitted "
                "to read this document."
            )

        except FileNotFoundError:
            # 3b) VALIDATION: bad input (no such doc). Fix the name, don't retry.
            return validation_error(
                f"No document named '{name}'. Available documents: "
                f"{list_documents()}."
            )

    # Should never reach here.
    return transient_error(f"Unknown problem reading '{name}'.")


TOOL_FUNCTIONS = {
    "search_documents": tool_search_documents,
    "read_document": tool_read_document,
}


def run_tool(tool_name: str, tool_input: dict) -> dict:
    func = TOOL_FUNCTIONS.get(tool_name)
    if func is None:
        return validation_error(f"Unknown tool: {tool_name}")
    return func(**tool_input)
