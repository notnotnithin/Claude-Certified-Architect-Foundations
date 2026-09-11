"""
antipattern_narrow.py
----------------------
TEACHING FILE — shows the #1 multi-agent mistake the exam tests for
(Task Statement 1.2): TOO-NARROW TASK DECOMPOSITION.

THE TRAP (from the exam's "creative industries" sample question)
----------------------------------------------------------------
A coordinator is asked a BROAD question, but it breaks the work into subtasks
that only cover PART of the topic. Every subagent then succeeds at its narrow
job — yet the final answer is incomplete, because whole areas were never
assigned to anyone.

HERE we make a customer ask a multi-part question:
    "I am CUST-1001. Is ORD-5001 delivered, can I refund it,
     and what is your shipping policy?"

That has THREE parts: (1) order status, (2) refund eligibility, (3) shipping
policy. The BROKEN coordinator below decomposes it too narrowly — it only
looks at the order status and forgets the refund and shipping parts.

WHY IT'S WRONG
--------------
The subagent does its job perfectly. The failure is in the COORDINATOR's
decomposition: it didn't cover everything the customer asked. The fix (shown
in coordinator.py) is to (a) plan to cover every part, and (b) run a gap-check
refinement pass to catch anything missed.

Run this, then run coordinator.py with the SAME question to see the difference.
"""

import os
from dotenv import load_dotenv

from tools import ORDER_TOOL_SCHEMAS, run_tool
from subagent import SubAgent

load_dotenv()

# We reuse the same Order Specialist subagent.
ORDER_AGENT = SubAgent(
    name="Order Specialist",
    system_prompt=(
        "You are the Order Specialist for PyStack Mart. You look up customers "
        "and orders. Report the facts you find clearly and briefly."
    ),
    tool_schemas=ORDER_TOOL_SCHEMAS,
    run_tool_fn=run_tool,
)


def handle_too_narrowly(customer_message: str) -> str:
    """
    A BROKEN coordinator. Instead of analysing the WHOLE message, it assumes
    every question is just an order-status question and delegates only that.
    Notice there is NO planning step and NO gap-check.
    """
    print("\n[BROKEN Coordinator] Assuming this is only an order-status question...")
    print("[BROKEN Coordinator] Delegating ONLY to the Order Specialist.")

    # ❌ TOO-NARROW DECOMPOSITION: we hard-code a single narrow subtask and
    # ignore the refund and shipping parts of the customer's message.
    narrow_task = (
        f"The customer said: '{customer_message}'. "
        "Just look up the order status for any order ID you find."
    )
    finding = ORDER_AGENT.run(narrow_task)

    # We return only the order finding. The refund + shipping parts are lost.
    return finding


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not found.")
        print("Create a .env file in this folder with this line:")
        print('  ANTHROPIC_API_KEY=your-key-here')
        raise SystemExit(1)

    print("=" * 70)
    print("BROKEN multi-agent demo — TOO-NARROW decomposition.")
    print("Watch it answer only PART of a multi-part question.")
    print("Type 'quit' or 'exit' to stop.")
    print("=" * 70)
    print("Best prompt to expose the bug:")
    print("  I am CUST-1001. Is ORD-5001 delivered, can I refund it, "
          "and what is your shipping policy?")

    while True:
        user_message = input("\nYour question > ").strip()
        if user_message.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not user_message:
            continue
        answer = handle_too_narrowly(user_message)
        print("\n(TOO-NARROW) FINAL ANSWER:\n" + answer)
        print("\nNotice: the refund and shipping parts were never answered.")
