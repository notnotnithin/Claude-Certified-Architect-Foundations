"""
coordinator.py
---------------
THE MAIN DEMO 3 FILE (Task 2.3): a small RESEARCH PIPELINE where each agent is
SCOPED to only the tools its role needs, and tool_choice is used deliberately.

PIPELINE:
  Searcher    -> finds which documents are relevant   (tools: search_documents)
  Analyzer    -> reads those documents                (tools: load_document)
  Synthesizer -> writes the answer, with a scoped      (tools: verify_fact)
                 verify_fact tool for quick checks

WHY SCOPING (Task 2.3):
  - Each agent has 1 tool, not all 3. Fewer, role-relevant tools = more reliable
    selection. (Giving one agent 18 tools would hurt its choices.)
  - An agent can't misuse tools outside its role, because it doesn't have them.

TOOL_CHOICE shown here:
  - Searcher uses FORCED tool_choice {"type":"tool","name":"search_documents"}
    to guarantee it searches FIRST before anything else.
  - Analyzer uses "any" to guarantee it actually loads a document (no chit-chat).
  - Synthesizer uses "auto" so it can verify IF needed, then write the answer.
"""

import os
from dotenv import load_dotenv

from tools import (
    SEARCH_TOOL_SCHEMAS, ANALYZE_TOOL_SCHEMAS, VERIFY_TOOL_SCHEMAS,
    SEARCH_FUNCTIONS, ANALYZE_FUNCTIONS, VERIFY_FUNCTIONS,
    make_runner,
)
from subagent import AgentDefinition, SubAgent

load_dotenv()


# ==========================================================================
# THREE SCOPED AGENTS — each gets ONLY its role's tools.
# ==========================================================================
SEARCHER = AgentDefinition(
    name="Searcher",
    system_prompt=(
        "You are the Searcher. Use search_documents to find which documents are "
        "relevant to the question. Report the document names you found."
    ),
    tool_schemas=SEARCH_TOOL_SCHEMAS,
    run_tool=make_runner(SEARCH_FUNCTIONS),
)

ANALYZER = AgentDefinition(
    name="Analyzer",
    system_prompt=(
        "You are the Analyzer. Use load_document to read the document(s) you are "
        "told to read, and report the key facts relevant to the question."
    ),
    tool_schemas=ANALYZE_TOOL_SCHEMAS,
    run_tool=make_runner(ANALYZE_FUNCTIONS),
)

SYNTHESIZER = AgentDefinition(
    name="Synthesizer",
    system_prompt=(
        "You are the Synthesizer. Write the final answer for the user from the "
        "facts you are given. If you need to quickly confirm a simple claim, use "
        "your verify_fact tool. Do not ask for more research — answer from what "
        "you have."
    ),
    tool_schemas=VERIFY_TOOL_SCHEMAS,
    run_tool=make_runner(VERIFY_FUNCTIONS),
)


def handle(question: str) -> str:
    # STEP 1: Searcher — FORCED to call search_documents first.
    print("\n[Coordinator] Step 1: Searcher (forced tool_choice = search_documents)")
    search_out = SubAgent(SEARCHER).run(
        f"Question: {question}\nFind the relevant documents.",
        tool_choice={"type": "tool", "name": "search_documents"},
    )
    print(f"[Coordinator] Searcher said: {search_out}")

    # STEP 2: Analyzer — 'any' guarantees it actually loads a document.
    print("\n[Coordinator] Step 2: Analyzer (tool_choice = any)")
    analyze_out = SubAgent(ANALYZER).run(
        f"Question: {question}\n"
        f"The Searcher found these relevant documents:\n{search_out}\n"
        "Load the most relevant document(s) and report the key facts.",
        tool_choice="any",
    )
    print(f"[Coordinator] Analyzer said: {analyze_out}")

    # STEP 3: Synthesizer — 'auto': may verify a fact, then writes the answer.
    print("\n[Coordinator] Step 3: Synthesizer (tool_choice = auto, has scoped verify_fact)")
    final = SubAgent(SYNTHESIZER).run(
        f"Question: {question}\n\n"
        f"Facts gathered by the Analyzer:\n{analyze_out}\n\n"
        "Write the final answer for the user.",
        tool_choice="auto",
    )
    return final


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not found.")
        print("Create a .env file in this folder with this line:")
        print('  ANTHROPIC_API_KEY=your-key-here')
        raise SystemExit(1)

    print("=" * 70)
    print("DocDesk — Scoped Tools & tool_choice (Demo 3, Task 2.3)")
    print("A research pipeline: Searcher -> Analyzer -> Synthesizer,")
    print("each SCOPED to only its role's tools.")
    print("Type your question and press Enter. Type 'quit' or 'exit' to stop.")
    print("=" * 70)
    print("Try things like:")
    print("  - What is the refund window, and is it the same for warranty claims?")
    print("  - How long is the warranty on accessories?")

    while True:
        q = input("\nYour question > ").strip()
        if q.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not q:
            continue
        answer = handle(q)
        print("\nFINAL ANSWER:\n" + answer)
