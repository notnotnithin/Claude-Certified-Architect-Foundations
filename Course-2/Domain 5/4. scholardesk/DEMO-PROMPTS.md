# Part 3 — Live Demo Guide

### Task 5.3 — Error Propagation

---

## Read this first — the map of Part 3

Three scripts, run in cmd. **None of them need an API key** — this part is about the
*structure* of tool results and recovery logic, which is pure Python. So it all runs
instantly, no key required.

| Step | Where | Task | Needs API key? |
|------|-------|------|----------------|
| Demo 1 | cmd | ◆ **Task 5.3** | ❌ No |
| Demo 2 | cmd | ◆ **Task 5.3** | ❌ No |
| Demo 3 | cmd | ◆ **Task 5.3** | ❌ No |

Start in the project folder:

```cmd
cd C:\path\to\4. scholardesk
```

---

## Demo 1 ◆ Task 5.3 — The anti-pattern: generic errors

Run the generic version:

```cmd
python error_generic.py
```

**What it does:** simulates a source tool that reports **every** failure the same lazy
way — `"Source error"` — across three very different situations: a timeout, an
invalid source id, and a search that simply found nothing relevant.

**What to look for:** all three collapse into the same useless message. The assistant
is **blind** — it can't tell a temporary timeout (retry it!) from a bad source id
(don't retry) from an empty search (which isn't even an error). So it just says
"something went wrong" and can't recover.

---

## Demo 2 ◆ Task 5.3 — The fix: structured error context

Run the structured version:

```cmd
python error_structured.py
```

**What it does:** the same three situations, but each comes back as **structured**
information — a failure `type`, a `retryable` flag, the `attempted` operation, a clear
message. And the empty search returns `ok: True` with an empty result list.

**What to look for:** now the assistant makes the **right move** for each:

| Situation | Structured result | Assistant's move |
|-----------|-------------------|-----------------|
| Timeout | `type: transient, retryable: true` | retry locally |
| Bad source id | `type: validation, retryable: false` | don't retry — report the bad reference |
| No match | `ok: true, results: []` | report "no source covers this" — a real answer |

The **crucial distinction** is the last one: an **access failure** (the search couldn't
run) is completely different from a **valid empty result** (the search ran fine and
found nothing). Collapsing those two is a classic bug — "no relevant source" is a
useful answer (and, per Part 2, a good moment to escalate), not a failure.

---

## Demo 3 ◆ Task 5.3 — Local recovery + coverage gaps

Run the recovery version:

```cmd
python local_recovery.py
```

**What it does:** two things.
1. A flaky source fails twice, then works — a local retry loop absorbs the transient
   failures **quietly**, so the user never sees a hiccup.
2. Then it shows what to do when a source genuinely **can't** be reached: don't
   abandon the whole task or hide the gap — finish with the sources you have, and
   **annotate the coverage**, marking which topics are well-supported and which have a
   gap.

**What to look for:** the transient failures are handled locally; and the final
synthesis clearly marks `[well-supported]` topics versus a `[GAP]` where a source
stayed unavailable. This avoids three anti-patterns: **killing the task** on one blip,
**hiding the error silently**, and **pretending a missing source was empty**.

---

## Why this matters (the one-line takeaway)

> **Tell the truth about failures — with structure.** A failure type lets the
> assistant retry, skip, or report correctly; "found nothing" is a valid answer; and a
> gap should be marked, not hidden.

---

## Quick recap

| Demo | Task | Script | Shows |
|------|------|--------|-------|
| 1 | ◆ 5.3 | `error_generic.py` | "Source error" hides everything → assistant blind |
| 2 | ◆ 5.3 | `error_structured.py` | Structured context → right recovery; access-fail vs empty-result |
| 3 | ◆ 5.3 | `local_recovery.py` | Retry transient failures locally; annotate coverage gaps |

---

*CCAR-F · Domain 5 · ScholarDesk · ANKIT MISTRY*
