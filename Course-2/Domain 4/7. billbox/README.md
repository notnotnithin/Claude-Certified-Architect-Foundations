# Part 6 — Multi-Instance & Multi-Pass Review

### Domain 4: Prompt Engineering & Structured Output · Task 4.6

---

## Where we are

- **Parts 1–5** — got receipts extracted reliably, validated, and processed in
  bulk.
- **Part 6** (`7. billbox`, this folder) — the finale: **how to review the work
  well**, so mistakes get caught before they ship.

> **Read** in **VS Code**. **Run** in **cmd**. You need your API key (Part 0).

---

## The one big idea of Part 6

> **The best reviewer is a fresh one.** A model that just did the work carries its
> own reasoning and tends to defend it. A separate, independent instance — with no
> attachment to how the work was made — catches more.

---

## Why self-review is weak

It's tempting to extract a receipt and then, in the same conversation, ask Claude
to check its own work. Efficient, right? But it's the *weaker* approach.

The reviewing instance is the **same one** that produced the extraction, so it
still holds all the reasoning it used. Having already "decided" the total was 985,
it's inclined to defend or lightly polish that decision rather than truly question
it. It's the same reason a writer misses their own typos — they read what they
*meant* to write.

Our `review_self.py` shows this: it extracts `broken_total.txt` (items sum to 885,
printed total 985) and asks itself to check. Sometimes it catches the mismatch;
often it glosses over it. **Inconsistent** — which is exactly the problem.

---

## Why an independent instance is stronger

`review_independent.py` does it right. The extraction is produced in one
conversation; then a **completely separate** conversation reviews it — a fresh
instance that receives only the receipt and the extraction, with **none of the
generator's reasoning**.

With nothing to defend, the independent reviewer just checks: do these numbers add
up? And it **reliably catches** the 885-vs-985 mismatch that self-review might miss.

That's the heart of Task 4.6: **to catch subtle errors, use a separate instance
without the generator's context — not the same one that produced the work.**

---

## Confidence and calibrated routing

The independent reviewer also reports a **confidence** level (high/medium/low). That
small addition is powerful: a **low-confidence** review is a signal to route that
receipt to a **human**. Instead of reviewing everything by hand, you let the model
flag which results are shaky and focus human attention there. That's **calibrated
routing** — the model helps you spend limited review time where it matters.

---

## Multi-pass: local + integration

When there are **many** receipts to review, one giant prompt reviewing them all at
once **dilutes attention** — some get a careful look, others get skimmed, and the
model can even contradict itself (flagging a pattern in one receipt while approving
the same thing in another).

`multi_pass_review.py` splits the work into two kinds of pass:

1. **Local passes** — review each receipt on its own, one at a time. Full attention
   on one receipt means consistent, careful checks.

2. **An integration pass** — one look *across* all receipts for issues that only
   appear in aggregate: duplicate bills, the same merchant with wildly different
   totals, dates out of order.

Neither pass alone is enough — a local pass can't see cross-receipt issues, and an
integration pass can't give each receipt deep individual attention. **You need
both.**

---

## The demo

```cmd
python review_self.py           # same instance reviews itself (weak)
python review_independent.py    # fresh instance reviews (strong) + confidence
python multi_pass_review.py     # local passes + one integration pass
```

Full walkthrough in **`DEMO-PROMPTS.md`**.

---

## Your folder layout

```
7. billbox/
├── review_self.py           ← NEW: ❌ same instance reviews its own work
├── review_independent.py    ← NEW: ✅ fresh instance reviews + confidence
├── multi_pass_review.py     ← NEW: local passes + integration pass
├── DEMO-PROMPTS.md, README.md
├── billbox/                 ← unchanged (cli, reader, _shared, receipt_model)
├── receipts/, schemas/      ← unchanged
├── requirements.txt, .env.example, .gitignore
```

---

## Exam objective coverage

**◆ Task 4.6 — Design multi-instance and multi-pass review architectures**

- ✅ Self-review limitations (a model retains reasoning from generation, less likely
  to question its own decisions): `review_self.py` + the "why self-review is weak"
  section.
- ✅ Independent review instances catch more than self-review: `review_independent.py`.
- ✅ Multi-pass — per-item local passes plus a cross-item integration pass:
  `multi_pass_review.py`.
- ✅ Using a second independent instance without the generator's context: the two
  separate conversations in `review_independent.py`.
- ✅ Splitting large reviews into focused per-item passes + an integration pass:
  the local/integration split.
- ✅ Verification passes with self-reported confidence for calibrated routing: the
  confidence level in `review_independent.py` and the routing note.

---

## Domain 4 complete — what you've built

Starting from a plain receipt reader, BillBox now extracts reliable structured data
from messy documents. Look back at the seven folders:

| Part | What you added | Task |
|------|----------------|------|
| 0 | Setup + a receipt reader | — |
| 1 | Explicit criteria (report vs ignore) | 4.1 |
| 2 | Few-shot examples for varied formats | 4.2 |
| 3 | tool_use + JSON schema (guaranteed shape) | 4.3 |
| 4 | Validation + retry (guaranteed meaning) | 4.4 |
| 5 | Batch processing (cheap at scale) | 4.5 |
| 6 | Independent + multi-pass review | 4.6 |

**All six Domain 4 task statements, on one project.**

And notice how they build on each other: few-shot (Part 2) got the shape *usually*
right; tool_use (Part 3) made it *guaranteed*; validation (Part 4) caught the
*semantic* errors the schema couldn't; and independent review (Part 6) catches what
a single pass — even a validated one — might still miss. Each layer catches a class
of problem the previous one couldn't. That's what a reliable extraction pipeline
actually looks like.

---

*CCAR-F · Domain 4 · Part 6 — ANKIT MISTRY*
