"""
antipattern_fixed_pipeline.py
-----------------------------
TEACHING FILE — shows the Task 1.6 trap: using a FIXED pipeline for a request
that actually needs ADAPTIVE planning.

THE TRAP
--------
This broken agent ALWAYS runs the same hard-coded steps, no matter what:

    STEP 1: get_refund_policy
    STEP 2: get_order("ORD-5001")     # assumes the issue is ORD-5001
    STEP 3: decide a refund for ORD-5001

It never LOOKS at the customer's full list of orders, so it cannot adapt. For a
vague request like "sort out my recent orders," this pipeline:
  - misses ORD-5005 (in transit), ORD-5006 (damaged), ORD-5002 (old), and
  - wastes effort assuming the problem is ORD-5001.

WHY IT'S WRONG
--------------
A fixed pipeline is fine when the steps are always the same. But an open-ended
request can contain anything, so the RIGHT next step depends on what you find.
Hard-coding the steps means you investigate the wrong things and miss the real
issues. The fix (in agent.py) is to LOOK first, then ADAPT the plan to what was
discovered.

Run this, then run agent.py with the SAME vague request to see the difference.
"""

import os
import json
from dotenv import load_dotenv

from tools import run_tool

load_dotenv()

# A rigid, predetermined sequence. Notice it never lists the customer's orders.
FIXED_STEPS = [
    ("get_refund_policy", {}),
    ("get_order", {"order_id": "ORD-5001"}),   # assumes the issue is here
]


def handle_with_fixed_pipeline(customer_message: str) -> str:
    print("\n[FIXED Pipeline] Running the SAME predetermined steps every time.")
    print("[FIXED Pipeline] (It never looks at the full list of orders.)")

    notes = []
    for tool, tool_input in FIXED_STEPS:
        print(f"  -> step: {tool}({tool_input})")
        result = run_tool(tool, tool_input)
        print(f"     result: {result}")
        notes.append(f"{tool}({tool_input}) -> {result}")

    # The pipeline only ever "knows" about ORD-5001 and the policy.
    return (
        "Based on my fixed steps, I only looked at the refund policy and order "
        "ORD-5001. I did not check your other orders (some may be in transit, "
        "old, or damaged) because my steps are hard-coded.\n\n"
        f"Notes:\n" + "\n".join(f"- {n}" for n in notes)
    )


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not found.")
        print("Create a .env file in this folder with this line:")
        print('  ANTHROPIC_API_KEY=your-key-here')
        raise SystemExit(1)

    print("=" * 70)
    print("BROKEN demo — FIXED pipeline (no adaptation).")
    print("Watch it run the same steps and miss most of the orders.")
    print("Type 'quit' or 'exit' to stop.")
    print("=" * 70)
    print("Use the same vague request as agent.py:")
    print("  I am CUST-1001. Something's off with my recent orders, sort it out.")

    while True:
        user_message = input("\nYour question > ").strip()
        if user_message.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not user_message:
            continue
        answer = handle_with_fixed_pipeline(user_message)
        print("\n(FIXED-PIPELINE) FINAL ANSWER:\n" + answer)
        print("\nNotice: it never adapted — it missed the other orders entirely.")
