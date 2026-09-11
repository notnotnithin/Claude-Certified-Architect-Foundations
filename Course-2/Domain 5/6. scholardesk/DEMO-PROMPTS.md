# Part 5 — Live Demo Guide

### Task 5.5 — Human Review & Confidence

---

## Read this first — the map of Part 5

Three scripts, run in cmd. Two call the API (the answer demos); one runs on its own
(the accuracy demo). You need your API key (from Part 0) for the two answer scripts.

| Step | Where | Task | Needs API key? |
|------|-------|------|----------------|
| Demo 1 | cmd | ◆ **Task 5.5** | ✅ Yes |
| Demo 2 | cmd | ◆ **Task 5.5** | ✅ Yes |
| Demo 3 | cmd | ◆ **Task 5.5** | ❌ No |

Start in the project folder:

```cmd
cd C:\path\to\6. scholardesk
```

---

## Demo 1 ◆ Task 5.5 — The anti-pattern: no confidence

Run the no-confidence version:

```cmd
python answer_no_confidence.py
```

**What it does:** asks three questions — two clearly answered by the sources, one
("5-year resale value?") the sources **don't cover** — and prints every answer flat,
with no signal about which is risky.

**What to look for:** all three answers go out looking **equally confident**, even the
resale-value one, which isn't in the sources at all. Nobody knows which answer to
double-check, so a shaky answer reaches the user looking just as authoritative as a
solid one.

---

## Demo 2 ◆ Task 5.5 — The fix: confidence + human routing

Run the confidence version:

```cmd
python answer_with_confidence.py
```

**What it does:** same questions, but now ScholarDesk returns a **confidence level**
(high/medium/low) alongside each answer — as structured output via tool use (the
reliable method from Domain 4). A threshold then **routes** the answers: high goes to
the user, anything lower goes to a **human**.

**What to look for:**
- the two clearly-covered questions come back **high** → sent to the user,
- the "resale value" question comes back **low** ("not covered by sources") → **routed
  to human review**, instead of going out looking authoritative.

Human review time is limited, so this spends it only where the assistant itself
flagged uncertainty. That's **calibrated routing**.

---

## Demo 3 ◆ Task 5.5 — One number hides a weak spot

Run the accuracy demo (no API key needed):

```cmd
python accuracy_by_segment.py
```

**What it does:** works from a small labelled set of past answers (already marked
correct/incorrect) and shows accuracy two ways.

**What to look for:**
- **The headline:** `97.3% accurate overall` — looks great, trust it without review!
- **Broken down by topic:** `cost` 99%, `adoption` 98%, but **`charging` just 60%.**
  The one big number **hid** a topic where the assistant is unreliable.

Then it shows **stratified sampling**: instead of spot-checking random answers (which
would mostly land on the biggest topic and barely touch `charging`), it samples a few
from **every** topic — so the weak one can't hide.

---

## Why this matters (the one-line takeaway)

> **Let the assistant flag its own uncertainty, and never trust one aggregate number.**
> Route low-confidence answers to humans, and measure accuracy per segment before
> automating.

---

## Quick recap

| Demo | Task | Script | Shows |
|------|------|--------|-------|
| 1 | ◆ 5.5 | `answer_no_confidence.py` | Every answer looks equally trustworthy |
| 2 | ◆ 5.5 | `answer_with_confidence.py` | Confidence scores → route shaky ones to a human |
| 3 | ◆ 5.5 | `accuracy_by_segment.py` | 97% overall hides a 60% segment; stratified sampling |

---

*CCAR-F · Domain 5 · ScholarDesk · ANKIT MISTRY*
