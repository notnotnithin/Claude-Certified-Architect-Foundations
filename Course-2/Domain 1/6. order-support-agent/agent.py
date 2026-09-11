"""
agent.py
---------
THE HEART OF DEMO 6: DYNAMIC (ADAPTIVE) PLANNING.

In Demo 4 the coordinator made its whole plan UP FRONT, in one shot, then ran
it. That works when every part of the request is visible immediately.

But some requests are VAGUE: "something's off with my recent orders, sort it
out." You cannot plan that up front — you don't yet know what the orders are.
So the agent must:

    1. LOOK first (map the situation with list_customer_orders),
    2. DECIDE the next step based on what it just found,
    3. repeat — the plan UNFOLDS step by step from intermediate findings.

This is ADAPTIVE decomposition. We make it visible by keeping a PLAN scratchpad
that the agent REVISES after each step, so you can watch the plan change as new
facts come in.

FIXED PIPELINE vs ADAPTIVE (Task 1.6)
-------------------------------------
  - FIXED (prompt chaining): same steps every time. Great when predictable.
  - ADAPTIVE: next step depends on what was discovered. Great for open-ended
    investigation. THIS demo is adaptive. (See antipattern_fixed_pipeline.py
    for the rigid version and why it falls short on a vague request.)

HOW THE LOOP WORKS
------------------
Each round we ask the model for a small JSON object:
    {"thought": "...", "action": {...}, "updated_plan": ["step", ...],
     "done": false}
- if action is a tool call, we run it, show the result, and loop again;
- the model REVISES updated_plan every round based on the latest finding;
- when done is true, we ask for a final customer-facing answer.
"""

import os
import json
from dotenv import load_dotenv
import anthropic

from tools import run_tool

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"
MAX_STEPS = 12

# We describe the tools in plain text for the planner (it returns JSON actions,
# so it doesn't need the formal tool schema — just to know what's available).
TOOLS_DESCRIPTION = (
    "Available actions (tools):\n"
    "  - list_customer_orders(customer_id): see all of a customer's orders "
    "(brief status of each). Use FIRST for vague requests.\n"
    "  - get_order(order_id): full details of one order.\n"
    "  - get_refund_policy(): the refund rules.\n"
    "  - get_shipping_policy(): the shipping rules.\n"
)

PLANNER_SYSTEM = (
    "You are an adaptive customer-support investigator for PyStack Mart. "
    "Today's date is 2026-06-28. You work step by step and ADAPT your plan as "
    "you learn more.\n\n"
    + TOOLS_DESCRIPTION +
    "\nEach turn, respond with ONLY a JSON object:\n"
    "{\n"
    '  "thought": "one short sentence: what you learned and what to do next",\n'
    '  "updated_plan": ["short step", "short step", ...],\n'
    '  "action": {"tool": "<tool name>", "input": { ... }},\n'
    '  "done": false\n'
    "}\n"
    "Rules:\n"
    "- For a vague request, your FIRST action should be list_customer_orders.\n"
    "- Revise 'updated_plan' every turn based on what you just found (e.g. add "
    "a refund check for a recently delivered order, a shipping check for an "
    "in-transit order, a damage/return step for a damaged order).\n"
    "- Put ONE action per turn.\n"
    "- When you have investigated everything the plan needs, set \"done\": true "
    "and omit 'action'. Do not write the final answer yet."
)


def _ask_planner(messages: list) -> dict:
    """Ask the model for its next thought/plan/action as JSON."""
    response = client.messages.create(
        model=MODEL, max_tokens=700, system=PLANNER_SYSTEM, messages=messages,
    )
    text = "".join(b.text for b in response.content if b.type == "text")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        return json.loads(text[start:end + 1]) if start >= 0 else {"done": True}


FINAL_SYSTEM = (
    "You are a customer-support agent for PyStack Mart. Using ONLY the "
    "investigation notes provided, write ONE clear, friendly reply that "
    "addresses everything you found, order by order, with a recommended next "
    "step for each. Amounts are in Rupees (Rs.). Today is 2026-06-28."
)


def _write_final(customer_message: str, notes: list) -> str:
    notes_text = "\n".join(f"- {n}" for n in notes)
    user_block = (
        f"CUSTOMER MESSAGE:\n{customer_message}\n\n"
        f"INVESTIGATION NOTES (what you found):\n{notes_text}"
    )
    response = client.messages.create(
        model=MODEL, max_tokens=1200, system=FINAL_SYSTEM,
        messages=[{"role": "user", "content": user_block}],
    )
    return "".join(b.text for b in response.content if b.type == "text").strip()


def run_agent(customer_message: str) -> str:
    # The running conversation with the planner.
    messages = [{"role": "user", "content": customer_message}]
    notes = []          # plain-language findings we collect along the way
    last_plan = []

    for step in range(1, MAX_STEPS + 1):
        decision = _ask_planner(messages)

        # Show the adapting plan so the concept is visible.
        plan = decision.get("updated_plan", last_plan)
        if plan != last_plan:
            print(f"\n[Plan @ step {step}] (revised based on findings)")
            for i, s in enumerate(plan, 1):
                print(f"    {i}. {s}")
            last_plan = plan
        thought = decision.get("thought", "")
        if thought:
            print(f"[Thought] {thought}")

        # Are we done investigating?
        if decision.get("done") and "action" not in decision:
            print("\n[Investigation complete] Writing the final answer...")
            return _write_final(customer_message, notes)

        action = decision.get("action")
        if not action:
            # No action and not done -> nudge the model to finish.
            messages.append({"role": "assistant",
                             "content": json.dumps(decision)})
            messages.append({"role": "user",
                             "content": "If investigation is complete, set "
                                        "done=true with no action."})
            continue

        # Run the chosen tool and feed the result back so the NEXT plan adapts.
        tool, tool_input = action.get("tool"), action.get("input", {})
        print(f"  -> action: {tool}({tool_input})")
        result = run_tool(tool, tool_input)
        print(f"     result: {result}")
        notes.append(f"{tool}({tool_input}) -> {result}")

        # Append this round to the conversation so the model adapts next turn.
        messages.append({"role": "assistant", "content": json.dumps(decision)})
        messages.append({"role": "user",
                         "content": f"Result of {tool}: {json.dumps(result)}\n"
                                    f"Update your plan and choose the next "
                                    f"action, or set done=true."})

    return _write_final(customer_message, notes)


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not found.")
        print("Create a .env file in this folder with this line:")
        print('  ANTHROPIC_API_KEY=your-key-here')
        raise SystemExit(1)

    print("=" * 70)
    print("PyStack Mart — Adaptive Investigator (Demo 6)")
    print("The agent LOOKS first, then revises its PLAN based on what it finds.")
    print("Type your question and press Enter. Type 'quit' or 'exit' to stop.")
    print("=" * 70)
    print("Try a vague request like:")
    print("  - I am CUST-1001. Something's off with my recent orders, can you")
    print("    sort it out?")

    while True:
        user_message = input("\nYour question > ").strip()
        if user_message.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not user_message:
            continue
        answer = run_agent(user_message)
        print("\nFINAL ANSWER:\n" + answer)
