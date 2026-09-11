# Demo 4 — Engineering Workflows: Multi-Concern Decomposition

Fourth demo in **Domain 1: Agentic Architecture & Orchestration**, continuing
Demo 1.3.
In **Demo 4**, the coordinator can handle **multiple requests in a single user message**.

Instead of treating the message as one task, it:
1. Splits the message into separate concerns.
2. Assigns each concern to the right specialist.
3. Combines all the results into one final response.

**Example:**

User says: 
> "Check my order status, update my address, and explain your refund policy."

The coordinator splits this into three tasks:

* Order Status Specialist → Check order status.
* Account Specialist → Update address.
* Policy Specialist → Explain the refund policy.

Finally, it combines all three answers into one response.

------------------------------

## What Changed Since Demo 1.3

* **Demo 1.3:** The coordinator chose a subagent based on its **specialization** (Order, Policy, etc.).

* **Demo 4:** The coordinator first **splits a multi-request message** into separate concerns, then sends each concern to the correct specialist.

* A new **Account Specialist** is added to handle account-related tasks (like reading or updating an address).

* The features from Demo 1.3, such as **Task spawning, parallel execution, and explicit context passing**, are still used behind the scenes.

------------------------------

## The concepts (in short)

- **Concern** — A single request inside a larger message.
Example: "Check my order, update my address, and explain the refund policy."

- **Decomposition** — Breaking one large message into smaller tasks and sending each task to the right specialist.

- **Dependencies** — Some tasks depend on the result of another task.
Example:
First check whether the order was delivered.
Then decide if the customer is eligible for a refund.

- **Unified resolution** — After all specialists finish their work, the coordinator combines everything into one clear response.

- **Two decomposition styles (Task 1.6):**
  - **Prompt chaining (fixed pipeline)** — Tasks always run in the same predefined order. Best when every request follows the same steps.

  - **Dynamic decomposition (adaptive)** — The coordinator first understands the user's message, then decides how many tasks are needed and in what order. Best for unpredictable user requests.

> **The trap (exam favourite):** treating a multi-concern message as **one
> blob** and answering only the first part. See `antipattern_no_decompose.py`.

------------------------------

## The flow (in short)

```
You type ONE message with several concerns
      │
      ▼
COORDINATOR decomposes → concern #1, concern #2, concern #3 (+ dependencies)
      │
      ├─ independent concerns → investigate IN PARALLEL
      │
      ▼
dependent concern → coordinator passes in the facts it needs → investigate
      │
      ▼
COORDINATOR writes ONE unified resolution covering every concern
```

1. You type one message that bundles several requests.
2. `decompose()` splits it into concerns, each with a specialist and an
   optional `depends_on`.
3. Independent concerns run in parallel; dependent ones get prior facts injected.
4. `synthesize()` merges all concern findings into one reply.

---

## Files

| File | Job |
|------|-----|
| `mock_data.py` | Fake "database": customers (with address), orders, policies. |
| `tools.py` | Tools in three groups: **order**, **policy**, **account** (incl. `update_address`). |
| `subagent.py` | `AgentDefinition` + subagent loop; returns structured findings (same as 1.3). |
| `coordinator.py` | **Main demo** — decompose into concerns, investigate each, unify. |
| `antipattern_no_decompose.py` | The WRONG way: treat the message as one blob (drops concerns). |
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
3. Run the multi-concern system and type one message at a time:
   ```bash
   python coordinator.py
   ```
   Type `quit` (or `exit`) to stop.

---

## Prompts to try (copy-paste)

**1. Three concerns (status + refund + address) — the headline demo:**
```
I am CUST-1001. Is ORD-5001 delivered, can I refund it, and please update my address to 99 Park Street, Pune 411002.
```

**2. Two independent concerns (no dependency):**
```
I am CUST-1001. What is your shipping policy, and please update my address to 7 Hill Road, Pune 411004.
```

**3. Two concerns with a dependency (refund needs the status):**
```
I am CUST-1001. Is ORD-5001 delivered, and based on that can I refund it?
```

---

## See the anti-pattern (no decomposition)

This shows the mistake: a bundled message handled as one blob, so concerns get
dropped.

```bash
python antipattern_no_decompose.py
```
Then paste the **same prompt #1** into both files and compare:

- `antipattern_no_decompose.py` → answers the order part; refund + address are dropped.
- `coordinator.py` → decomposes into three concerns and resolves all of them.

```
I am CUST-1001. Is ORD-5001 delivered, can I refund it, and please update my address to 99 Park Street, Pune 411002.
```
