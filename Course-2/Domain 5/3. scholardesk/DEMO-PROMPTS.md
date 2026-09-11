# Part 2 — Live Demo Guide

### Task 5.2 — Escalation & Ambiguity

---

## Read this first — the map of Part 2

Three scripts, run in cmd. Two call the API (the escalation demos); one runs on its
own (the ambiguity demo). You need your API key (from Part 0) for the two escalation
scripts.

| Step | Where | Task | Needs API key? |
|------|-------|------|----------------|
| Demo 1 | cmd | ◆ **Task 5.2** | ✅ Yes |
| Demo 2 | cmd | ◆ **Task 5.2** | ✅ Yes |
| Demo 3 | cmd | ◆ **Task 5.2** | ❌ No |

Start in the project folder:

```cmd
cd C:\path\to\3. scholardesk
```

Both escalation demos use the **same three questions**, so you can compare directly:
1. an **urgent-sounding but fully-covered** question (running cost per km),
2. a **not-covered** question (5-year resale value — no source mentions it),
3. an **explicit ask for a human expert**.

---

## Demo 1 ◆ Task 5.2 — The anti-pattern: escalate on difficulty/tone

Run the vague version:

```cmd
python escalate_vague.py
```

**What it does:** tells ScholarDesk to escalate if the question *seems hard* or the
user *sounds demanding*.

**What to look for:** the decisions misfire. The urgent-but-covered cost question may
get **escalated** (just because it's phrased forcefully), while the resale-value
question — which **no source covers** — may get **answered with a made-up number**,
because it didn't "seem hard." **Difficulty and tone are unreliable signals** for
whether a question needs a human.

---

## Demo 2 ◆ Task 5.2 — The fix: explicit criteria

Run the criteria version:

```cmd
python escalate_criteria.py
```

**What it does:** same three questions, but now ScholarDesk escalates only on
**explicit triggers**, with few-shot examples marking the boundary:

- the user **explicitly asks for a human expert** → escalate immediately,
- the **sources don't cover** the question (a coverage gap) → escalate,
- ScholarDesk **can't make progress** (e.g. sources conflict unresolvably) → escalate,
- otherwise → **answer** it from the sources — and a forcefully-phrased but covered
  question still just gets answered.

**What to look for:** the decisions now line up with reality:
- urgent-but-covered cost → **ANSWER** (tone doesn't matter),
- resale value (uncovered) → **ESCALATE** (coverage gap),
- "have a human look into this" → **ESCALATE** (explicit request).

The **coverage gap** is the research version of the exam's "policy gap": escalate when
the sources are silent on the question, not just when it feels difficult.

---

## Demo 3 ◆ Task 5.2 — Ambiguity: ask, don't guess

Run the ambiguity demo (no API key needed):

```cmd
python ambiguity.py
```

**What it does:** a user asks "What's the cost?" — but the sources cover **several**
costs: the vehicle's purchase price, the running cost per km, and battery replacement.
The query matches more than one. It shows both responses:

- **Anti-pattern:** guess — pick one meaning (say, purchase price) and answer it. If
  the user meant a different cost, the answer is confidently about the **wrong thing**.
- **Right way:** recognise the ambiguity and **ask which cost they mean**, briefly
  listing the options the sources can answer.

**What to look for:** when one query maps to several distinct answers, the safe move is
to **ask for clarification**, never to pick a meaning by heuristic. One short question
gets it right.

---

## Why this matters (the one-line takeaway)

> **Escalate on real triggers, not on difficulty or tone — and when a query is
> ambiguous, ask instead of guessing.**

---

## Quick recap

| Demo | Task | Script | Shows |
|------|------|--------|-------|
| 1 | ◆ 5.2 | `escalate_vague.py` | Escalating on difficulty/tone misfires |
| 2 | ◆ 5.2 | `escalate_criteria.py` | Explicit triggers + few-shot → correct decisions |
| 3 | ◆ 5.2 | `ambiguity.py` | Ambiguous query → ask which meaning, don't guess |

---

*CCAR-F · Domain 5 · ScholarDesk · ANKIT MISTRY*
