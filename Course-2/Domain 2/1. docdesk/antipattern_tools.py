"""
antipattern_tools.py
--------------------
TEACHING FILE — the BAD tool design for DocDesk (Task Statement 2.1).

This is the "BEFORE" in our before/after story. It shows the mistakes the exam
tests you to spot:
  1. MINIMAL descriptions ("Analyzes a document.") — the model can't tell tools
     apart, so it misroutes.
  2. OVERLAPPING descriptions — analyze_content vs analyze_document are nearly
     identical, so the model picks almost at random.
  3. A single GENERIC tool (analyze_document) that tries to do everything —
     extract, summarize, and verify — so its behavior is unpredictable.

Run agent.py with --bad to load these tools and watch tool selection become
unreliable. Then compare with the good tools.py (the "AFTER").
"""

from doc_store import read_document, list_documents


# ❌ Minimal + overlapping descriptions. Notice how little they say, and how
# similar analyze_content and analyze_document sound.
TOOL_SCHEMAS = [
    {
        "name": "analyze_content",
        "description": "Analyzes content.",   # ❌ says nothing useful
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "request": {"type": "string"},
            },
            "required": ["name", "request"],
        },
    },
    {
        "name": "analyze_document",
        "description": "Analyzes a document.",  # ❌ near-identical to above
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "request": {"type": "string"},
            },
            "required": ["name", "request"],
        },
    },
    {
        "name": "get_document",
        "description": "Gets a document.",     # ❌ is this search? read? unclear
        "input_schema": {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        },
    },
]


def _doc_or_error(name: str) -> dict:
    text = read_document(name)
    if text is None:
        return {"error": f"No document named '{name}'. "
                         f"Available: {list_documents()}"}
    return {"name": name, "text": text}


# Both "analyze" tools do the SAME vague thing — return the doc text. Because
# the schemas don't differentiate them, the model can't choose reliably.
def tool_analyze_content(name: str, request: str) -> dict:
    result = _doc_or_error(name)
    if "error" not in result:
        result["request"] = request
    return result


def tool_analyze_document(name: str, request: str) -> dict:
    result = _doc_or_error(name)
    if "error" not in result:
        result["request"] = request
    return result


def tool_get_document(name: str) -> dict:
    return _doc_or_error(name)


TOOL_FUNCTIONS = {
    "analyze_content": tool_analyze_content,
    "analyze_document": tool_analyze_document,
    "get_document": tool_get_document,
}


def run_tool(tool_name: str, tool_input: dict) -> dict:
    func = TOOL_FUNCTIONS.get(tool_name)
    if func is None:
        return {"error": f"Unknown tool: {tool_name}"}
    return func(**tool_input)
