# Demo 1 — Tool Descriptions & Disambiguation (DocDesk)

First demo in **Domain 2: Tool Design & MCP Integration**. We start a new
evolving project, **DocDesk** — an assistant that answers questions about a
small set of local documents. This demo is all about **tool descriptions**:
the text the model reads to decide which tool to call.
Maps to **Task Statement 2.1 — Design effective tool interfaces with clear
descriptions and boundaries.**

---

## The concepts (short & simple)

**1. The model chooses a tool by reading its description.**
The description is the single most important part of a tool. If it's unclear,
the model picks the wrong tool.

**2. Vague descriptions cause misrouting.**
"Analyzes a document." tells the model nothing, so it can't choose reliably.

**3. Overlapping descriptions make the model guess.**
Two tools that sound the same (like `analyze_content` vs `analyze_document`)
give the model no way to tell them apart — it picks almost at random.

**4. A generic tool is unpredictable — so split it.**
One tool that tries to extract, summarize, AND verify is a black box. Split it
into small, purpose-specific tools, each with a clear job.

**5. A good description states four things:**
what it does · the input format · an example · when to use it vs a similar tool.

**6. System-prompt wording can override descriptions.**
A keyword in the system prompt (e.g. "always analyze") can bias tool choice
even when a different tool fits better. Keep the prompt neutral unless you mean
to steer.

---

## Before → After (the heart of this demo)

**BEFORE** (`antipattern_tools.py`) — vague and overlapping:

```
analyze_content    "Analyzes content."     ← says nothing
analyze_document   "Analyzes a document."  ← sounds identical
get_document       "Gets a document."      ← search? read? unclear
```
The model can't tell these apart, and the user's real intent (extract vs
summarize vs verify) is lost.

**AFTER** (`tools.py`) — one generic tool split into clear, purpose-specific tools:

```
analyze_document  ✗  (vague: extract? summarize? verify?)
      │ split into
      ▼
extract_data_points          → pull specific facts (prices, dates, windows)
summarize_content            → give the gist of a document
verify_claim_against_source  → check if a claim is true against a document
```
Plus two clearly-separated helpers: `search_documents` (find WHICH document)
and `read_document` (read ONE document you already know).

---

## How the agent works — and where each concept applies

```
You ask a question
      │
      ▼
[1] Model reads ALL tool DESCRIPTIONS         ← Concept 1: descriptions drive choice
      │
      ▼
[2] Model PICKS a tool that matches your goal ← Concepts 2–4: clear vs vague/overlapping
      │                                          decides whether this pick is right
      ▼
[3] Agent RUNS that tool  → prints "TOOL CHOSEN: ..."   ← watch this line
      │
      ▼
[4] Tool returns the document text
      │
      ▼
[5] (loop) Model may pick another tool, or finish        ← stop_reason drives the loop
      │
      ▼
[6] Model writes the final ANSWER from the document
```

- Steps **1–2** are the whole lesson: with **good** descriptions the model picks
  the tool that matches your intent (extract / summarize / verify). With **bad**
  descriptions it can only choose between look-alike `analyze_*` tools, so the
  pick is unreliable.
- Step **3** ("TOOL CHOSEN") is where you SEE the concept working — run the same
  question with good vs bad tools and compare this line.
- The loop in step **5** (drive on `stop_reason`) is the same agentic loop from
  Domain 1 — unchanged. Here the focus is the tools, not the loop.

---

## Files

| File | Job |
|------|-----|
| `documents/` | The sample documents DocDesk answers from (FAQ, returns policy, spec). |
| `doc_store.py` | Loads/searches the documents (DocDesk's little backend). |
| `tools.py` | **GOOD** tools — clear, split, differentiated descriptions (the AFTER). |
| `antipattern_tools.py` | **BAD** tools — vague, overlapping, generic (the BEFORE). |
| `agent.py` | **Main demo** — loads good tools by default, or bad tools with `--bad`. |
| `.env.example` | Template for your API key — copy it to `.env`. |
| `.gitignore` | Keeps your real `.env` out of version control. |

`requirements.txt` lives **outside** this folder (one level up).

---

## Setup & run

1. Install packages (from the folder that has `requirements.txt`):
   ```bash
   pip install -r requirements.txt
   ```
2. Create your key file and paste your key into it:
   ```bash
   # Windows (PowerShell):    copy .env.example .env
   # macOS / Linux / WSL:     cp .env.example .env
   ```
   Then edit `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-...your-real-key...
   ```
3. Run with the GOOD tools:
   ```bash
   python agent.py
   ```
   Run with the BAD tools (to see misrouting):
   ```bash
   python agent.py --bad
   ```
   Type `quit` (or `exit`) to stop.

---

## Prompts to try (copy-paste)

Ask the **same** three questions in both modes and watch the `TOOL CHOSEN` line.

**1. A specific-fact question (should route to `extract_data_points`):**
```
What is the refund window? Pull the exact number of days from the returns policy.
```

**2. A summary question (should route to `summarize_content`):**
```
Give me a short summary of the returns policy.
```

**3. A true/false question (should route to `verify_claim_against_source`):**
```
Is it true that In Transit orders can be refunded? Check the returns policy.
```

**With `tools.py` (good):** each question routes to the matching purpose-specific tool.
**With `--bad`:** the model can only pick between `analyze_content` / `analyze_document` /
`get_document`, which all sound the same — so selection is unreliable and the
intent (extract vs summarize vs verify) is lost.

> Tip: because the model is smart, the **bad** tools may *sometimes* still work.
> That inconsistency across runs IS the lesson — vague descriptions mean you're
> relying on luck, not design.

---

## Bonus: system-prompt keyword sensitivity

Open `agent.py`, find `SYSTEM_PROMPT`, and add a keyword like
"always analyze the document first". Re-run and watch how one word can bias the
model toward an "analyze" tool even when another tool fits better. That's why
system-prompt wording matters as much as tool descriptions.
