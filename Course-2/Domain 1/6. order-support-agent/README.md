# Demo 6 — Dynamic (Adaptive) Planning

Sixth demo in **Domain 1: Agentic Architecture & Orchestration**, continuing
from Demo 5.
The agent stops planning everything up front. Instead it **looks
first, then revises its plan based on what it finds** — adapting step by step.
Covers the **adaptive-decomposition** parts of **Task Statement 1.6** (fixed
pipeline vs dynamic adaptive decomposition; plans that generate subtasks from
intermediate findings).

---

## What changed since Demo 4

- Demo 4 decomposed the message **once, up front**, then ran the plan. Good for
  requests where every part is visible immediately.
- Demo 6 handles **vague** requests ("sort out my recent orders") where you
  **can't** plan up front. The agent maps the situation first, then decides the
  next step from what it discovered — the plan **unfolds**.
- New tool `list_customer_orders` lets the agent "look first."
- Customer CUST-1001 now has several orders in different states (recent,
  old, in-transit, damaged) so adaptation actually matters.

---

## The concepts (in short)

- **Fixed pipeline (prompt chaining)** — the same predetermined steps every
  time. Great when the work is **predictable**.

- **Dynamic / adaptive decomposition** — the **next step depends on what you
  just found**. Great for **open-ended** investigation.

- **Map first, then plan** — for a vague request, the first action is to look
  (`list_customer_orders`). Only then can a sensible plan be made.

- **Adaptive plan** — a living list of steps the agent **revises every round**
  as findings come in (e.g. "found an in-transit order → add a shipping check";
  "found a damaged order → add a return step").

- **Prioritized investigation** — the agent handles what actually matters,
  instead of doing fixed work that may be irrelevant.

> **The trap (exam favourite):** using a **fixed pipeline** for a request that
> needs adaptation — so you investigate the wrong things and miss the real
> issues. See `antipattern_fixed_pipeline.py`.

---

## The flow (in short)

```
You type a VAGUE request
      │
      ▼
LOOK first  → list_customer_orders (map the situation)
      │
      ▼
REVISE PLAN based on what was found
      │
      ├─ found in-transit order  → add a shipping check
      ├─ found recent delivered  → add a refund-window check
      └─ found damaged order      → add a return step
      │
      ▼
do the NEXT step → revise the plan again → ... → done
      │
      ▼
write ONE final answer (per-order, with a next step for each)
```

1. You type one vague request.
2. The agent's first action maps the situation (`list_customer_orders`).
3. After each finding it **revises its plan** and picks the next action.
4. When the plan is fully investigated, it writes one clear per-order answer.

---

## Files

| File | Job |
|------|-----|
| `mock_data.py` | CUST-1001 with several orders in different states; policies. |
| `tools.py` | Tools incl. `list_customer_orders` (the "look first" tool). |
| `agent.py` | **Main demo** — the adaptive planning loop (revises plan each step). |
| `antipattern_fixed_pipeline.py` | The WRONG way: a rigid fixed pipeline that can't adapt. |
| `.env.example` | Template for your API key — copy it to `.env`. |

`requirements.txt` lives **outside** this folder (one level up), same as before.

---

## Setup & run

1. Install packages (from the folder that has `requirements.txt`):
   ```bash
   pip install -r requirements.txt
   ```
2. Create your key file inside this demo folder and paste your key into it:
   ```bash
   # Windows (PowerShell):    copy .env.example .env
   # macOS / Linux / WSL:     cp .env.example .env
   ```
   Then edit `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-...your-real-key...
   ```
3. Run the agent and type one question at a time:
   ```bash
   python agent.py
   ```
   Type `quit` (or `exit`) to stop.

---

## Prompts to try (copy-paste)

**1. Vague request — the headline demo (watch the plan adapt):**
```
I am CUST-1001. Something's off with my recent orders, can you sort it out?
```

**2. Slightly directed, still open-ended:**
```
I am CUST-1001. Please review all my orders and tell me what needs my attention.
```

**3. A specific request (less adaptation needed — for contrast):**
```
I am CUST-1001. Is my Desk Lamp order okay?
```
(It's ORD-5006, flagged damaged — watch the agent add a return/damage step.)

---

## See the anti-pattern (fixed pipeline)

This shows why a rigid pipeline fails on a vague request.

```bash
python antipattern_fixed_pipeline.py
```
Then paste the **same vague prompt #1** into both files and compare:

- `antipattern_fixed_pipeline.py` → always checks only the policy + ORD-5001,
  missing the in-transit, old, and damaged orders.
- `agent.py` → lists all orders first, then adapts its plan to cover each one.

```
I am CUST-1001. Something's off with my recent orders, can you sort it out?
```
