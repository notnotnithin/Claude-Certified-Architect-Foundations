"""
agent.py
---------
THE MAIN DEMO 7 FILE: an agent whose conversations are PERSISTENT.

It is the same agentic loop you know (drive on stop_reason), but now the
message history is SAVED to disk after every turn, so you can stop and come
back to the SAME named conversation later.

You start it with a SESSION NAME, like:

    python agent.py asha-case        # resume (or create) the 'asha-case' session

Inside, besides normal questions, you can type special commands:

    /fork <new-name>   -> branch this session into an independent copy
                          (models fork_session): explore a different path.
    /fresh             -> start fresh in THIS session, seeded with only a short
                          summary instead of the old (maybe stale) history.
    /deliver ORD-5005  -> (demo helper) simulate the outside world changing:
                          marks that order Delivered, and INFORMS the session.
    /history           -> show how many messages are stored in this session.
    quit / exit        -> stop (the session stays saved on disk).

WHY THIS MATTERS (Task 1.7)
---------------------------
  - RESUME a named session when the earlier context is still valid.
  - FORK to try a different direction from a shared baseline, safely.
  - START FRESH WITH A SUMMARY when old tool results are STALE.
  - When resuming after something changed, TELL the agent what changed so it
    re-checks instead of trusting outdated results.
"""

import os
import sys
import json
from dotenv import load_dotenv
import anthropic

from tools import TOOL_SCHEMAS, run_tool
from mock_data import mark_order_delivered
import session as sess

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"
MAX_LOOPS = 10

SYSTEM_PROMPT = (
    "You are a customer support agent for PyStack Mart. You help with orders "
    "and refunds, using your tools to find real information. Today is "
    "2026-06-28. All amounts are in Rupees (Rs.). If you are told something "
    "changed since earlier, re-check the affected order instead of trusting "
    "older results."
)


def _one_turn(messages: list) -> str:
    """Run the agentic loop for the current messages; return final text."""
    for _ in range(MAX_LOOPS):
        response = client.messages.create(
            model=MODEL, max_tokens=1000,
            system=SYSTEM_PROMPT, tools=TOOL_SCHEMAS, messages=messages,
        )
        messages.append({"role": "assistant", "content": _serialize(response.content)})

        if response.stop_reason == "end_turn":
            return _extract_text(response)

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  -> {block.name}({block.input})")
                    result = run_tool(block.name, block.input)
                    print(f"     {result}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result),
                    })
            messages.append({"role": "user", "content": tool_results})
            continue

        return f"[stopped: unexpected stop_reason '{response.stop_reason}']"
    return "[stopped: reached the safety loop limit]"


def _serialize(content):
    """
    Convert the SDK response content blocks into plain dicts so the session
    can be saved as JSON and resumed later.
    """
    out = []
    for b in content:
        if b.type == "text":
            out.append({"type": "text", "text": b.text})
        elif b.type == "tool_use":
            out.append({"type": "tool_use", "id": b.id, "name": b.name,
                        "input": b.input})
    return out


def _extract_text(response) -> str:
    return "\n".join(b.text for b in response.content if b.type == "text").strip()


def main(session_name: str):
    # RESUME the named session (or start a new one if it doesn't exist yet).
    messages = sess.resume_session(session_name)

    print("=" * 70)
    print(f"PyStack Mart — Persistent Session: '{session_name}' (Demo 7)")
    print("Ask normal questions, or use commands:")
    print("  /fork <name>     branch this session into an independent copy")
    print("  /fresh           restart this session from a short summary only")
    print("  /deliver ORD-..  simulate that order being delivered (+inform)")
    print("  /history         show how many messages are stored")
    print("  quit / exit      stop (session stays saved)")
    print("=" * 70)

    while True:
        user_message = input(f"\n[{session_name}] > ").strip()
        low = user_message.lower()

        if low in ("quit", "exit", "q"):
            sess.save_session(session_name, messages)
            print("Goodbye! (session saved)")
            break
        if not user_message:
            continue

        # ---- special commands ----
        if low == "/history":
            print(f"[session] '{session_name}' has {len(messages)} messages.")
            continue

        if low.startswith("/fork"):
            parts = user_message.split()
            if len(parts) < 2:
                print("usage: /fork <new-name>")
                continue
            new_name = parts[1]
            sess.save_session(session_name, messages)          # save current first
            sess.fork_session(session_name, new_name)          # then copy it
            print(f"Forked into '{new_name}'. Re-run: python agent.py {new_name}")
            continue

        if low == "/fresh":
            summary = input("Enter a short summary to start fresh from: ").strip()
            messages = sess.start_fresh_with_summary(summary)
            sess.save_session(session_name, messages)
            continue

        if low.startswith("/deliver"):
            parts = user_message.split()
            if len(parts) < 2:
                print("usage: /deliver ORD-XXXX")
                continue
            oid = parts[1].upper()
            mark_order_delivered(oid, "2026-06-28")
            messages = sess.inform_of_change(
                messages, f"order {oid} has now been delivered (on 2026-06-28).")
            sess.save_session(session_name, messages)
            print(f"(Order {oid} marked Delivered and the session was informed.)")
            continue

        # ---- normal question ----
        messages.append({"role": "user", "content": user_message})
        answer = _one_turn(messages)
        print("\nANSWER:\n" + answer)
        sess.save_session(session_name, messages)   # persist after every turn


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not found.")
        print("Create a .env file in this folder with this line:")
        print('  ANTHROPIC_API_KEY=your-key-here')
        raise SystemExit(1)

    # The session name comes from the command line (models --resume <name>).
    # Default to 'default' if none is given.
    name = sys.argv[1] if len(sys.argv) > 1 else "default"
    main(name)
