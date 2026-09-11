# Demo 7 — Persistent Sessions

The final demo in **Domain 1: Agentic Architecture & Orchestration**, continuing
from Demo 6.
We make conversations **persistent**: stop now, continue later in
the **same named session** — and learn the right way to continue when the world
has changed.
Covers **Task Statement 1.7 — Manage session state, resumption, and forking.**

---

## What changed since Demo 6

- The agent now **saves its conversation to disk** after every turn, under
  `sessions/<name>.json`.
- You start it with a **session name**, so you can come back to the same case.
- New commands let you **fork** a session and **start fresh with a summary**.
- A helper (`/deliver`) simulates the outside world changing, so we can show
  why a resumed session must be **informed of changes**.

---

## The concepts (in short)

- **Named session** — a saved conversation you can return to. Resuming it is
  the `--resume <session-name>` idea from the Agent SDK.

- **Resume** — continue a saved session. Best when the earlier context is
  **mostly still valid**.

- **Fork (`fork_session`)** — copy a session into a new, **independent** branch,
  so you can try a different direction without changing the original.

- **Start fresh with a summary** — begin a NEW history seeded with only a short
  **summary**, not the old tool results. Best when the old results are **stale**
  (the world changed). A clean summary is more reliable than replaying outdated
  data.

- **Inform of change** — when you resume after something changed, **tell the
  agent what changed** so it re-checks the affected facts instead of trusting
  stale results.

> **The trap (exam favourite):** resuming a session whose old tool results are
> **stale**, without informing the agent — so it answers from out-of-date data.
> See `antipattern_stale_resume.py`.

---

## Choosing how to continue (the key decision)

```
Coming back to an earlier case?
        │
        ├─ context still valid          → RESUME the session
        │
        ├─ something changed             → RESUME + INFORM of the change
        │                                   (agent re-checks affected facts)
        │
        ├─ old results are stale/messy   → START FRESH with a short summary
        │
        └─ want to try another direction → FORK into an independent branch
```

---

## Files

| File | Job |
|------|-----|
| `mock_data.py` | Customers, orders, refund policy; a helper to "deliver" an order. |
| `tools.py` | Simple `get_order` and `get_refund_policy` tools. |
| `session.py` | **The new piece** — save / resume / fork / start-fresh / inform. |
| `agent.py` | **Main demo** — persistent agent; pass a session name; `/fork`, `/fresh`, `/deliver`. |
| `antipattern_stale_resume.py` | The WRONG way: resume with stale results, no re-check. |
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
3. Run the agent **with a session name**:
   ```bash
   python agent.py asha-case
   ```
   Type `quit` (or `exit`) to stop — the session stays saved on disk.

---

## Demo walkthrough — simple steps

### Part A — Resume a named session
1. In your terminal, run: `python agent.py asha-case`
2. At the prompt, type: `What is the status of order ORD-5001?` and press Enter.
3. Read the answer, then type: `quit`
4. Run the same command again: `python agent.py asha-case`
5. Look for the line: `resumed 'asha-case' (... messages restored)` — this proves the session came back.
6. Type a follow-up: `And is that one refundable?` (it remembers ORD-5001 from before.)
7. Type `quit` when done.

### Part B — Fork into an independent branch
1. Start the session again: `python agent.py asha-case`
2. At the prompt, type: `/fork asha-alt`
3. You'll see it create an independent copy named `asha-alt`.
4. To work in the copy, type `quit`, then run: `python agent.py asha-alt`
5. Anything you do in `asha-alt` does **not** change `asha-case`, and vice versa.

### Part C — Resume + inform of a change (the correct way)
1. Start a session: `python agent.py asha-case`
2. Type: `What is the status of order ORD-5005?` (it will say *In Transit*.)
3. Type: `/deliver ORD-5005` (this changes the order to Delivered **and** tells the agent it changed.)
4. Type: `Now can I refund ORD-5005?`
5. Because you informed it, the agent re-checks and answers correctly (now refundable).

### Part D — Start fresh with a summary
1. Inside any running session, type: `/fresh`
2. When it asks for a summary, type something short like: `Customer CUST-1001 (Asha) is asking about refunds for recent orders.`
3. The session restarts from just that summary — no old, stale results carried over.
4. Continue asking questions normally from there.

### Quick reminders
- Type the questions and the `/commands` at the `[asha-case] >` prompt (not in a separate window).
- `quit` or `exit` always stops the agent and saves the session.
- The session name (`asha-case`, `asha-alt`) is just a label you choose — you can pick any name.
- For a minimal recording, **Part A alone** proves the core idea (a conversation that survives across runs). Parts B, C, and D each add one extra concept (fork, inform-of-change, fresh-start).


## See the anti-pattern (stale resume)

```bash
python antipattern_stale_resume.py
```
It resumes a session that still says ORD-5005 is "In Transit", silently marks
the order Delivered, then asks about a refund **without informing the agent**.
Watch it answer from the **old, wrong** status.

- `antipattern_stale_resume.py` → trusts stale results → out-of-date answer.
- `agent.py` (option C above) → informs the agent of the change → correct answer.
