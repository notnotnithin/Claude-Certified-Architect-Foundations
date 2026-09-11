"""
coordinator.py
---------------
THE HEART OF DEMO 1.3: how a coordinator SPAWNS subagents, PASSES CONTEXT to
them explicitly, and runs them IN PARALLEL.

This continues Demo 1.2 (coordinator + specialists), and adds the Task 1.3
ideas:

1. THE Task TOOL (spawn_task)
   In the Agent SDK a coordinator spawns a subagent by calling the "Task"
   tool, and its allowedTools must include "Task". We model that here with a
   spawn_task() helper: the coordinator's ONLY way to do work is to spawn a
   subagent via this function. (ALLOWED_TOOLS lists "Task" to make the rule
   explicit for the demo.)

2. EXPLICIT CONTEXT PASSING
   Subagents do NOT inherit the coordinator's memory. So when one subagent's
   result is needed by another, the coordinator copies that finding straight
   INTO the next subagent's task text. We show this: the Order Specialist's
   findings are passed into the Policy Specialist's task.

3. PARALLEL SPAWNING
   When two subtasks DON'T depend on each other, the coordinator spawns them
   together (one "batch") and runs them at the same time using threads —
   modelling "multiple Task calls in a single response".

4. GOAL-ORIENTED TASKS
   The coordinator writes tasks that state the GOAL ("find out X"), not
   step-by-step tool instructions. This lets each subagent adapt.
"""

import os
import json
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import anthropic

from tools import (
    ORDER_TOOL_SCHEMAS, POLICY_TOOL_SCHEMAS, run_tool,
)
from subagent import AgentDefinition, SubAgent

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-6"

# The coordinator's "allowed tools". In the Agent SDK, a coordinator must have
# "Task" in allowedTools to be able to spawn subagents. We list it here to make
# that requirement explicit for the demo.
ALLOWED_TOOLS = ["Task"]


# ==========================================================================
# 1. DEFINE THE SUBAGENTS using AgentDefinition (Task 1.3)
# ==========================================================================
ORDER_DEF = AgentDefinition(
    name="Order Specialist",
    description="Looks up customers and orders. Needs IDs in its task text.",
    system_prompt=(
        "You are the Order Specialist for PyStack Mart. You look up customers "
        "and orders using your tools. Report the facts you find clearly and "
        "briefly. Amounts are in Indian Rupees (Rs.)."
    ),
    tool_schemas=ORDER_TOOL_SCHEMAS,
    run_tool_fn=run_tool,
)

POLICY_DEF = AgentDefinition(
    name="Policy Specialist",
    description="Explains the refund and shipping policies.",
    system_prompt=(
        "You are the Policy Specialist for PyStack Mart. You explain the "
        "refund policy and the shipping policy using your tools. If the task "
        "gives you order facts (like a status or delivery date), apply the "
        "policy to those exact facts. Be brief."
    ),
    tool_schemas=POLICY_TOOL_SCHEMAS,
    run_tool_fn=run_tool,
)

AGENT_DEFS = {"order": ORDER_DEF, "policy": POLICY_DEF}


# ==========================================================================
# 2. THE Task TOOL — the ONLY way the coordinator does work.
# ==========================================================================
def spawn_task(agent_key: str, task: str) -> dict:
    """
    Spawn ONE subagent (like calling the SDK 'Task' tool) and return its
    structured finding. The coordinator must put everything the subagent needs
    INTO `task`, because subagents have isolated context.
    """
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
    """
    Spawn several subagents AT THE SAME TIME (models emitting multiple Task
    calls in one response). `specs` is a list of (agent_key, task) pairs that
    do NOT depend on each other.
    """
    print(f"\n[Coordinator] Spawning {len(specs)} subagents IN PARALLEL...")
    with ThreadPoolExecutor(max_workers=len(specs)) as pool:
        futures = [pool.submit(spawn_task, key, task) for key, task in specs]
        return [f.result() for f in futures]


# ==========================================================================
# 3. PLANNER — decide subagents, tasks, and whether they can run in parallel.
# ==========================================================================
PLANNER_SYSTEM = (
    "You are the COORDINATOR of a customer-support system. You have NO tools "
    "except the ability to spawn specialist subagents. Plan how to answer the "
    "customer.\n\n"
    "Specialists:\n"
    "  - 'order'  : looks up customers and orders (needs IDs from the message)\n"
    "  - 'policy' : explains the refund policy and the shipping policy\n\n"
    "Decide, for each subtask, whether it DEPENDS on another subtask's result:\n"
    "  - If a subtask needs facts another subtask will find (e.g. a refund "
    "decision needs the order's status first), mark it dependent.\n"
    "  - Independent subtasks can run in parallel.\n\n"
    "Write each task as a GOAL (what to find or explain), not step-by-step "
    "instructions. Cover EVERY part of the customer's message.\n\n"
    "Respond with ONLY JSON in this shape:\n"
    '{\n'
    '  "parallel": [ {"agent":"order","task":"..."},'
    ' {"agent":"policy","task":"..."} ],\n'
    '  "dependent": [ {"agent":"policy","task":"...","needs":"order"} ]\n'
    '}\n'
    "Either list may be empty. Use 'dependent' only when a task truly needs "
    "another's result."
)


def make_plan(customer_message: str) -> dict:
    response = client.messages.create(
        model=MODEL, max_tokens=700, system=PLANNER_SYSTEM,
        messages=[{"role": "user", "content": customer_message}],
    )
    text = "".join(b.text for b in response.content if b.type == "text")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        return json.loads(text[start:end + 1]) if start >= 0 else \
            {"parallel": [], "dependent": []}


# ==========================================================================
# 4. SYNTHESIS — combine structured findings into one reply (with attribution)
# ==========================================================================
SYNTH_SYSTEM = (
    "You are the COORDINATOR writing the FINAL reply to the customer. You are "
    "given the customer's message and structured findings from specialists "
    "(each with a summary and its sources). Combine them into one friendly, "
    "clear answer. Use only the findings provided — do not invent details. "
    "Amounts are in Rupees (Rs.)."
)


def synthesize(customer_message: str, findings: list) -> str:
    findings_text = "\n\n".join(
        f"### {f['agent']} (sources: {json.dumps(f['sources'])})\n{f['summary']}"
        for f in findings
    )
    user_block = (
        f"CUSTOMER MESSAGE:\n{customer_message}\n\n"
        f"STRUCTURED FINDINGS:\n{findings_text}"
    )
    response = client.messages.create(
        model=MODEL, max_tokens=1000, system=SYNTH_SYSTEM,
        messages=[{"role": "user", "content": user_block}],
    )
    return "".join(b.text for b in response.content if b.type == "text").strip()


# ==========================================================================
# 5. PUT IT TOGETHER
# ==========================================================================
def _format_prior(findings: list) -> str:
    """Turn prior findings into text we can inject into a dependent task."""
    return "\n".join(
        f"- {f['agent']} found: {f['summary']} (sources: {json.dumps(f['sources'])})"
        for f in findings
    )


def handle(customer_message: str) -> str:
    print("\n[Coordinator] Planning...")
    plan = make_plan(customer_message)
    parallel = plan.get("parallel", [])
    dependent = plan.get("dependent", [])

    findings = []

    # STEP 1: run all INDEPENDENT subtasks in parallel.
    if parallel:
        specs = [(s["agent"], s["task"]) for s in parallel]
        findings.extend(spawn_parallel(specs))

    # STEP 2: run DEPENDENT subtasks one by one, INJECTING prior findings
    # directly into the task text (explicit context passing).
    for step in dependent:
        prior = _format_prior(findings)
        enriched_task = (
            f"{step['task']}\n\n"
            f"Here is what other specialists already found "
            f"(use these exact facts):\n{prior}"
        )
        print(f"\n[Coordinator] This task depends on earlier results — "
              f"passing them in explicitly.")
        findings.append(spawn_task(step["agent"], enriched_task))

    if not findings:
        return "[Coordinator] I couldn't form a plan for that. Please rephrase."

    # STEP 3: combine everything into one answer.
    print("\n[Coordinator] Combining findings into one answer...")
    return synthesize(customer_message, findings)


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
    print("PyStack Mart — Multi-Agent Support (Demo 1.3)")
    print("Coordinator spawns subagents, passes context, and runs in parallel.")
    print("Type your question and press Enter. Type 'quit' or 'exit' to stop.")
    print("=" * 70)
    print("Try things like:")
    print("  - Compare orders ORD-5001 and ORD-5003 for customer CUST-1001.")
    print("  - I am CUST-1001. Is ORD-5001 delivered, and based on that can I")
    print("    refund it?")

    while True:
        user_message = input("\nYour question > ").strip()
        if user_message.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        if not user_message:
            continue
        answer = handle(user_message)
        print("\nFINAL ANSWER:\n" + answer)
