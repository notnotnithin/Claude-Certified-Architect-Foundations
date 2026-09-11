# Demo 1.3 — Context Sharing & Spawning (Smart Order Support Assistant)

Third demo in **Domain 1: Agentic Architecture & Orchestration**, continuing
Demo 1.2.
The coordinator now **spawns** subagents the way the Agent SDK does,
**passes context** between them explicitly, and runs independent subagents
**in parallel**.
Maps to **Task Statement 1.3 — Configure subagent invocation, context passing,
and spawning.**

------------------------------

# What Changed Since Demo 1.2

In **Demo 1.2**, the coordinator acted like a **manager** who assigned work to employees (subagents), collected their answers, and combined them into the final result.
In **Demo 1.3**, the workflow became smarter with the following improvements:

## 1. Task Tool (`spawn_task`)
Instead of talking to employees directly, the manager now creates an **official task** for each employee using the **Task** tool (`spawn_task`).

**Example:**
* **Demo 1.2:** Manager → Employee
* **Demo 1.3:** Manager → Task → Employee

This makes task assignment more organized and consistent.

---

## 2. Explicit Context Passing

Sometimes one employee needs information discovered by another employee.
Instead of expecting employees to remember previous conversations, the manager copies the required information into the new task.

**Example:**

* Employee A finds that **"The CEO of Apple is Tim Cook."**
* Employee B is asked to write a summary.
* The manager includes **"The CEO of Apple is Tim Cook"** in Employee B's task.

This ensures every employee has the information they need.

---

## 3. Parallel Spawning

If multiple employees have independent work, they don't need to wait for each other.
The manager assigns all their tasks at the same time.

**Example:**

* Employee A researches Apple.
* Employee B researches Microsoft.
* Employee C researches Google.

All three work **in parallel**, making the overall process much faster.

---

## Other Improvements

### AgentDefinition

Instead of creating every employee from scratch, we now use an **AgentDefinition**.

Think of it as a **job description** that defines an employee's role, tools, and instructions. Whenever we need that type of employee, we simply reuse the same definition.

### Structured Findings

Previously, an employee returned only an answer.

Now, each employee returns:

* A **summary** of what they found.
* The **sources** they used.

This helps the coordinator know exactly **where each piece of information came from**, making the final answer more reliable.


---------------------------------------


## The concepts (in short)

- **`AgentDefinition`** — a reusable spec for a subagent: name, description,
  system prompt, and allowed tools. (See `subagent.py`.)
  Think of it as a job description for a subagent. It defines the agent's role, instructions, and the tools it can use.

- **`Task` tool** — the mechanism a coordinator uses to spawn a subagent. The
  coordinator must have `"Task"` in its `allowedTools` (we list it explicitly).
  The coordinator uses the Task tool to assign work to a subagent. It cannot create subagents directly.

- **Isolated context** — subagents do **not** inherit the coordinator's memory
  or each other's results. Each subagent starts a fresh conversation.
Every subagent starts with a clean slate. It does not automatically know what the coordinator or other subagents know.

- **Explicit context passing** — because of isolation, the coordinator must
  **copy** any needed facts INTO the next subagent's task text. Nothing is
  shared automatically.
If a subagent needs information from another subagent, the coordinator must include that information in the new task.

- **Structured findings (content + metadata)** — a subagent returns a
  `summary` plus `sources` (which tools/IDs it used), so the coordinator always
  knows where each fact came from.
Instead of returning only an answer, a subagent returns a summary along with the sources it used.

- **Parallel spawning** — independent subtasks are spawned together (multiple
  `Task` calls at once) and run at the same time.
Independent subagents can work at the same time, making the workflow faster.

- **Goal-oriented tasks** — the coordinator tells a subagent *what to find*,
  not step-by-step *how* — so the subagent can adapt.
The coordinator tells a subagent what to achieve, not how to do it. The subagent decides the best approach.

> **The trap (exam favourite):** assuming subagents **share memory**. If the
> coordinator forgets to pass prior findings into a dependent task, the next
> subagent simply doesn't have them. See `antipattern_no_context.py`.
Don't assume subagents share memory. If the coordinator doesn't pass important information, the next subagent won't know it.

---------------------------------------

## The flow (in short)

```
You type a question
      │
      ▼
COORDINATOR plans → which subagents? which are independent vs dependent?
      │
      ├─ INDEPENDENT tasks → spawn IN PARALLEL  (run at the same time)
      │
      ▼
DEPENDENT task → coordinator INJECTS prior findings into its task text
      │            (explicit context passing)
      ▼
spawn the dependent subagent → it now has the facts it needs
      │
      ▼
COORDINATOR combines structured findings → one final answer
```

1. You type one question.
2. `make_plan()` splits it into `parallel` (independent) and `dependent` tasks.
3. `spawn_parallel()` runs independent subagents at the same time.
4. For a dependent task, the coordinator copies earlier findings into the task
   text, then `spawn_task()` runs it.
5. `synthesize()` merges the structured findings into one reply.

---

## Files

| File | Job |
|------|-----|
| `mock_data.py` | Fake "database": customers, orders, refund + shipping policy. |
| `tools.py` | Tools grouped by role: **order** tools and **policy** tools. |
| `subagent.py` | `AgentDefinition` + the subagent loop; returns **structured findings**. |
| `coordinator.py` | **Main demo** — `Task` tool, parallel spawning, explicit context passing. |
| `antipattern_no_context.py` | The WRONG way: not passing context to a dependent subagent. |
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
3. Run the multi-agent system and type one question at a time:
   ```bash
   python coordinator.py
   ```
   Type `quit` (or `exit`) to stop.

---

## Prompts to try (copy-paste)

**1. Parallel spawning — two INDEPENDENT lookups run at the same time:**
```
Compare orders ORD-5001 and ORD-5003 for customer CUST-1001.
```

**2. Explicit context passing — the refund decision DEPENDS on the order status:**
```
I am CUST-1001. Is ORD-5001 delivered, and based on that can I refund it?
```

**3. Mix — independent shipping question + dependent refund decision:**
```
I am CUST-1001. What is your shipping policy, and can I refund ORD-5001 based on its status?
```

---

## See the anti-pattern (subagents don't share memory)

This shows the #1 context mistake the exam tests: a dependent subagent never
receives the facts it needs, because they weren't passed in.

```bash
python antipattern_no_context.py
```
Then paste the **same prompt #2** into both files and compare:

- `antipattern_no_context.py` → the Policy Specialist can't decide; it has no order facts.
- `coordinator.py` → the order status is passed in, so the refund decision is correct.

```
I am CUST-1001. Is ORD-5001 delivered, and based on that can I refund it?
```
