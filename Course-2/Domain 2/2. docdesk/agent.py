"""
agent.py
---------
THE MAIN DEMO 2 FILE (Task 2.2): a DocDesk agent whose tools return STRUCTURED
errors, so the agent can make smart recovery decisions.

The agentic loop is the same as before (drive on stop_reason). What's new is
the ERROR CONTRACT: tools return {isError, errorCategory, isRetryable, message},
and the system prompt tells the agent how to react to each category.

Run two ways to SEE the difference:

    python agent.py          # GOOD tools (structured errors)
    python agent.py --bad    # BAD tools  (generic "Operation failed.")

Prompts to try are printed at the bottom.
"""

import os
import sys
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"
MAX_LOOPS = 12

# The system prompt teaches the agent how to USE the structured error metadata.
SYSTEM_PROMPT = (
    "You are DocDesk, a helpful assistant that answers questions from local "
    "documents using tools.\n\n"
    "Some tool results are errors. An error looks like: "
    '{"isError": true, "errorCategory": "...", "isRetryable": true/false, '
    '"message": "..."}. React based on the category:\n'
    "  - transient  : a temporary problem. If isRetryable is true, try the "
    "same call ONE more time before giving up.\n"
    "  - validation : the input was wrong (e.g. a bad document name). Do NOT "
    "retry the same call; correct the input (use the available names) or ask.\n"
    "  - business   : a rule blocks the request. Do NOT retry; explain the "
    "reason to the user politely using the message.\n"
    "  - permission : access is not allowed. Do NOT retry; tell the user you "
    "cannot access that document.\n\n"
    "A result with isError false is a SUCCESS. An empty search result "
    "(count 0) means 'found nothing' — that is NOT an error; just tell the user "
    "nothing matched. Base every answer only on what the documents say."
)


def run_agent(user_message: str, tools_module) -> str:
    TOOL_SCHEMAS = tools_module.TOOL_SCHEMAS
    run_tool = tools_module.run_tool

    messages = [{"role": "user", "content": user_message}]

    for _ in range(MAX_LOOPS):
        response = client.messages.create(
            model=MODEL, max_tokens=1000,
            system=SYSTEM_PROMPT, tools=TOOL_SCHEMAS, messages=messages,
        )
        print(f"\nstop_reason = {response.stop_reason!r}")
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            return _extract_text(response)

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  -> TOOL CALL: {block.name}({block.input})")
                    result = run_tool(block.name, block.input)
                    # Show the structured error clearly when present.
                    if isinstance(result, dict) and result.get("isError"):
                        print(f"     [ERROR] category={result.get('errorCategory')} "
                              f"retryable={result.get('isRetryable')} :: "
                              f"{result.get('message')}")
                    else:
                        preview = json.dumps(result)[:100]
                        print(f"     result: {preview}...")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    })

            # Carry-over fix from Demo 1: never send an empty user message.
            if not tool_results:
                text = _extract_text(response)
                return text or "[stopped: no tool results to return]"

            messages.append({"role": "user", "content": tool_results})
            continue

        return f"[stopped: unexpected stop_reason '{response.stop_reason}']"

    return "[stopped: reached the safety loop limit]"


def _extract_text(response) -> str:
    return "\n".join(b.text for b in response.content if b.type == "text").strip()


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not found.")
        print("Create a .env file in this folder with this line:")
        print('  ANTHROPIC_API_KEY=your-key-here')
        raise SystemExit(1)

    use_bad = "--bad" in sys.argv
    if use_bad:
        import antipattern_tools as tools_module
        banner = "BAD tools (generic 'Operation failed.')"
    else:
        import tools as tools_module
        banner = "GOOD tools (structured errors: category + retryable)"

    print("=" * 70)
    print("DocDesk — Structured Error Responses (Demo 2, Task 2.2)")
    print(f"Loaded: {banner}")
    print("Type your question and press Enter. Type 'quit' or 'exit' to stop.")
    print("=" * 70)
    print("Try these to trigger each error type:")
    print("  - Read the document 'nope.md'.                 (validation)")
    print("  - Read the document 'internal_pricing.md'.     (permission)")
    print("  - Read the returns policy in full.             (transient -> retry)")
    print("  - Search the documents for 'spaceship'.        (empty result, NOT an error)")

    while True:
        user_message = input("\nYour question > ").strip()
        if user_message.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not user_message:
            continue
        answer = run_agent(user_message, tools_module)
        print("\nANSWER:\n" + answer)
