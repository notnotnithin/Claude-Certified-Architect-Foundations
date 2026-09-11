# Demo 3 — Tool Distribution & tool_choice (DocDesk)

Third demo in **Domain 2: Tool Design & MCP Integration**, continuing DocDesk.
Now we have several agents, and the lesson is: **give each agent only the tools
its role needs**, and use **`tool_choice`** to control how tools are called.
Maps to **Task Statement 2.3 — Distribute tools appropriately across agents and
configure tool choice.**

---

## The concepts (short & simple)

**1. Too many tools hurts tool selection.**
An agent with 18 tools chooses worse than one with 4-5. More options = more ways
to pick wrong. Keep each agent's toolset small.

**2. Scope tools to the role.**
Give each agent ONLY the tools its job needs. A Searcher gets search tools; an
Analyzer gets read tools; a Synthesizer gets a small verify tool. If an agent
doesn't have a tool, it can't misuse it.

**3. Agents misuse tools outside their specialty.**
Give a "writer" agent web-search tools and it'll wander off searching. Scoping
prevents this by construction.

**4. Constrained tools beat generic ones.**
Replace a vague generic tool (like a raw `fetch`) with a constrained one (like
`load_document`, which only loads known, validated documents).

**5. A scoped cross-role tool for common needs.**
Sometimes one agent has a frequent small need from another role. Give it a
*narrow* cross-role tool for that — e.g. the Synthesizer gets `verify_fact` for
quick checks — while complex work still routes through the coordinator.

**6. `tool_choice` controls HOW tools are used on a call:**

| `tool_choice` | Meaning | Use it when |
|---------------|---------|-------------|
| `"auto"` | model may call a tool OR just answer | normal (default) |
| `"any"` | model MUST call some tool (no plain text) | you require a tool action |
| `{"type":"tool","name":"X"}` | model MUST call tool **X** | you need a specific tool first |

---

## Before → After

**BEFORE** (`antipattern_all_tools.py`) — ONE agent, **18 tools**, no role:
```
one agent  →  search_documents + load_document + verify_fact   (the 3 real ones)
           +  fetch_url, translate_document, summarize_email,
              delete_document, export_pdf, web_search, ... (15 decoys)
```
This recreates the exam's warning: **18 tools instead of 4-5 degrades selection.**
With a crowded tool list and no role, the agent has to sift 18 options and may
reach for an irrelevant tool (watch for the `❌ DECOY` flag in the output).

**AFTER** (`coordinator.py`) — three SCOPED agents, one tool each:
```
Searcher     →  search_documents      (find relevant docs)
Analyzer     →  load_document         (read them)
Synthesizer  →  verify_fact           (scoped cross-role quick check) → writes answer
```
Each agent chooses from 1 tool, not 18 — so selection is easy and reliable.

---

## How the pipeline works — and where each concept applies

```
You ask a question
      │
      ▼
[Searcher]     forced tool_choice = search_documents        ← Concept 6 (forced)
      │        (guaranteed to search FIRST)                   Concept 2 (scoped: search only)
      ▼
finds relevant document names
      │
      ▼
[Analyzer]     tool_choice = "any"                          ← Concept 6 ("any" = must act)
      │        (guaranteed to actually load a doc)            Concept 2 (scoped: load only)
      ▼                                                       Concept 4 (constrained load_document)
reports key facts
      │
      ▼
[Synthesizer]  tool_choice = "auto"                         ← Concept 6 ("auto")
      │        may use verify_fact if needed                  Concept 5 (scoped cross-role tool)
      ▼
writes the FINAL ANSWER
```

- Each agent is **scoped** (Concepts 1-3): one tool for its role, so selection is
  easy and misuse is impossible.
- `tool_choice` is used deliberately at each step (Concept 6): **forced** to make
  the Searcher search first, **any** to make the Analyzer actually read, **auto**
  to let the Synthesizer verify only if it wants to.
- The Synthesizer's `verify_fact` (Concept 5) is a *narrow* cross-role tool for a
  common need — not full search power.

---

## Files

| File | Job |
|------|-----|
| `documents/` | Sample docs (FAQ, returns policy, spec, warranty). |
| `doc_store.py` | Document backend. |
| `tools.py` | Tools **grouped by role** + a scoped `verify_fact` + constrained `load_document`. |
| `subagent.py` | A scoped agent; supports `tool_choice` (auto / any / forced). |
| `coordinator.py` | **Main demo** — three scoped agents wired into a pipeline. |
| `antipattern_all_tools.py` | **BAD** — one agent with **18 tools** (3 real + 15 decoys), no scoping. |
| `.env.example`, `.gitignore` | Setup helpers. |

`requirements.txt` lives **outside** this folder.

---

## Setup & run

1. Install packages (from the folder with `requirements.txt`):
   ```bash
   pip install -r requirements.txt
   ```
2. Copy the env file and add your key:
   ```bash
   # Windows:  copy .env.example .env
   # mac/Linux: cp .env.example .env
   ```
3. Run:
   ```bash
   python coordinator.py             # GOOD: scoped agents + tool_choice
   python antipattern_all_tools.py   # BAD: one agent, all tools
   ```

---

## Prompts to try (copy-paste)

**1. A two-part question (uses the whole pipeline):**
```
What is the refund window, and is it the same period for warranty claims?
```

**2. A single-fact question:**
```
How long is the warranty on accessories?
```

Run the same question in both files and compare:
- **`coordinator.py`** → clean flow: Searcher (forced) → Analyzer (any) → Synthesizer (auto).
  Watch the `[Searcher]/[Analyzer]/[Synthesizer] uses ...` lines — each only ever
  uses its own tool.
- **`antipattern_all_tools.py`** → one agent juggling all tools; watch it pick
  tools in a less clean order, or reach for a cross-role tool at the wrong time.

---

## What to watch for

- In the good demo, **each agent only ever calls its own tool** — that's scoping
  working. And the `tool_choice` labels (forced / any / auto) show up exactly
  where the coordinator sets them.
- In the bad demo, one agent has **18 tools** and no role. Watch for the
  `❌ DECOY` flag — that's the agent reaching for an irrelevant tool it should
  never need (like `fetch_url` or `translate_document`). Even when it lands on
  the right ones, selection is slower and less predictable with 18 options.

> The lesson: **scope tools to roles for reliable selection, and use
> `tool_choice` to control when a tool must (or must not) be used.**

> Note: a capable model may still muddle through 18 tools on a simple question —
> so the bad demo won't always visibly fail. The point is *reliability at scale*:
> as real systems grow to dozens of tools, an unscoped agent's selection degrades,
> while scoped agents keep choosing from just 1-2 tools no matter how big the
> system gets.
