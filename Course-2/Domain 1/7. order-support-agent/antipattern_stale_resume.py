"""
antipattern_stale_resume.py
---------------------------
TEACHING FILE — shows the Task 1.7 mistake: RESUMING a session whose old tool
results are STALE, without telling the agent anything changed.

THE STORY
---------
1. Earlier, the agent looked up ORD-5005 and saw status 'In Transit'. That
   result is now saved in the session history.
2. Time passes. The order is actually DELIVERED now.
3. We RESUME the old session and ask "can I refund ORD-5005?" — BUT we do not
   inform the agent of the change, and we let it rely on the OLD result still
   sitting in the conversation.

WHAT GOES WRONG
---------------
The agent sees the stale 'In Transit' result in its history and may answer
"no, it's still in transit, you can't refund it" — which is now WRONG.

THE FIX (in agent.py)
---------------------
Either:
  - RESUME and INFORM the agent of the change (so it re-checks the order), or
  - START FRESH with a short summary instead of replaying stale results.
This file deliberately does NEITHER, to show the failure.

Run this, then in agent.py use /deliver + a re-check to see the correct way.
"""

import os
import json
from dotenv import load_dotenv
import anthropic

from tools import TOOL_SCHEMAS, run_tool
from mock_data import mark_order_delivered

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"

SYSTEM_PROMPT = (
    "You are a customer support agent for PyStack Mart. Use the conversation "
    "so far to answer. Today is 2026-06-28. Amounts are in Rupees (Rs.)."
)


def build_stale_session() -> list:
    """
    Recreate a session that already contains an OLD tool result saying
    ORD-5005 is 'In Transit'. (In a real app this would have been saved to
    disk earlier; here we build it directly to keep the demo self-contained.)
    """
    return [
        {"role": "user", "content": "What is the status of ORD-5005?"},
        {"role": "assistant", "content": [
            {"type": "tool_use", "id": "old_1", "name": "get_order",
             "input": {"order_id": "ORD-5005"}},
        ]},
        {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": "old_1",
             # NOTE: this is the STALE result captured earlier.
             "content": json.dumps({
                 "order_id": "ORD-5005", "item": "Webcam 1080p",
                 "amount_inr": 2200, "status": "In Transit",
                 "delivered_on": None})},
        ]},
        {"role": "assistant", "content": [
            {"type": "text",
             "text": "Your order ORD-5005 (Webcam 1080p) is currently In Transit."},
        ]},
    ]


def ask_without_informing(messages: list, question: str) -> str:
    """
    Ask a new question on the resumed session WITHOUT telling the agent that
    anything changed, and WITHOUT forcing a re-check. The agent is free to lean
    on the stale 'In Transit' result already in the history.
    """
    messages.append({"role": "user", "content": question})
    response = client.messages.create(
        model=MODEL, max_tokens=800,
        system=SYSTEM_PROMPT, tools=TOOL_SCHEMAS, messages=messages,
    )
    # We only read the text; we are NOT running any fresh tool calls here,
    # to highlight the agent relying on stale context.
    return "\n".join(b.text for b in response.content if b.type == "text").strip()


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not found.")
        print("Create a .env file in this folder with this line:")
        print('  ANTHROPIC_API_KEY=your-key-here')
        raise SystemExit(1)

    print("=" * 70)
    print("BROKEN demo — RESUMING with STALE results (no re-check, no notice).")
    print("Earlier the session saw ORD-5005 as 'In Transit'. It is now")
    print("Delivered — but we won't tell the agent. Watch it answer with the")
    print("old, wrong status.")
    print("=" * 70)

    # 1) Resume an old session that holds the stale 'In Transit' result.
    messages = build_stale_session()
    print("[resumed] old session restored (still says ORD-5005 = In Transit).")

    # 2) The world changes: the webcam is delivered now.
    mark_order_delivered("ORD-5005", "2026-06-28")
    print("[world]   ORD-5005 is actually DELIVERED now (2026-06-28).")

    # 3) Ask about a refund WITHOUT informing the agent of the change.
    print("\n[asking, without informing of the change]")
    answer = ask_without_informing(
        messages, "Can I refund ORD-5005 now?")
    print("\n(STALE-RESUME) FINAL ANSWER:\n" + answer)
    print("\nNotice: the agent likely leaned on the OLD 'In Transit' result and "
          "gave an out-of-date answer. The fix is to INFORM it of the change "
          "(or start fresh with a summary) — see agent.py.")
