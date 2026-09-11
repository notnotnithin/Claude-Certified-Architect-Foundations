# Demo 1.2 — Multi-Agent System (Smart Order Support Assistant)

Second demo in **Domain 1: Agentic Architecture & Orchestration**, and a direct
continuation of Demo 1.1.
The single agent from 1.1 now becomes a **subagent**, and a new **coordinator** delegates work to specialists.
Maps to **Task Statement 1.2 — Orchestrate multi-agent systems with
coordinator–subagent patterns.**

---

## What changed since Demo 1.1

- In 1.1, **one agent** did everything (customers, orders, refund policy).
- In 1.2, a **coordinator** sits on top and delegates to two **specialists**:
  an **Order Specialist** and a **Policy Specialist**.
- The single-agent loop from 1.1 didn't disappear — it now runs **inside every
  subagent** (see `subagent.py`). Same loop, new wrapping.

---

## The concepts (in short)

- **Coordinator (the hub)** — the boss agent. It has **no tools of its own**.
  Its job: split the question into sub-tasks, pick which specialists to use,
  and combine their answers into one reply.

- **Subagent (a spoke)** — a small agent with one role and only the tools that
  role needs (Order Specialist, Policy Specialist). It's the Demo 1.1 loop reused.

- **Hub-and-spoke** — all communication goes **through the coordinator**.
  Subagents never talk to each other.

- **Isolated context** — a subagent does **not** see the coordinator's
  conversation or other subagents' work. The coordinator must pass it
  everything it needs inside the task text. (Each subagent starts fresh.)

- **Dynamic selection** — the coordinator picks **only the specialists it
  needs**. A shipping-only question shouldn't wake the refund logic.

- **Decomposition** — breaking the customer's message into clear sub-tasks,
  covering **every** part of a multi-part question.

- **Iterative refinement (gap-check)** — after combining the answers, the
  coordinator checks: "did I cover everything?" If not, it delegates again.

> **The classic trap (exam favourite):** *too-narrow decomposition* — the
> coordinator splits a broad question too narrowly and silently drops whole
> parts of it. See `antipattern_narrow.py` for the wrong way.

---

## The flow (in short)

```
You type a question
      │
      ▼
COORDINATOR plans  → which specialists? what task for each?
      │
      ├─ delegate → Order Specialist   (its own loop + tools)
      └─ delegate → Policy Specialist  (its own loop + tools)
      │
      ▼
COORDINATOR combines the findings into one draft answer
      │
      ▼
COORDINATOR gap-check → anything missing?
      ├─ yes → delegate again to fill the gap
      └─ no  → print final answer → done
```

1. You type one question.
2. `make_plan()` asks Claude which specialists are needed and writes each a task.
3. Each chosen subagent runs its own loop (with its own tools) and reports back.
4. `synthesize()` merges the findings into one reply.
5. `find_gaps()` checks coverage; if a part was missed, it re-delegates.

---

## Files

| File | Job |
|------|-----|
| `mock_data.py` | Fake "database": customers, orders, refund + shipping policy. |
| `tools.py` | Tools grouped by role: **order** tools and **policy** tools. |
| `subagent.py` | The Demo 1.1 loop, reused as a focused specialist (isolated context). |
| `coordinator.py` | **Main demo** — the hub that plans, delegates, combines, and gap-checks. |
| `antipattern_narrow.py` | The WRONG way: too-narrow decomposition (teaching contrast). |
| `.env.example` | Template for your API key — copy it to `.env`. |

`requirements.txt` lives **outside** this folder (one level up), same as Demo 1.1.

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
3. Run the multi-agent system and type one question at a time:
   ```bash
   python coordinator.py
   ```
   Type `quit` (or `exit`) to stop.

---

## Prompts to try (copy-paste)

**1. Dynamic selection — only ONE specialist is needed (policy):**
```
What does your shipping policy say about delivery time?
```

**2. Dynamic selection — only the order specialist is needed:**
```
I am CUST-1002. What is the status of order ORD-5003?
```

**3. Multi-part question — BOTH specialists, combined answer:**
```
I am CUST-1001. Is order ORD-5001 delivered, can I refund it, and what is your shipping policy?
```

---

## See the anti-pattern (too-narrow decomposition)

This shows the #1 multi-agent mistake the exam tests: the coordinator answers
only PART of a multi-part question.

```bash
python antipattern_narrow.py
```
Then paste the **same multi-part prompt** (#3 above) into both files and compare:

- `antipattern_narrow.py` → answers only the order status; refund + shipping are dropped.
- `coordinator.py` → covers all three parts (and the gap-check catches anything missed).

```
I am CUST-1001. Is order ORD-5001 delivered, can I refund it, and what is your shipping policy?
```
