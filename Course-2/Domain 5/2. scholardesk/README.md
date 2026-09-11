# Part 1 — Context Management

### Domain 5: Context Management & Reliability · Task 5.1

---

## Where we are

- **Part 0** (`1. scholardesk`) — set up ScholarDesk and asked a question of one
  source.
- **Part 1** (`2. scholardesk`, this folder) — keeping the **important findings alive**
  across a long research session, and keeping the context **uncluttered**.

Part 0's app is unchanged. Part 1 adds three small scripts.

> **Read** in **VS Code**. **Run** in **cmd**. The two research demos need your API key
> (Part 0); the trimming demo doesn't.

---

## The one big idea of Part 1

> **In a long research session, the facts get lost — unless you protect them.**

A research session runs for many turns across several sources. As it grows, two
problems appear:

1. **Findings get summarised away.** To save space, people compress the session so
   far into a vague summary — and the exact figures, dates, and source names vanish
   with it.
2. **Sources arrive bloated.** A fetched page or long report drags in nav bars, ads,
   and footers, burying the few sentences that matter.

Part 1 fixes both. That's Task 5.1.

---

## Problem 1 — progressive summarisation destroys findings

Watch `research_lossy.py`. A long session is carried forward as a summary:

> "EVs are selling well and are cheaper to run. Charging is mostly in big cities."

Then a follow-up asks: *"what were the exact per-km figures, and which source and
date?"* ScholarDesk **can't answer** — the specific `Rs 0.25/km` vs `Rs 2.50/km`, the
document name, and the date `2026-01-20` were all summarised into mush.

**The exam's point:** progressive summarisation quietly condenses numbers,
percentages, dates, and stated details into vague summaries — exactly the things a
research tool can't afford to lose, because it needs them to **cite**.

---

## Fix 1 — a persistent "key findings" block

`research_findings.py` keeps the hard facts **verbatim** in a block that rides along
in every prompt, each fact tagged with its source and date:

```
KEY FINDINGS (verified, do not alter):
- EV two-wheeler running cost: Rs 0.25/km; petrol: Rs 2.50/km
  [source: EV Ownership Cost Brief, 2026-01-20]
- India EV sales 2025-26: crossed 2 million units
  [source: India EV Adoption Report, 2026-03-10]
- Pune public charging points: ~350 as of early 2026
  [source: Public Charging Note, 2026-02-05]
```

The narrative can still be summarised — that part is fine to compress. But the
**hard findings** (figures, dates, source names) live in a fixed block that is
**never** condensed. Now ScholarDesk answers exactly, no matter how long the session
runs.

> Notice the findings block already carries **source names and dates**. That habit
> pays off directly in Part 6, where provenance — which source said what, and when —
> is the whole lesson.

---

## The "lost in the middle" effect — and where to put the block

There's a second reason the findings block matters: **position**.

Models read the **beginning and end** of a long input most reliably, and are most
likely to **miss things in the middle** — the "lost in the middle" effect. So we
don't just keep the facts, we put them **first**, in the most reliably-read position.
(Clear section headers help too, so the model can find each part.)

---

## Problem 2 & Fix 2 — trim verbose sources

`trim_source.py` shows a fetched source wrapped in noise — a nav bar, cookie banner,
advert, "related articles," and a footer — when a **single sentence** answers the
question.

Dropping the whole thing into context wastes tokens and buries the useful sentence.
The fix is to **trim each source to the relevant excerpt before it enters the
session**:

```
~900 characters of boilerplate  ->  ~130 characters that actually answer the question
```

Across a long session pulling many sources, trimming is the difference between a
focused context and one clogged with nav bars and footers.

---

## The demo

```cmd
python research_lossy.py      # findings summarised away -> can't cite
python research_findings.py   # persistent findings block, placed first -> exact answer
python trim_source.py         # trim a noisy source to the relevant excerpt (no API key)
```

Full walkthrough in **`DEMO-PROMPTS.md`**.

---

## Your folder layout

```
2. scholardesk/
├── research_lossy.py       ← NEW: ❌ findings lost to summarisation
├── research_findings.py    ← NEW: ✅ persistent key-findings block
├── trim_source.py          ← NEW: trim verbose sources
├── DEMO-PROMPTS.md, README.md
├── scholardesk/            ← unchanged (ask.py, _shared.py)
├── sources/                ← unchanged (three EV sources)
├── requirements.txt, .env.example, .gitignore
```

---

## Exam objective coverage

**◆ Task 5.1 — Manage conversation context to preserve critical information**

- ✅ Progressive summarisation risks (condensing numbers, dates, details):
  `research_lossy.py`.
- ✅ "Lost in the middle" — models read beginning/end reliably, may omit the middle:
  the positioning section; findings block placed first.
- ✅ Verbose inputs accumulate and consume tokens disproportionately: `trim_source.py`.
- ✅ Extracting transactional facts (figures, dates, source names) into a persistent
  block in each prompt: `research_findings.py`.
- ✅ Trimming verbose outputs to only relevant content: `trim_source.py`.
- ✅ Placing key findings at the beginning + section headers to mitigate position
  effects: the KEY FINDINGS block is placed first, with a clear header.

---

## What's next

**Part 2 — Escalation & ambiguity (Task 5.2).** ScholarDesk can't (and shouldn't)
answer everything itself. We give it explicit criteria for **when to escalate to a
human expert** — for example, when the sources genuinely don't cover the question, or
when they conflict in a way it can't resolve — versus answering on its own.

See you in Part 2.

---

*CCAR-F · Domain 5 · Part 1 — ANKIT MISTRY*
