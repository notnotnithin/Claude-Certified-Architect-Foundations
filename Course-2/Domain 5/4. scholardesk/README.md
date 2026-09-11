# Part 3 — Error Propagation

### Domain 5: Context Management & Reliability · Task 5.3

---

## Where we are

- **Part 2** (`3. scholardesk`) — escalation and ambiguity.
- **Part 3** (`4. scholardesk`, this folder) — when a source **fails to load**, how
  that failure should travel back so the assistant can recover intelligently.

> **Read** in **VS Code**. **Run** in **cmd**. **No API key needed** for this part —
> it's about the *structure* of tool results and recovery logic, which is pure Python.
> Everything runs instantly.

---

## The one big idea of Part 3

> **A failure should carry enough information to recover from it.**

ScholarDesk relies on operations that reach for sources — fetch a document, search the
source set. Those operations fail sometimes. What they return *when they fail* decides
whether the assistant can recover or is left blind.

---

## The anti-pattern: generic errors

`error_generic.py` shows a tool that reports every failure as `"Source error"`. Three
completely different situations —

- a **timeout** (temporary — should retry),
- an **invalid source id** (retrying won't help),
- a **search that found nothing relevant** (not even an error),

— all collapse into the same message. The assistant can't tell them apart, so it can't
do the right thing. It says "something went wrong" even when the real situation was
just "no source covers this."

**The exam's point:** generic error statuses ("search unavailable", "source error")
**hide the context** the assistant needs to recover.

---

## The fix: structured error context

`error_structured.py` returns useful structure for each case:

```
timeout       -> { ok: false, error_type: "transient",  retryable: true,  attempted, message }
bad source id -> { ok: false, error_type: "validation", retryable: false, attempted, message }
no match      -> { ok: true,  results: [] , attempted }
```

Now the assistant recovers correctly:

| Situation | Assistant's move |
|-----------|-----------------|
| `transient` + `retryable` | retry locally |
| `validation` (not retryable) | don't retry — report the bad reference |
| `ok: true, results: []` | report "no source covers this" — a real answer |

Structured context (failure type, retryable flag, attempted operation, partial
results) is what makes intelligent recovery possible.

---

## The crucial distinction: access failure vs valid empty result

This one is worth pausing on, because collapsing it is a classic bug.

- An **access failure** means the search *couldn't run* — a timeout, the source
  service was down. The assistant may need to retry.
- A **valid empty result** means the search *ran perfectly* and found nothing. That's
  a **successful answer** — "no source covers EV resale value" — not a failure. (And,
  per Part 2, exactly the coverage-gap moment to escalate.)

If your tool reports "no relevant source" the same way it reports "source service
down," the assistant will treat a perfectly good answer as an error (or a real error
as an empty answer). Keep them distinct.

---

## Local recovery, and honest coverage gaps

`local_recovery.py` shows the last pieces.

**Recover locally first.** When a failure is **transient**, retry a couple of times
right where it happened, before propagating anything. The user never sees a brief blip.

**Annotate gaps instead of hiding them.** When a source genuinely can't be reached
after retries, don't abandon the whole task and don't pretend the source was empty.
Finish with the sources you have, and **mark the coverage**: which topics are
well-supported, and where there's a gap because a source was unavailable.

```
[well-supported] EV adoption figures   (source: ev_adoption_report.txt)
[well-supported] running costs          (source: ev_cost_brief.txt)
[GAP]            charging infrastructure - could not be covered (source unavailable)
```

This avoids three anti-patterns at once: **terminating the task** on the first
hiccup, **hiding the error silently**, and **pretending a missing source was empty**.
Coverage annotations are the exam's recommended way to keep synthesis honest about
what it could and couldn't support — and they fit a research assistant naturally.

---

## The demo

```cmd
python error_generic.py      # "Source error" -> assistant blind
python error_structured.py   # structured context -> right recovery
python local_recovery.py     # retry transient failures; annotate coverage gaps
```

Full walkthrough in **`DEMO-PROMPTS.md`**.

---

## Your folder layout

```
4. scholardesk/
├── error_generic.py        ← NEW: ❌ generic, contextless errors
├── error_structured.py     ← NEW: ✅ structured error context
├── local_recovery.py       ← NEW: local retry + coverage annotations
├── DEMO-PROMPTS.md, README.md
├── scholardesk/, sources/  ← unchanged
├── requirements.txt, .env.example, .gitignore
```

---

## Exam objective coverage

**◆ Task 5.3 — Implement error propagation strategies across multi-agent systems**

- ✅ Structured error context (failure type, attempted query, partial results,
  alternatives) enables recovery: `error_structured.py`.
- ✅ Access-failure vs valid-empty-result distinction: the `no_match` case
  (`ok: true, results: []`) vs the timeout.
- ✅ Generic error statuses hide context: `error_generic.py`.
- ✅ Silently suppressing errors, or terminating on a single failure, are both
  anti-patterns: covered in `local_recovery.py` and the README.
- ✅ Returning structured error context: the structured tool results.
- ✅ Distinguishing access failures from valid empty results: the dedicated section.
- ✅ Local recovery for transient failures before propagating: `local_recovery.py`.
- ✅ Structuring synthesis with coverage annotations (well-supported vs gaps):
  the coverage-annotation part of `local_recovery.py`.

---

## What's next

**Part 4 — Large codebase exploration (Task 5.4).** A change of tool: this part uses
**Claude Code**, not the API. We'll explore ScholarDesk's own code the way you'd
explore a big unfamiliar codebase — using scratchpad files, subagents, and `/compact`
to keep context from degrading over a long session.

See you in Part 4.

---

*CCAR-F · Domain 5 · Part 3 — ANKIT MISTRY*
