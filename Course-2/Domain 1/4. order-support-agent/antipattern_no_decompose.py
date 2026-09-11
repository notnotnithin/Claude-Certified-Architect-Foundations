"""
antipattern_no_decompose.py
---------------------------
TEACHING FILE — shows the Demo 4 mistake: NOT decomposing a multi-concern
message. The coordinator treats the whole message as ONE task and hands it to
a single specialist, so most concerns are dropped or half-answered.

THE TRAP
--------
A customer asks THREE things in one message:
    "I am CUST-1001. Is ORD-5001 delivered, can I refund it, and please
     update my address to 99 Park Street, Pune 411002."

The broken coordinator below does NOT break this into concerns. It just throws
the whole message at the Order Specialist. That specialist can answer the order
part, but it has no refund-policy tool and no account tool — so the refund and
address-change concerns are never properly handled.

WHY IT'S WRONG
--------------
A bundled message contains DISTINCT items. If you don't split them, each
specialist sees a request full of things outside its scope, and concerns get
dropped. The fix (in coordinator.py) is to DECOMPOSE the message into concerns,
investigate each with the right specialist, and synthesize one unified reply.

Run this, then run coordinator.py with the SAME message to see the difference.
"""

import os
from dotenv import load_dotenv

from tools import ORDER_TOOL_SCHEMAS, run_tool
from subagent import AgentDefinition, SubAgent

load_dotenv()

ORDER_DEF = AgentDefinition(
    name="Order Specialist",
    description="Looks up orders and their status.",
    system_prompt=(
        "You are the Order Specialist for PyStack Mart. Look up orders using "
        "your tools and report what you find. Be brief."
    ),
    tool_schemas=ORDER_TOOL_SCHEMAS,
    run_tool_fn=run_tool,
)


def handle_as_one_blob(customer_message: str) -> str:
    """
    A BROKEN coordinator. No decomposition: it sends the ENTIRE multi-concern
    message to a single specialist and returns whatever comes back.
    """
    print("\n[BROKEN Coordinator] Not splitting the message into concerns.")
    print("[BROKEN Coordinator] Sending the WHOLE message to the Order Specialist.")

    # ❌ NO DECOMPOSITION: the whole bundled message goes to one specialist
    # that only has order tools. Refund + address concerns can't be handled.
    finding = ORDER_DEF and SubAgent(ORDER_DEF).run(customer_message)
    return finding["summary"]


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not found.")
        print("Create a .env file in this folder with this line:")
        print('  ANTHROPIC_API_KEY=your-key-here')
        raise SystemExit(1)

    print("=" * 70)
    print("BROKEN demo — NO decomposition of a multi-concern message.")
    print("Watch it answer only the order part and drop refund + address.")
    print("Type 'quit' or 'exit' to stop.")
    print("=" * 70)
    print("Best prompt to expose the bug:")
    print("  I am CUST-1001. Is ORD-5001 delivered, can I refund it, and")
    print("  please update my address to 99 Park Street, Pune 411002.")

    while True:
        user_message = input("\nYour question > ").strip()
        if user_message.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not user_message:
            continue
        answer = handle_as_one_blob(user_message)
        print("\n(NO-DECOMPOSE) FINAL ANSWER:\n" + answer)
        print("\nNotice: the refund and address concerns were not properly handled.")
