"""
antipattern_no_context.py
--------------------------
TEACHING FILE — shows the Task 1.3 mistake: ASSUMING SUBAGENTS SHARE MEMORY.

THE TRAP
--------
A dependent subtask needs facts another subagent already found. The broken
coordinator below runs the Order Specialist, then runs the Policy Specialist
WITHOUT passing the order facts into its task. Because subagents have ISOLATED
context, the Policy Specialist never sees the order status — so it cannot give
a definite answer and has to guess or ask for the very facts that were already
known.

WHY IT'S WRONG
--------------
Subagents do NOT inherit the coordinator's memory or each other's results. If
the coordinator doesn't COPY the needed facts into the next task text, that
information simply isn't there. The fix (in coordinator.py) is EXPLICIT context
passing: inject prior findings into the dependent subagent's task.

Run this, then run coordinator.py with the SAME prompt to see the difference.
"""

import os
from dotenv import load_dotenv

from tools import ORDER_TOOL_SCHEMAS, POLICY_TOOL_SCHEMAS, run_tool
from subagent import AgentDefinition, SubAgent

load_dotenv()

ORDER_DEF = AgentDefinition(
    name="Order Specialist",
    description="Looks up customers and orders.",
    system_prompt=(
        "You are the Order Specialist for PyStack Mart. Look up customers and "
        "orders using your tools. Report the facts clearly and briefly."
    ),
    tool_schemas=ORDER_TOOL_SCHEMAS,
    run_tool_fn=run_tool,
)

POLICY_DEF = AgentDefinition(
    name="Policy Specialist",
    description="Explains refund and shipping policies.",
    system_prompt=(
        "You are the Policy Specialist for PyStack Mart. Explain the refund "
        "policy and decide if a refund is allowed. Be brief."
    ),
    tool_schemas=POLICY_TOOL_SCHEMAS,
    run_tool_fn=run_tool,
)


def handle_without_passing_context(customer_message: str) -> str:
    """
    A BROKEN coordinator. It runs the order lookup, then asks the Policy
    Specialist to decide the refund — but NEVER passes the order facts along.
    """
    # Step 1: Order Specialist finds the order facts.
    print("\n[BROKEN Coordinator] Spawning Order Specialist...")
    order_finding = SubAgent(ORDER_DEF).run(
        f"The customer said: '{customer_message}'. Look up the customer and "
        "the order, and report the order status."
    )
    print(f"[BROKEN Coordinator] Order Specialist found:\n   {order_finding['summary']}")

    # Step 2: Policy Specialist is asked to decide the refund...
    # ❌ BUG: we do NOT pass the order status we just found. The Policy
    # Specialist has isolated context and cannot see order_finding at all.
    print("\n[BROKEN Coordinator] Spawning Policy Specialist WITHOUT the order facts...")
    policy_finding = SubAgent(POLICY_DEF).run(
        "Decide whether this customer's order can be refunded."
        # (notice: no order status, no order ID, nothing passed in)
    )

    return policy_finding["summary"]


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not found.")
        print("Create a .env file in this folder with this line:")
        print('  ANTHROPIC_API_KEY=your-key-here')
        raise SystemExit(1)

    print("=" * 70)
    print("BROKEN demo — subagent context is NOT shared automatically.")
    print("Watch the Policy Specialist fail because it never receives the")
    print("order facts the Order Specialist already found.")
    print("Type 'quit' or 'exit' to stop.")
    print("=" * 70)
    print("Best prompt to expose the bug:")
    print("  I am CUST-1001. Is ORD-5001 delivered, and based on that can I "
          "refund it?")

    while True:
        user_message = input("\nYour question > ").strip()
        if user_message.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not user_message:
            continue
        answer = handle_without_passing_context(user_message)
        print("\n(NO-CONTEXT) FINAL ANSWER:\n" + answer)
        print("\nNotice: the Policy Specialist had no order facts to work with.")
