"""
agent.py
---------
THE MAIN DEMO 5 FILE: a support agent whose tool calls are governed by HOOKS.

This is the Demo 1.1 agentic loop (drive on stop_reason) with hooks wired in:

  - BEFORE running each tool, we call pre_tool_hook(). If it returns a result,
    that tool call is BLOCKED and the hook's result is sent back instead.
  - AFTER a tool runs, we call post_tool_hook() to normalize the result before
    the model sees it.

It enforces, deterministically:
  1. PREREQUISITE GATE  — process_refund is blocked until identity is verified.
  2. THRESHOLD BLOCK    — refunds above Rs. 500 are blocked and must escalate.
  3. NORMALIZATION      — legacy order formats are cleaned up automatically.

It also shows a STRUCTURED HANDOFF: when escalating, the agent passes a tidy
summary (customer, order, amount, reason, recommended action) to a human.
"""

import os
import json
from dotenv import load_dotenv
import anthropic

from tools import TOOL_SCHEMAS, run_tool
from hooks import pre_tool_hook, post_tool_hook

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"
MAX_LOOPS = 12

SYSTEM_PROMPT = (
    "You are a customer support agent for PyStack Mart. You can look up "
    "customers and orders, read the refund policy, verify identity, process "
    "refunds, and escalate to a human.\n\n"
    "Follow this process for refunds:\n"
    "1. Look up the order and verify the customer's identity (verify_identity).\n"
    "2. Check the refund policy and the order status.\n"
    "3. If a refund is allowed and within limits, process it.\n"
    "4. If a tool result says an action was BLOCKED, do not try to force it — "
    "follow the reason given (e.g. verify first, or escalate to a human).\n"
    "5. When escalating, write a clear structured summary: customer ID, order "
    "ID, amount, the root cause, and your recommended action.\n"
    "All amounts are in Indian Rupees (Rs.)."
)


def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]
    # `state` persists across the loop so hooks can remember things,
    # e.g. whether identity has been verified in this conversation.
    state = {"verified": False}

    for _ in range(MAX_LOOPS):
        response = client.messages.create(
            model=MODEL, max_tokens=1200,
            system=SYSTEM_PROMPT, tools=TOOL_SCHEMAS, messages=messages,
        )
        print(f"\nstop_reason = {response.stop_reason!r}")
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            return _extract_text(response)

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                print(f"  -> wants: {block.name}({block.input})")

                # ---- PRE-TOOL HOOK: maybe block the call ----
                blocked = pre_tool_hook(block.name, block.input, state)
                if blocked is not None:
                    result = blocked
                else:
                    # Run the real tool, then POST-TOOL normalize the result.
                    result = run_tool(block.name, block.input)
                    result = post_tool_hook(block.name, result)

                    # Record identity verification in state for later calls.
                    if block.name == "verify_identity" and result.get("verified"):
                        state["verified"] = True
                        print("      [state] identity verified = True")

                print(f"     result: {result}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                })
            messages.append({"role": "user", "content": tool_results})
            continue

        return f"[Stopped: unexpected stop_reason '{response.stop_reason}'.]"

    return "[Stopped: reached the safety loop limit.]"


def _extract_text(response) -> str:
    return "\n".join(b.text for b in response.content if b.type == "text").strip()


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not found.")
        print("Create a .env file in this folder with this line:")
        print('  ANTHROPIC_API_KEY=your-key-here')
        raise SystemExit(1)

    print("=" * 70)
    print("PyStack Mart — Compliant Support Agent (Demo 5)")
    print("Tool calls are governed by HOOKS: prerequisite gate, threshold")
    print("block, and data normalization.")
    print("Type your question and press Enter. Type 'quit' or 'exit' to stop.")
    print("=" * 70)
    print("Try things like:")
    print("  - I am CUST-1001. Please refund order ORD-5002.   (small -> allowed)")
    print("  - I am CUST-1001. Please refund order ORD-5001.   (big -> escalates)")
    print("  - What is the status of order ORD-5004?           (legacy -> normalized)")

    while True:
        user_message = input("\nYour question > ").strip()
        if user_message.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not user_message:
            continue
        answer = run_agent(user_message)
        print("\nFINAL ANSWER:\n" + answer)
