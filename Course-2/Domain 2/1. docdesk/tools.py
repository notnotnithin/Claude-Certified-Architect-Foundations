"""
tools.py
---------
The GOOD tool design for DocDesk (Task Statement 2.1).

KEY EXAM IDEA: Tool descriptions are the PRIMARY thing the model reads to
decide which tool to call. So each description below clearly states:
  - what the tool does,
  - the input format it expects,
  - an example query,
  - and WHEN to use it vs a similar tool (the boundary).

THE SPLIT (the exam's own example):
A single generic "analyze_document" tool is vague — the model can't tell what
it will do. We SPLIT it into three purpose-specific tools with clear contracts:

    analyze_document  ->  extract_data_points
                          summarize_content
                          verify_claim_against_source

We also keep the search/read tools clearly separated so the model never
confuses "find which document" with "read a document" with "analyze it".
"""

from doc_store import list_documents, read_document, search_documents


# ==========================================================================
# TOOL SCHEMAS — note how detailed and DIFFERENTIATED each description is.
# ==========================================================================
TOOL_SCHEMAS = [
    {
        "name": "search_documents",
        "description": (
            "Find WHICH documents mention a keyword or phrase. Input: a short "
            "search string (e.g. 'refund window' or 'warranty'). Returns a list "
            "of matching document names with a short snippet each. "
            "Use this FIRST when you don't yet know which document holds the "
            "answer. Do NOT use this to read a full document (use read_document) "
            "or to pull out specific facts (use extract_data_points)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Keyword or phrase to search for, e.g. 'refund'.",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "read_document",
        "description": (
            "Return the FULL text of ONE document, given its exact file name "
            "(e.g. 'returns_policy.md'). Use this when you already know which "
            "document you need and want to read all of it. Do NOT use this to "
            "search across documents (use search_documents) or to extract just "
            "a few specific values (use extract_data_points)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Exact document file name, e.g. 'product_faq.md'.",
                }
            },
            "required": ["name"],
        },
    },
    {
        "name": "extract_data_points",
        "description": (
            "Pull out SPECIFIC factual values from ONE document — things like "
            "prices, dates, numbers, time windows, or named terms. Input: the "
            "document name and a list of the data points you want (e.g. "
            "['refund window in days', 'warranty length']). Returns the document "
            "text so you can read those exact values. Use this when the user "
            "wants precise facts, NOT a general summary (use summarize_content) "
            "and NOT a true/false claim check (use verify_claim_against_source)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string",
                          "description": "Document file name to read from."},
                "data_points": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "The specific facts to look for.",
                },
            },
            "required": ["name", "data_points"],
        },
    },
    {
        "name": "summarize_content",
        "description": (
            "Produce a SHORT plain-language summary of ONE document's overall "
            "content. Input: the document name. Returns the document text so you "
            "can summarize it. Use this when the user wants the gist or an "
            "overview — NOT specific values (use extract_data_points) and NOT a "
            "yes/no verification of a claim (use verify_claim_against_source)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string",
                          "description": "Document file name to summarize."},
            },
            "required": ["name"],
        },
    },
    {
        "name": "verify_claim_against_source",
        "description": (
            "Check whether a specific CLAIM is supported by ONE document. Input: "
            "the document name and the claim to check (e.g. 'Refunds are allowed "
            "for In Transit orders'). Returns the document text so you can judge "
            "whether the claim is true, false, or not stated. Use this ONLY for "
            "true/false fact-checking against a source — NOT for summaries and "
            "NOT for pulling lists of values."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string",
                          "description": "Document file name to check against."},
                "claim": {"type": "string",
                          "description": "The claim to verify."},
            },
            "required": ["name", "claim"],
        },
    },
]


# ==========================================================================
# TOOL IMPLEMENTATIONS
# For this demo, the "analyze" tools return the document text plus a hint;
# the model then does the extraction/summary/verification in its reply. The
# POINT of the demo is the DESCRIPTIONS and tool selection, not the analysis.
# ==========================================================================
def _doc_or_error(name: str) -> dict:
    text = read_document(name)
    if text is None:
        return {"error": f"No document named '{name}'. "
                         f"Available: {list_documents()}"}
    return {"name": name, "text": text}


def tool_search_documents(query: str) -> dict:
    return {"matches": search_documents(query)}


def tool_read_document(name: str) -> dict:
    return _doc_or_error(name)


def tool_extract_data_points(name: str, data_points: list) -> dict:
    result = _doc_or_error(name)
    if "error" not in result:
        result["requested_data_points"] = data_points
    return result


def tool_summarize_content(name: str) -> dict:
    result = _doc_or_error(name)
    if "error" not in result:
        result["task"] = "summarize"
    return result


def tool_verify_claim_against_source(name: str, claim: str) -> dict:
    result = _doc_or_error(name)
    if "error" not in result:
        result["claim_to_verify"] = claim
    return result


TOOL_FUNCTIONS = {
    "search_documents": tool_search_documents,
    "read_document": tool_read_document,
    "extract_data_points": tool_extract_data_points,
    "summarize_content": tool_summarize_content,
    "verify_claim_against_source": tool_verify_claim_against_source,
}


def run_tool(tool_name: str, tool_input: dict) -> dict:
    func = TOOL_FUNCTIONS.get(tool_name)
    if func is None:
        return {"error": f"Unknown tool: {tool_name}"}
    return func(**tool_input)
