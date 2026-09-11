"""
antipattern_loop.py
--------------------
TEACHING FILE — DO NOT USE THIS IN PRODUCTION.

This file shows TWO common WRONG ways to stop an agentic loop. The exam
(Task Statement 1.1) specifically tests whether you can spot these broken
loop-termination patterns:

  1. Stopping on ANY text          -> run_agent_stop_on_text()
  2. Stopping on a magic PHRASE    -> run_agent_stop_on_phrase()

Both ignore the one reliable signal: stop_reason. Compare them with the
correct loop in agent.py.

WHY BOTH ARE WRONG
------------------
A model's wording changes from run to run, and the model can write text AND
request a tool in the SAME turn. So:
  - "Stop on any text" can quit before a requested tool ever runs.
  - "Stop on a phrase like 'done'" is even sneakier: it looks deliberate, but
    the model may never say your exact word, or may say it while still needing
    a tool. Either way the loop becomes unpredictable.
The reliable signal is ALWAYS stop_reason ("tool_use" vs "end_turn").

HOW TO USE
----------
Run:  python antipattern_loop.py
Pick which broken loop to run, then type a question. Type 'quit' to stop.

TIP: To make the bug show up, give the agent everything it needs to call a
tool right away, e.g.:
    "I am customer CUST-1001. Can I get a refund for order ORD-5001?"
With a question like that the model often writes a short lead-in sentence in
the same turn as its first tool call — and the broken loops quit on that text
before the work is finished.
"""

import os
import json
from dotenv import load_dotenv
import anthropic

from tools import TOOL_SCHEMAS, run_tool

# Load ANTHROPIC_API_KEY from the .env file (same as agent.py).
load_dotenv()

client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"

SYSTEM_PROMPT = (
    "You are a customer support assistant for PyStack Mart. Use the tools to "
    "answer questions about customers, orders, and refunds."
)

# Words the second broken loop watches for to decide (wrongly) that it's done.
DONE_PHRASES = ("done", "complete", "finished", "all set", "here is", "here's")


def _get_text(response) -> str:
    """Collect any text the model wrote in this response."""
    return "".join(b.text for b in response.content if b.type == "text")


def _run_requested_tools(response, messages):
    """Run any tools the model asked for and append the results."""
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            result = run_tool(block.name, block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": json.dumps(result),
            })
    if tool_results:
        messages.append({"role": "user", "content": tool_results})


# ==========================================================================
# BROKEN WAY #1 — stop as soon as there is ANY text.
# ==========================================================================
def run_agent_stop_on_text(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model=MODEL, max_tokens=1000,
            system=SYSTEM_PROMPT, tools=TOOL_SCHEMAS, messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        # ❌ ANTI-PATTERN: "there is some text, so we must be done."
        # If the model wrote a sentence AND also requested a tool, we quit
        # too early and never run the tool the model asked for.
        text = _get_text(response)
        if text.strip():
            print("[BROKEN #1] Saw some text, so I'm assuming we're done. Stopping.")
            return text

        # (Rarely reached, because the check above usually stops us first.)
        _run_requested_tools(response, messages)


# ==========================================================================
# BROKEN WAY #2 — loop until the model says a "magic" phrase.
# This is the "parsing natural-language signals to terminate" anti-pattern.
# ==========================================================================
def run_agent_stop_on_phrase(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model=MODEL, max_tokens=1000,
            system=SYSTEM_PROMPT, tools=TOOL_SCHEMAS, messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        text = _get_text(response).lower()

        # ❌ ANTI-PATTERN: decide we're finished by hunting for a phrase.
        # Problem 1: the model may say "here's..." while STILL needing a tool,
        #            so we stop before the real work is done.
        # Problem 2: the model may finish WITHOUT ever saying any of our words,
        #            so we loop forever (or until some other failure).
        if any(phrase in text for phrase in DONE_PHRASES):
            print("[BROKEN #2] Found a 'done' word in the text. Stopping.")
            return _get_text(response)

        # Otherwise keep going: run any requested tools, then loop again.
        _run_requested_tools(response, messages)


# ==========================================================================
# Interactive runner: pick a broken loop, then type prompts.
# ==========================================================================
if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not found.")
        print("Create a .env file in this folder with this line:")
        print('  ANTHROPIC_API_KEY=your-key-here')
        raise SystemExit(1)

    print("=" * 70)
    print("BROKEN loop demos — watch them stop too early (or loop oddly).")
    print("Both ignore stop_reason. Compare with the correct agent.py.")
    print("=" * 70)
    print("Choose which broken loop to run:")
    print("  1 = stop on ANY text")
    print("  2 = stop on a 'done' PHRASE")
    choice = input("Enter 1 or 2 > ").strip()

    broken_loop = run_agent_stop_on_phrase if choice == "2" else run_agent_stop_on_text
    label = "BROKEN #2 (phrase)" if choice == "2" else "BROKEN #1 (text)"

    print(f"\nRunning {label}.")
    print("Tip: try  'I am customer CUST-1001. Can I get a refund for ORD-5001?'")
    print("Type 'quit' or 'exit' to stop.")

    while True:
        user_message = input("\nYour question > ").strip()
        if user_message.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not user_message:
            continue
        answer = broken_loop(user_message)
        print(f"\n({label}) FINAL ANSWER:\n" + answer)
