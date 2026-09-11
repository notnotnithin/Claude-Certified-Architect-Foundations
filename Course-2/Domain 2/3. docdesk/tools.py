"""
tools.py
---------
Tools for DocDesk's research pipeline (Task 2.3), GROUPED BY ROLE so each agent
gets only the tools it needs.

ROLES AND THEIR TOOLS:
  - SEARCHER   : search_documents          (find which documents are relevant)
  - ANALYZER   : load_document             (read ONE document's content)
  - SYNTHESIZER: verify_fact               (scoped cross-role: quick fact-check)

TWO EXAM IDEAS SHOWN HERE:
  1. CONSTRAINED tool instead of generic: we use `load_document` (validates the
     name and only loads known documents) instead of a vague generic `fetch`.
  2. SCOPED CROSS-ROLE tool: the synthesizer gets a small `verify_fact` tool for
     the common "is this claim supported?" need, so it doesn't have to bounce
     every check back through the coordinator. Complex research still routes
     through the coordinator.
"""

from doc_store import list_documents, read_document, search_documents


# ==========================================================================
# SEARCHER tools
# ==========================================================================
SEARCH_TOOL_SCHEMAS = [
    {
        "name": "search_documents",
        "description": (
            "Find WHICH documents mention a keyword or phrase. Input: a short "
            "search string. Returns matching document names with a snippet each. "
            "An empty list means nothing matched (not an error)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
]


# ==========================================================================
# ANALYZER tools
# `load_document` is a CONSTRAINED alternative to a generic fetch: it only
# loads a known document by exact name and validates it.
# ==========================================================================
ANALYZE_TOOL_SCHEMAS = [
    {
        "name": "load_document",
        "description": (
            "Load the FULL text of ONE known document by its exact file name "
            "(e.g. 'returns_policy.md'). Validates that the document exists. "
            "Use this to read a document's content for analysis."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        },
    },
]


# ==========================================================================
# SYNTHESIZER tools — a SCOPED cross-role tool for a high-frequency need.
# `verify_fact` lets the synthesizer quickly check a simple claim without a
# full round-trip back to the coordinator + searcher + analyzer.
# ==========================================================================
VERIFY_TOOL_SCHEMAS = [
    {
        "name": "verify_fact",
        "description": (
            "Quickly check whether a short factual CLAIM is supported by the "
            "documents (a simple fact-check: dates, numbers, names, yes/no). "
            "Input: the claim text. Returns which document supports or "
            "contradicts it, if any. Use ONLY for simple checks — for deep "
            "research, defer to the coordinator."
        ),
        "input_schema": {
            "type": "object",
            "properties": {"claim": {"type": "string"}},
            "required": ["claim"],
        },
    },
]


# ==========================================================================
# IMPLEMENTATIONS
# ==========================================================================
def tool_search_documents(query: str) -> dict:
    return {"matches": search_documents(query), "count": len(search_documents(query))}


def tool_load_document(name: str) -> dict:
    text = read_document(name)
    if text is None:
        return {"error": f"No document named '{name}'. "
                         f"Available: {list_documents()}"}
    return {"name": name, "text": text}


def tool_verify_fact(claim: str) -> dict:
    """
    A lightweight fact-check: scan the documents for the key words in the claim
    and return any document whose text overlaps. (Simple on purpose — the point
    is that the synthesizer has a SCOPED tool, not a powerful search engine.)
    """
    words = [w for w in claim.lower().replace(",", " ").split() if len(w) > 4]
    supporting = []
    for name in list_documents():
        text = (read_document(name) or "").lower()
        if any(w in text for w in words):
            supporting.append(name)
    return {"claim": claim, "supporting_documents": supporting}


# Role -> (schemas, function map). The coordinator uses these to SCOPE agents.
SEARCH_FUNCTIONS = {"search_documents": tool_search_documents}
ANALYZE_FUNCTIONS = {"load_document": tool_load_document}
VERIFY_FUNCTIONS = {"verify_fact": tool_verify_fact}

# A combined map for convenience (used by the anti-pattern that dumps ALL tools
# onto one agent).
ALL_TOOL_SCHEMAS = SEARCH_TOOL_SCHEMAS + ANALYZE_TOOL_SCHEMAS + VERIFY_TOOL_SCHEMAS
ALL_FUNCTIONS = {**SEARCH_FUNCTIONS, **ANALYZE_FUNCTIONS, **VERIFY_FUNCTIONS}


def make_runner(function_map):
    """Return a run_tool function scoped to a specific set of tools."""
    def run_tool(tool_name: str, tool_input: dict) -> dict:
        func = function_map.get(tool_name)
        if func is None:
            return {"error": f"Tool '{tool_name}' is not available to this agent."}
        return func(**tool_input)
    return run_tool
