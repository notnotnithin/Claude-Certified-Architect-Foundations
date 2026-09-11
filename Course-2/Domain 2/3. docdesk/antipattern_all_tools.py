"""
antipattern_all_tools.py
------------------------
TEACHING FILE — the BAD tool distribution for DocDesk Demo 3 (Task 2.3).

This is the "BEFORE": instead of three SCOPED agents (one tool each), we give
ONE agent a HUGE pile of tools and no role. This recreates the exam's core
warning:

    "Giving an agent access to too many tools (e.g. 18 instead of 4-5)
     degrades tool selection reliability by increasing decision complexity."

WHAT'S IN THE PILE
------------------
  - The 3 REAL tools that actually work: search_documents, load_document,
    verify_fact.
  - ~15 DECOY tools that sound plausible but are NOT needed for a document Q&A
    task: translate_document, summarize_email, fetch_url, delete_document,
    export_pdf, send_slack_message, and so on.

The decoys are never the RIGHT choice for a documents question — but they crowd
the tool list, so the model has to sift through 18 options instead of 3. Watch
for symptoms of too-many-tools:
  - the agent reaching for an irrelevant tool (e.g. fetch_url, translate_document),
  - extra/rambling tool calls,
  - slower, less predictable tool selection.

THE FIX (coordinator.py): scope each agent to ONLY its role's tools, so every
agent chooses from 1-2 options, not 18.

Note: the decoy tools have simple stub implementations so nothing crashes if the
model calls one — but calling them is itself the mistake we want to expose.
"""

import os
import json
from dotenv import load_dotenv
import anthropic

from tools import (
    SEARCH_TOOL_SCHEMAS, ANALYZE_TOOL_SCHEMAS, VERIFY_TOOL_SCHEMAS,
    SEARCH_FUNCTIONS, ANALYZE_FUNCTIONS, VERIFY_FUNCTIONS,
    make_runner,
)

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"
MAX_LOOPS = 12


# ==========================================================================
# ~15 DECOY TOOLS — plausible-sounding, but irrelevant to document Q&A.
# Their only job is to CROWD the tool list so selection degrades.
# ==========================================================================
def _decoy(name, description, props=None):
    return {
        "name": name,
        "description": description,
        "input_schema": {
            "type": "object",
            "properties": props or {"input": {"type": "string"}},
            "required": list((props or {"input": {}}).keys()),
        },
    }


DECOY_TOOL_SCHEMAS = [
    _decoy("fetch_url", "Fetch the contents of a web URL.",
           {"url": {"type": "string"}}),
    _decoy("translate_document", "Translate a document into another language.",
           {"name": {"type": "string"}, "target_language": {"type": "string"}}),
    _decoy("summarize_email", "Summarize an email thread.",
           {"thread_id": {"type": "string"}}),
    _decoy("send_slack_message", "Send a message to a Slack channel.",
           {"channel": {"type": "string"}, "text": {"type": "string"}}),
    _decoy("export_pdf", "Export a document to PDF.",
           {"name": {"type": "string"}}),
    _decoy("delete_document", "Delete a document permanently.",
           {"name": {"type": "string"}}),
    _decoy("rename_document", "Rename a document.",
           {"name": {"type": "string"}, "new_name": {"type": "string"}}),
    _decoy("create_document", "Create a new blank document.",
           {"name": {"type": "string"}}),
    _decoy("upload_document", "Upload a document from a local path.",
           {"path": {"type": "string"}}),
    _decoy("get_weather", "Get the current weather for a city.",
           {"city": {"type": "string"}}),
    _decoy("calculate", "Evaluate a math expression.",
           {"expression": {"type": "string"}}),
    _decoy("schedule_meeting", "Schedule a calendar meeting.",
           {"title": {"type": "string"}, "time": {"type": "string"}}),
    _decoy("lookup_order", "Look up an e-commerce order by ID.",
           {"order_id": {"type": "string"}}),
    _decoy("process_refund", "Process a refund for an order.",
           {"order_id": {"type": "string"}, "amount": {"type": "number"}}),
    _decoy("web_search", "Search the public web for a query.",
           {"query": {"type": "string"}}),
]


def _decoy_runner(name):
    def fn(**kwargs):
        # A harmless stub — but the model calling this at all is the mistake.
        return {"note": f"(decoy tool '{name}' ran; it is not relevant to a "
                        f"document question)", "input": kwargs}
    return fn


DECOY_FUNCTIONS = {t["name"]: _decoy_runner(t["name"]) for t in DECOY_TOOL_SCHEMAS}


# ==========================================================================
# THE BLOATED TOOL LIST: 3 real tools + 15 decoys = 18 tools on ONE agent.
# ==========================================================================
BLOATED_TOOL_SCHEMAS = (
    SEARCH_TOOL_SCHEMAS + ANALYZE_TOOL_SCHEMAS + VERIFY_TOOL_SCHEMAS
    + DECOY_TOOL_SCHEMAS
)
BLOATED_FUNCTIONS = {
    **SEARCH_FUNCTIONS, **ANALYZE_FUNCTIONS, **VERIFY_FUNCTIONS,
    **DECOY_FUNCTIONS,
}

run_tool = make_runner(BLOATED_FUNCTIONS)

SYSTEM_PROMPT = (
    "You are DocDesk. Answer the user's question using your tools. "
    "You have many tools available; choose whichever you think are appropriate."
)


def run_agent(question: str) -> str:
    print(f"[setup] This agent has {len(BLOATED_TOOL_SCHEMAS)} tools available "
          f"(3 real + {len(DECOY_TOOL_SCHEMAS)} decoys).")
    messages = [{"role": "user", "content": question}]
    for _ in range(MAX_LOOPS):
        response = client.messages.create(
            model=MODEL, max_tokens=900,
            system=SYSTEM_PROMPT, tools=BLOATED_TOOL_SCHEMAS, messages=messages,
        )
        print(f"\nstop_reason = {response.stop_reason!r}")
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            return "\n".join(b.text for b in response.content
                             if b.type == "text").strip()

        if response.stop_reason == "tool_use":
            results = []
            for block in response.content:
                if block.type == "tool_use":
                    # Flag when the agent reaches for an irrelevant decoy tool.
                    is_decoy = block.name in DECOY_FUNCTIONS
                    tag = "  ❌ DECOY (irrelevant!)" if is_decoy else ""
                    print(f"  -> TOOL CHOSEN: {block.name}({block.input}){tag}")
                    result = run_tool(block.name, block.input)
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    })
            if not results:
                return "\n".join(b.text for b in response.content
                                 if b.type == "text").strip() or "[no result]"
            messages.append({"role": "user", "content": results})
            continue

        return f"[stopped: {response.stop_reason}]"
    return "[stopped: loop limit]"


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not found.")
        print("Create a .env file with: ANTHROPIC_API_KEY=your-key-here")
        raise SystemExit(1)

    print("=" * 70)
    print("BROKEN demo — ONE agent with 18 TOOLS (3 real + 15 decoys), no roles.")
    print("Watch selection get messy: the agent may reach for irrelevant tools.")
    print("Type 'quit' or 'exit' to stop.")
    print("=" * 70)
    print("Use the same question as the good demo, e.g.:")
    print("  - What is the refund window, and is it the same for warranty claims?")

    while True:
        q = input("\nYour question > ").strip()
        if q.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not q:
            continue
        answer = run_agent(q)
        print("\n(ALL-TOOLS) FINAL ANSWER:\n" + answer)
        print("\nNotice: 18 tools on one unscoped agent = harder, less reliable "
              "selection. Scoping (coordinator.py) keeps each agent at 1-2 tools.")
