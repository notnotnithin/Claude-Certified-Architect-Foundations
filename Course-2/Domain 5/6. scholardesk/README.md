# Part 5 — Human Review & Confidence

### Domain 5: Context Management & Reliability · Task 5.5

---

## Where we are

- **Part 4** (`5. scholardesk`) — codebase exploration (the Claude Code sidebar).
- **Part 5** (`6. scholardesk`, this folder) — **back to the API.** Teaching ScholarDesk
  to know when it's unsure, and measuring where it's actually reliable.

> **Read** in **VS Code**. **Run** in **cmd**. The two answer demos need your API key
> (Part 0); the accuracy demo doesn't.

---

## The one big idea of Part 5

> **Know what you don't know — and check where you're actually weak.**

Two halves:

1. **Confidence + routing** — the assistant rates its confidence, and low-confidence
   answers go to a human instead of straight to the user.
2. **Segment accuracy** — one overall accuracy number can hide a weak spot; you have to
   measure per segment before trusting the assistant to run unreviewed.

---

## Half 1 — confidence and human routing

`answer_no_confidence.py` sends every answer out flat. A question the sources don't
cover ("5-year resale value?") goes out looking just as authoritative as a solid,
well-supported answer. Nobody can tell which to check.

`answer_with_confidence.py` fixes this. The assistant returns a **confidence level**
with each answer — as structured output via tool use (Domain 4's reliable method) — and
a threshold routes them:

| Confidence | Route |
|-----------|-------|
| high | → sent to the user |
| medium / low | → **routed to human review** |

Now the "resale value" answer comes back **low** and goes to a human, while the two
clearly-covered questions go straight out. Human reviewers are a limited resource, so
this spends their attention only where the assistant itself flagged uncertainty. That's
**calibrated routing** — and the confidence levels themselves would, in a real system,
be **calibrated against a labelled validation set** so that "high" genuinely means
"usually correct."

---

## Half 2 — one number hides a weak spot

This is the part the exam stresses most.

`accuracy_by_segment.py` shows a labelled evaluation set scored two ways:

- **Overall: 97.3%.** Looks excellent — you might trust it without review.
- **By topic:**

  | Topic | Accuracy |
  |-------|----------|
  | cost | 99.3% |
  | adoption | 98.0% |
  | charging | **60.0%** ← weak spot |

The single aggregate number **hid** a topic where the assistant is unreliable. If you'd
trusted the 97%, you'd have automated `charging` questions too — and been wrong 4 times
out of 10 there.

**The lesson:** measure accuracy **per segment** (by topic, by field) before automating
anything. An aggregate metric can mask poor performance on a specific type or field.

---

## Stratified sampling — so the weak segment can't hide

How do you check accuracy without hand-reviewing everything? You **sample**. But plain
random sampling has a trap: it draws mostly from the **biggest** topic (here, `cost`)
and might barely touch `charging` — so the weak spot stays hidden.

**Stratified sampling** fixes this: sample a few from **each** topic, so every segment
actually gets looked at. `accuracy_by_segment.py` demonstrates it — every topic gets
sampled, regardless of its size. This is how you measure error rates in high-confidence
answers without missing a small-but-weak segment.

---

## The demo

```cmd
python answer_no_confidence.py     # every answer looks equally trustworthy
python answer_with_confidence.py   # confidence -> route shaky answers to a human
python accuracy_by_segment.py      # 97% hides a 60% segment; stratified sampling (no API)
```

Full walkthrough in **`DEMO-PROMPTS.md`**.

---

## Your folder layout

```
6. scholardesk/
├── answer_no_confidence.py     ← NEW: ❌ trust every answer equally
├── answer_with_confidence.py   ← NEW: ✅ confidence + route to human
├── accuracy_by_segment.py      ← NEW: aggregate hides weak segment; stratified sampling
├── DEMO-PROMPTS.md, README.md
├── scholardesk/, sources/      ← unchanged
├── requirements.txt, .env.example, .gitignore
```

---

## Exam objective coverage

**◆ Task 5.5 — Design human review workflows and confidence calibration**

- ✅ Aggregate accuracy metrics may mask poor performance on specific topics/fields:
  `accuracy_by_segment.py` (97% overall hides 60% segment).
- ✅ Stratified random sampling for measuring error rates: the stratified-sampling
  section of `accuracy_by_segment.py`.
- ✅ Field-level confidence scores calibrated using labelled validation sets:
  `answer_with_confidence.py` outputs confidence; the README explains calibration.
- ✅ Validating accuracy by topic and field before automating: the per-topic breakdown.
- ✅ Outputting confidence scores and calibrating review thresholds: the high/medium/
  low tool output + the routing threshold.
- ✅ Routing low-confidence or ambiguous answers to human review: the `route()` logic.

---

## What's next

**Part 6 — Provenance in multi-source synthesis (Task 5.6).** The finale. When
ScholarDesk answers from **several** sources at once, it must track **which source each
fact came from** — and flag when two sources disagree, using their dates to tell an
update apart from a contradiction.

See you in Part 6.

---

*CCAR-F · Domain 5 · Part 5 — ANKIT MISTRY*
