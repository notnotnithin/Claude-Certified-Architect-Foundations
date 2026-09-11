"""
agent.py
---------
THE MAIN DEMO 1 FILE (Task 2.1): a DocDesk agent that answers questions about
local documents. The point of THIS demo is TOOL SELECTION — which tool the
model chooses, and why good descriptions make that reliable.

It reuses the same agentic loop you learned in Domain 1 (drive on stop_reason).
The new focus is the TOOLS, not the loop.

Run it two ways to SEE the difference:

    python agent.py          # GOOD tools (clear, differentiated descriptions)
    python agent.py --bad    # BAD tools  (vague, overlapping descriptions)

Ask the same question in both and watch which tool the model picks. With the
good tools it routes correctly; with the bad tools it misroutes or guesses.
"""

import os
import sys
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"
MAX_LOOPS = 10

# Neutral system prompt: we let the TOOL DESCRIPTIONS drive selection.
SYSTEM_PROMPT = (
    "You are DocDesk, a helpful assistant that answers questions using a small "
    "set of local documents. Use the provided tools to find and read the right "
    "document before answering. Be clear and concise, and base your answer only "
    "on what the documents say."
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
                    # THIS LINE is the point of the demo: which tool was chosen.
                    print(f"  -> TOOL CHOSEN: {block.name}({block.input})")
                    result = run_tool(block.name, block.input)
                    preview = json.dumps(result)[:120]
                    print(f"     result (preview): {preview}...")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    })

            # Safety: only send a follow-up message if we actually have tool
            # results. Sending an empty user message makes the API reject the
            # request ("user messages must have non-empty content").
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

    # Choose which tool set to load.
    use_bad = "--bad" in sys.argv
    if use_bad:
        import antipattern_tools as tools_module
        banner = "BAD tools (vague, overlapping descriptions)"
    else:
        import tools as tools_module
        banner = "GOOD tools (clear, differentiated descriptions)"

    print("=" * 70)
    print(f"DocDesk — Document Q&A (Demo 1, Task 2.1)")
    print(f"Loaded: {banner}")
    print("Type your question and press Enter. Type 'quit' or 'exit' to stop.")
    print("=" * 70)
    print("Try the SAME question with and without --bad, e.g.:")
    print("  - What is the refund window? Pull the exact number of days.")
    print("  - Give me a short summary of the returns policy.")
    print("  - Is it true that In Transit orders can be refunded?")

    while True:
        user_message = input("\nYour question > ").strip()
        if user_message.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not user_message:
            continue
        answer = run_agent(user_message, tools_module)
        print("\nANSWER:\n" + answer)
