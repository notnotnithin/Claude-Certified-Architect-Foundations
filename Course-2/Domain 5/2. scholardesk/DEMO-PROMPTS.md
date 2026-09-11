# Part 1 — Live Demo Guide

### Task 5.1 — Context Management

---

## Read this first — the map of Part 1

Three scripts, run in cmd. Two call the API (the research demos); one runs on its own
(the trimming demo). You need your API key (from Part 0) for the two research scripts.

| Step | Where | Task | Needs API key? |
|------|-------|------|----------------|
| Demo 1 | cmd | ◆ **Task 5.1** | ✅ Yes |
| Demo 2 | cmd | ◆ **Task 5.1** | ✅ Yes |
| Demo 3 | cmd | ◆ **Task 5.1** | ❌ No |

Start in the project folder:

```cmd
cd C:\path\to\2. scholardesk
```

---

## Demo 1 ◆ Task 5.1 — The anti-pattern: findings summarised away

Run the lossy version:

```cmd
python research_lossy.py
```

**What it does:** imagines a long research session, but carries forward only a vague
**summary** ("EVs are cheaper to run, charging is in big cities") instead of the real
figures. Then a follow-up asks for the **exact per-km costs and the source**.

**What to look for:** ScholarDesk **can't answer**. The exact figures, the document
name, and the date were summarised away, so it has to admit it lost them. That's the
danger of **progressive summarisation** — it quietly deletes the numbers and citations
research depends on.

---

## Demo 2 ◆ Task 5.1 — The fix: a persistent "findings" block

Run the findings version:

```cmd
python research_findings.py
```

**What it does:** same session, but the hard facts — `Rs 0.25/km` vs `Rs 2.50/km`, the
`Rs 1.10 lakh` price, the `2 million` sales figure, each with its **source and date** —
are kept **verbatim** in a `KEY FINDINGS` block that rides along in every prompt. The
narrative can be summarised; the facts never are.

**What to look for:** ScholarDesk now answers **exactly** — the figures, the source,
the date. Two ideas work together:

1. **Keep hard facts in a persistent block** (never summarise figures, dates, sources).
2. **Put that block first.** Models read the **beginning and end** of a long input most
   reliably and can miss the **middle** — the "lost in the middle" effect. So the most
   important facts go at the top.

---

## Demo 3 ◆ Task 5.1 — Trim a verbose source

Run the trimming demo (no API key needed):

```cmd
python trim_source.py
```

**What it does:** shows a realistic fetched source wrapped in **noise** — nav bars,
a cookie banner, an advert, "related articles," a footer — when only **one sentence**
answers the question. It then trims it to that relevant excerpt.

**What to look for:** the raw fetch is ~900 characters of mostly boilerplate; the
trimmed excerpt is ~130. In a long session pulling many sources, those dumps pile up
and bury the useful content. **Trim each source to the relevant excerpt before it
enters the session.**

---

## Why this matters (the one-line takeaway)

> **Protect the facts, and protect the space.** Keep exact figures/dates/sources in a
> persistent block at the top, and trim bloated sources before they crowd the context.

---

## Quick recap

| Demo | Task | Script | Shows |
|------|------|--------|-------|
| 1 | ◆ 5.1 | `research_lossy.py` | Summarising away findings → can't cite |
| 2 | ◆ 5.1 | `research_findings.py` | Persistent findings block, placed first → exact answer |
| 3 | ◆ 5.1 | `trim_source.py` | Trimming a noisy source to the relevant excerpt |

---

*CCAR-F · Domain 5 · ScholarDesk · ANKIT MISTRY*
