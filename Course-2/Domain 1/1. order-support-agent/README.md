# Demo 1.1 — Single Agent (Smart Order Support Assistant)

First demo in **Domain 1: Agentic Architecture & Orchestration**.
We build one AI agent for a fictional store, **PyStack Mart**, with a correct **agentic loop**.
Maps to **Task Statement 1.1 — Design and implement agentic loops.**

---

## The concepts (in short)

- **Agent** — not a one-shot chatbot. It can *take actions* (call tools) to
  fetch real data before answering, and repeat until the job is done.

- **Tool** — something the agent can do. Each tool has a **schema** (a
  description the agent reads to pick the tool) and a **function** (the code
  that runs). Good, detailed descriptions = reliable tool selection.

- **Agentic loop** — the repeating cycle: send conversation → check the
  result → maybe run a tool → send again → ... → stop.

- **`stop_reason`** — the one signal that drives the loop. The agent's reply
  always includes it:
  - `"tool_use"` → the agent wants a tool. Run it, add the result, **loop again**.
  - `"end_turn"` → the agent is finished. **Stop** and show the answer.
  
- **Conversation history** — the agent has no memory of its own, so we pass
  the *whole* conversation (question + replies + tool results) every time.

> **Golden rule:** decide whether to keep looping by checking `stop_reason` —
> never by reading the agent's text. (See `antipattern_loop.py` for the wrong way.)

---

## The flow (in short)

```
You type a question
      │
      ▼
Send conversation to the agent ──────────┐
      │                                   │
      ▼                                   │
Look at stop_reason                       │
      │                                   │
      ├─ "tool_use"  → run tool(s) →      │
      │                add results ───────┘  (loop again)
      │
      └─ "end_turn"  → print final answer → done
```

1. You type one question.
2. `run_agent()` sends it to Claude.
3. If `stop_reason` is `"tool_use"`, the code runs the requested tool(s),
   appends the results, and loops.
4. If `stop_reason` is `"end_turn"`, the loop ends and prints the answer.
5. You're prompted for the next question.

---

## Files

| File | Job |
|------|-----|
| `mock_data.py` | Fake "database": customers, orders, refund policy. |
| `tools.py` | The 3 tools + their schemas (descriptions). |
| `agent.py` | **Main demo** — the single agent and its `stop_reason` loop. |
| `antipattern_loop.py` | The WRONG way to stop the loop (teaching contrast). |
| `requirements.txt` | Packages: `anthropic`, `python-dotenv`. |
| `.env.example` | Template for your API key — copy it to `.env`. |

---


### Try these prompts

- `Can you tell me the status of my order ORD-5003?`
- `I am customer CUST-1001. Can I get a refund for ORD-5001?`

### See the anti-pattern (optional)

```bash
python antipattern_loop.py
```
antipattern_loop.py exists to show you the WRONG way to build the loop — on purpose — so you understand why the right way matters.
- run python antipattern_loop.py then try prompt
- run python agent.py then try prompt same prompt (see the difference)

Choose 1 or 2 to run one of two broken loops:

1 — stop on any text: quits the moment the model writes anything, so it can stop before a tool runs.
2 — stop on a "done" phrase: loops until the model's text contains a word like "done" — unreliable because the model's wording changes every run.

# prompt to try
- I am customer CUST-1001. Can I get a refund for order ORD-5001?
