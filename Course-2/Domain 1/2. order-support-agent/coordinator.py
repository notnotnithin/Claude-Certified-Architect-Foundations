"""
coordinator.py
---------------
THE HEART OF DEMO 1.2: a COORDINATOR that manages SUBAGENTS.

In Demo 1.1 a single agent did everything. Here we use a "hub-and-spoke"
design:

        Coordinator  (the hub)
         /        \\
   Order          Policy
 Specialist      Specialist   (the spokes / subagents)

The COORDINATOR (Task Statement 1.2) does four things:
  1. DECOMPOSE  — break the customer's question into clear sub-tasks.
  2. DELEGATE   — DYNAMICALLY pick only the subagents it actually needs
                  (not always all of them), and write each one a focused task.
  3. AGGREGATE  — combine the subagents' answers into ONE reply.
  4. REFINE     — check the combined result for GAPS; if something is missing,
                  delegate again. (iterative refinement loop)

EXAM IDEAS SHOWN HERE
---------------------
  - Hub-and-spoke: ALL communication goes THROUGH the coordinator. Subagents
    never talk to each other.
  - Isolated context: the coordinator passes each subagent everything it needs
    inside the task text (subagents don't share memory).
  - Dynamic selection: a shipping-only question should NOT wake the refund
    logic, and vice-versa.
  - Too-narrow decomposition: the classic failure the exam tests. The refine
    step is our guard against it.

We let CLAUDE do the planning (which subagents, what task each gets) by asking
it to return a small JSON plan. Then plain Python runs that plan.
"""

import os
import json
from dotenv import load_dotenv
import anthropic

from tools import (
    ORDER_TOOL_SCHEMAS, POLICY_TOOL_SCHEMAS, run_tool,
)
from subagent import SubAgent

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"


# ==========================================================================
# 1. DEFINE THE SUBAGENTS (the spokes)
#    Each gets ONLY the tools its role needs.
# ==========================================================================
ORDER_AGENT = SubAgent(
    name="Order Specialist",
    system_prompt=(
        "You are the Order Specialist for PyStack Mart. You look up customers "
        "and orders. Use your tools to find real data. Report the facts you "
        "find clearly and briefly. Amounts are in Indian Rupees (Rs.)."
    ),
    tool_schemas=ORDER_TOOL_SCHEMAS,
    run_tool_fn=run_tool,
)

POLICY_AGENT = SubAgent(
    name="Policy Specialist",
    system_prompt=(
        "You are the Policy Specialist for PyStack Mart. You answer questions "
        "about the refund policy and the shipping policy. Use your tools to "
        "read the relevant policy, then explain how it applies. Be brief."
    ),
    tool_schemas=POLICY_TOOL_SCHEMAS,
    run_tool_fn=run_tool,
)

# The coordinator looks subagents up by name.
SUBAGENTS = {
    "order": ORDER_AGENT,
    "policy": POLICY_AGENT,
}


# ==========================================================================
# 2. THE COORDINATOR ASKS CLAUDE FOR A PLAN
#    "Which subagents do we need, and what should each one do?"
# ==========================================================================
PLANNER_SYSTEM = (
    "You are the COORDINATOR for a customer support system. You do NOT answer "
    "the customer directly and you have NO tools of your own. Your job is to "
    "break the customer's message into sub-tasks and decide which specialists "
    "to delegate to.\n\n"
    "Available specialists:\n"
    "  - 'order'  : looks up customers and orders (needs IDs from the message)\n"
    "  - 'policy' : explains the refund policy and the shipping policy\n\n"
    "Rules:\n"
    "  - Only choose the specialists that are actually needed. A pure shipping "
    "question does NOT need the order specialist, etc.\n"
    "  - Cover EVERY distinct thing the customer asked. Do not drop a part of "
    "a multi-part question.\n"
    "  - For each chosen specialist, write a clear 'task' telling it exactly "
    "what to find or explain, including any IDs from the customer message.\n\n"
    "Respond with ONLY a JSON object, no other text, in this shape:\n"
    '{"plan": [ {"agent": "order", "task": "..."}, '
    '{"agent": "policy", "task": "..."} ]}'
)


def make_plan(customer_message: str) -> list:
    """Ask Claude which subagents to use and what each should do."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=600,
        system=PLANNER_SYSTEM,
        messages=[{"role": "user", "content": customer_message}],
    )
    text = "".join(b.text for b in response.content if b.type == "text")
    # The planner is told to return pure JSON; parse it safely.
    try:
        plan = json.loads(text).get("plan", [])
    except json.JSONDecodeError:
        # If the model added stray text, try to find the JSON object in it.
        start, end = text.find("{"), text.rfind("}")
        plan = json.loads(text[start:end + 1]).get("plan", []) if start >= 0 else []
    return plan


# ==========================================================================
# 3. THE COORDINATOR COMBINES SUBAGENT RESULTS INTO ONE REPLY
# ==========================================================================
SYNTH_SYSTEM = (
    "You are the COORDINATOR writing the FINAL reply to the customer. You are "
    "given the customer's original message and the findings from one or more "
    "specialists. Combine them into a single, friendly, clear answer. Use only "
    "the findings provided — do not invent details. Amounts are in Rupees (Rs.)."
)


def synthesize(customer_message: str, findings: dict) -> str:
    """Combine all subagent findings into the final customer-facing answer."""
    findings_text = "\n\n".join(
        f"### Findings from the {name} specialist:\n{result}"
        for name, result in findings.items()
    )
    user_block = (
        f"CUSTOMER MESSAGE:\n{customer_message}\n\n"
        f"SPECIALIST FINDINGS:\n{findings_text}"
    )
    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        system=SYNTH_SYSTEM,
        messages=[{"role": "user", "content": user_block}],
    )
    return "".join(b.text for b in response.content if b.type == "text").strip()


# ==========================================================================
# 4. THE COORDINATOR CHECKS FOR GAPS (iterative refinement)
# ==========================================================================
GAPCHECK_SYSTEM = (
    "You are the COORDINATOR checking your own work. Given the customer's "
    "original message and a draft answer, decide if EVERY part of the "
    "customer's request has been addressed.\n"
    "Respond with ONLY JSON: {\"complete\": true} if nothing is missing, or "
    "{\"complete\": false, \"missing\": \"short description of what is still "
    "unanswered\"}."
)


def find_gaps(customer_message: str, draft_answer: str) -> dict:
    """Ask Claude whether the draft answer covers the whole request."""
    user_block = (
        f"CUSTOMER MESSAGE:\n{customer_message}\n\n"
        f"DRAFT ANSWER:\n{draft_answer}"
    )
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=GAPCHECK_SYSTEM,
        messages=[{"role": "user", "content": user_block}],
    )
    text = "".join(b.text for b in response.content if b.type == "text")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        return json.loads(text[start:end + 1]) if start >= 0 else {"complete": True}


# ==========================================================================
# 5. PUT IT TOGETHER — the coordinator's main routine
# ==========================================================================
def handle(customer_message: str) -> str:
    print("\n[Coordinator] Planning which specialists to use...")
    plan = make_plan(customer_message)

    if not plan:
        return ("[Coordinator] I couldn't form a plan for that request. "
                "Could you rephrase?")

    # Show the plan so the routing is visible during the demo.
    chosen = ", ".join(step["agent"] for step in plan)
    print(f"[Coordinator] Plan: delegate to -> {chosen}")

    # DELEGATE: run each chosen subagent with its focused task.
    # (All communication goes THROUGH the coordinator — hub-and-spoke.)
    findings = {}
    for step in plan:
        agent_key, task = step["agent"], step["task"]
        agent = SUBAGENTS.get(agent_key)
        if agent is None:
            findings[agent_key] = f"[No specialist named '{agent_key}'.]"
            continue
        print(f"\n[Coordinator] -> Delegating to '{agent.name}':\n   task: {task}")
        findings[agent.name] = agent.run(task)

    # AGGREGATE: combine findings into one reply.
    print("\n[Coordinator] Combining specialist findings into one answer...")
    draft = synthesize(customer_message, findings)

    # REFINE: one gap-check pass. If something is missing, delegate again.
    gap = find_gaps(customer_message, draft)
    if not gap.get("complete", True):
        missing = gap.get("missing", "")
        print(f"\n[Coordinator] Gap found: {missing}")
        print("[Coordinator] Re-planning to fill the gap...")
        followup_plan = make_plan(
            f"{customer_message}\n\n(Still unanswered: {missing})"
        )
        for step in followup_plan:
            agent = SUBAGENTS.get(step["agent"])
            if agent:
                print(f"[Coordinator] -> Re-delegating to '{agent.name}'.")
                findings[f"{agent.name} (follow-up)"] = agent.run(step["task"])
        draft = synthesize(customer_message, findings)
    else:
        print("[Coordinator] Gap-check passed: all parts addressed.")

    return draft


# ==========================================================================
# Interactive runner — type one prompt at a time (like Demo 1.1).
# ==========================================================================
if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not found.")
        print("Create a .env file in this folder with this line:")
        print('  ANTHROPIC_API_KEY=your-key-here')
        raise SystemExit(1)

    print("=" * 70)
    print("PyStack Mart — Multi-Agent Support (Demo 1.2)")
    print("A coordinator delegates to Order and Policy specialists.")
    print("Type your question and press Enter. Type 'quit' or 'exit' to stop.")
    print("=" * 70)
    print("Try things like:")
    print("  - What does your shipping policy say about delivery time?")
    print("  - I am CUST-1001. Is order ORD-5001 delivered, and can I refund it?")

    while True:
        user_message = input("\nYour question > ").strip()
        if user_message.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not user_message:
            continue
        answer = handle(user_message)
        print("\nFINAL ANSWER:\n" + answer)
