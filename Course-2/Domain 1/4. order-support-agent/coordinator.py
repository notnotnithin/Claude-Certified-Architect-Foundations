"""
coordinator.py
---------------
THE HEART OF DEMO 4: handling a MULTI-CONCERN request by DECOMPOSING it into
distinct items, investigating each, and SYNTHESIZING one unified resolution.

This continues Demo 1.3 (spawning, context passing, parallel) and adds the
decomposition ideas from Task 1.4 and Task 1.6.

THE NEW IDEA: decompose by CONCERN, not by specialist.
------------------------------------------------------
A real customer message often bundles several requests:

    "I'm CUST-1001. Is ORD-5001 delivered, can I refund it,
     and please update my address to 99 Park Street, Pune."

That is THREE distinct concerns:
    1. order status        (order specialist)
    2. refund eligibility  (needs the status -> depends on concern 1)
    3. address update      (account specialist)

The coordinator breaks the message into these items, handles each (some in
parallel, some dependent), then writes ONE unified reply that resolves all of
them — instead of answering only the first.

TWO DECOMPOSITION STYLES (Task 1.6)
-----------------------------------
  - PROMPT CHAINING (fixed pipeline): when the steps are predictable and
    always the same, you can run a fixed sequence. Good for predictable work.
  - DYNAMIC DECOMPOSITION (adaptive): when you don't know up front what the
    message contains, you ASK the model to break it into concerns and decide
    dependencies. Good for open-ended, varied requests.
  This demo uses DYNAMIC decomposition, because customer messages vary. We
  explain the contrast in the README and in comments.
"""

import os
import json
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import anthropic

from tools import (
    ORDER_TOOL_SCHEMAS, POLICY_TOOL_SCHEMAS, ACCOUNT_TOOL_SCHEMAS, run_tool,
)
from subagent import AgentDefinition, SubAgent

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"
ALLOWED_TOOLS = ["Task"]   # coordinator must have "Task" to spawn subagents


# ==========================================================================
# 1. SUBAGENTS — now THREE specialists (order, policy, account)
# ==========================================================================
ORDER_DEF = AgentDefinition(
    name="Order Specialist",
    description="Looks up orders and their status.",
    system_prompt=(
        "You are the Order Specialist for PyStack Mart. Look up orders using "
        "your tools and report the facts (status, dates, amount) clearly and "
        "briefly. Amounts are in Rupees (Rs.)."
    ),
    tool_schemas=ORDER_TOOL_SCHEMAS,
    run_tool_fn=run_tool,
)

POLICY_DEF = AgentDefinition(
    name="Policy Specialist",
    description="Explains refund and shipping policies and applies them.",
    system_prompt=(
        "You are the Policy Specialist for PyStack Mart. Explain the refund or "
        "shipping policy using your tools. If the task gives you order facts "
        "(like a status or delivery date), apply the policy to those exact "
        "facts and give a clear decision. Be brief."
    ),
    tool_schemas=POLICY_TOOL_SCHEMAS,
    run_tool_fn=run_tool,
)

ACCOUNT_DEF = AgentDefinition(
    name="Account Specialist",
    description="Reads and updates customer account details (like address).",
    system_prompt=(
        "You are the Account Specialist for PyStack Mart. You can look up a "
        "customer and update their address using your tools. Confirm exactly "
        "what you changed. Be brief."
    ),
    tool_schemas=ACCOUNT_TOOL_SCHEMAS,
    run_tool_fn=run_tool,
)

AGENT_DEFS = {"order": ORDER_DEF, "policy": POLICY_DEF, "account": ACCOUNT_DEF}


# ==========================================================================
# 2. THE Task TOOL — spawn one subagent (same as Demo 1.3)
# ==========================================================================
def spawn_task(agent_key: str, task: str) -> dict:
    if "Task" not in ALLOWED_TOOLS:
        raise RuntimeError("Coordinator cannot spawn: 'Task' not in allowedTools.")
    definition = AGENT_DEFS.get(agent_key)
    if definition is None:
        return {"agent": agent_key, "summary": f"[no agent '{agent_key}']",
                "sources": []}
    print(f"\n[Coordinator] spawn_task('{agent_key}')")
    print(f"   task: {task}")
    return SubAgent(definition).run(task)


def spawn_parallel(specs: list) -> list:
    """Spawn several INDEPENDENT subagents at the same time."""
    print(f"\n[Coordinator] Investigating {len(specs)} concern(s) IN PARALLEL...")
    with ThreadPoolExecutor(max_workers=len(specs)) as pool:
        futures = [pool.submit(spawn_task, key, task) for key, task in specs]
        return [f.result() for f in futures]


# ==========================================================================
# 3. DECOMPOSE the message into distinct CONCERNS
# ==========================================================================
DECOMPOSE_SYSTEM = (
    "You are the COORDINATOR of a customer-support system. A customer message "
    "may contain SEVERAL separate concerns. Break the message into a list of "
    "distinct concerns and assign each to a specialist.\n\n"
    "Specialists:\n"
    "  - 'order'   : looks up an order's status/details (needs an order ID)\n"
    "  - 'policy'  : explains and applies the refund/shipping policy\n"
    "  - 'account' : reads or updates the customer's account (e.g. address)\n\n"
    "For each concern decide if it DEPENDS on another concern's result:\n"
    "  - e.g. a refund decision needs the order status first -> dependent on 'order'.\n"
    "  - independent concerns can be investigated in parallel.\n\n"
    "Write each task as a GOAL, and include any IDs/values from the message "
    "(order IDs, customer IDs, a new address, etc.). Cover EVERY concern — do "
    "not drop any part of the message.\n\n"
    "Respond with ONLY JSON in this shape:\n"
    '{\n'
    '  "concerns": [\n'
    '    {"id": 1, "agent": "order",   "task": "...", "depends_on": null},\n'
    '    {"id": 2, "agent": "policy",  "task": "...", "depends_on": 1},\n'
    '    {"id": 3, "agent": "account", "task": "...", "depends_on": null}\n'
    '  ]\n'
    '}\n'
    "Use depends_on = the id of the concern it needs, or null if independent."
)


def decompose(customer_message: str) -> list:
    response = client.messages.create(
        model=MODEL, max_tokens=800, system=DECOMPOSE_SYSTEM,
        messages=[{"role": "user", "content": customer_message}],
    )
    text = "".join(b.text for b in response.content if b.type == "text")
    try:
        return json.loads(text).get("concerns", [])
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        return json.loads(text[start:end + 1]).get("concerns", []) if start >= 0 else []


# ==========================================================================
# 4. SYNTHESIZE one unified resolution from all concern findings
# ==========================================================================
SYNTH_SYSTEM = (
    "You are the COORDINATOR writing ONE unified reply to the customer. You "
    "are given the customer's message and the findings for EACH concern. "
    "Address EVERY concern in a single, clear, friendly answer, in the order "
    "the customer raised them. Use only the findings provided — do not invent "
    "details. Amounts are in Rupees (Rs.)."
)


def synthesize(customer_message: str, findings_by_concern: dict) -> str:
    findings_text = "\n\n".join(
        f"### Concern {cid}: handled by {f['agent']}\n{f['summary']}"
        for cid, f in findings_by_concern.items()
    )
    user_block = (
        f"CUSTOMER MESSAGE:\n{customer_message}\n\n"
        f"FINDINGS PER CONCERN:\n{findings_text}"
    )
    response = client.messages.create(
        model=MODEL, max_tokens=1200, system=SYNTH_SYSTEM,
        messages=[{"role": "user", "content": user_block}],
    )
    return "".join(b.text for b in response.content if b.type == "text").strip()


# ==========================================================================
# 5. PUT IT TOGETHER — decompose, investigate (parallel + dependent), unify
# ==========================================================================
def _format_prior(findings_by_concern: dict, needed_id) -> str:
    f = findings_by_concern.get(needed_id)
    if not f:
        return ""
    return (f"- {f['agent']} found: {f['summary']} "
            f"(sources: {json.dumps(f['sources'])})")


def handle(customer_message: str) -> str:
    print("\n[Coordinator] Decomposing the message into concerns...")
    concerns = decompose(customer_message)

    if not concerns:
        return "[Coordinator] I couldn't break that into concerns. Please rephrase."

    # Show the decomposition so it's visible during the demo.
    print(f"[Coordinator] Found {len(concerns)} concern(s):")
    for c in concerns:
        dep = f" (depends on #{c['depends_on']})" if c.get("depends_on") else ""
        print(f"   #{c['id']} -> {c['agent']}{dep}: {c['task']}")

    findings_by_concern = {}

    # STEP 1: investigate all INDEPENDENT concerns in parallel.
    independent = [c for c in concerns if not c.get("depends_on")]
    dependent = [c for c in concerns if c.get("depends_on")]

    if independent:
        specs = [(c["agent"], c["task"]) for c in independent]
        results = spawn_parallel(specs)
        for c, result in zip(independent, results):
            findings_by_concern[c["id"]] = result

    # STEP 2: investigate DEPENDENT concerns, injecting the result they need
    # (explicit context passing, from Demo 1.3).
    for c in dependent:
        prior = _format_prior(findings_by_concern, c["depends_on"])
        enriched = (
            f"{c['task']}\n\n"
            f"Here is what concern #{c['depends_on']} already found "
            f"(use these exact facts):\n{prior}"
        )
        print(f"\n[Coordinator] Concern #{c['id']} depends on #{c['depends_on']} "
              f"— passing those facts in.")
        findings_by_concern[c["id"]] = spawn_task(c["agent"], enriched)

    # STEP 3: write ONE unified resolution covering every concern.
    print("\n[Coordinator] Writing one unified resolution for all concerns...")
    return synthesize(customer_message, findings_by_concern)


# ==========================================================================
# Interactive runner — type one prompt at a time.
# ==========================================================================
if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not found.")
        print("Create a .env file in this folder with this line:")
        print('  ANTHROPIC_API_KEY=your-key-here')
        raise SystemExit(1)

    print("=" * 70)
    print("PyStack Mart — Multi-Concern Support (Demo 4)")
    print("The coordinator splits ONE message into several concerns,")
    print("investigates each, and replies with one unified resolution.")
    print("Type your question and press Enter. Type 'quit' or 'exit' to stop.")
    print("=" * 70)
    print("Try a multi-concern message like:")
    print("  I am CUST-1001. Is ORD-5001 delivered, can I refund it, and")
    print("  please update my address to 99 Park Street, Pune 411002.")

    while True:
        user_message = input("\nYour question > ").strip()
        if user_message.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not user_message:
            continue
        answer = handle(user_message)
        print("\nFINAL ANSWER:\n" + answer)
