# Part 6 — Live Demo Guide

### Task 4.6 — Multi-Instance & Multi-Pass Review

---

## Read this first — the map of Part 6

Three scripts, run in cmd. This is the finale of Domain 4. You need your API key
(from Part 0).

| Step | Where | Task | Needs API key? |
|------|-------|------|----------------|
| Demo 1 | cmd | ◆ **Task 4.6** | ✅ Yes |
| Demo 2 | cmd | ◆ **Task 4.6** | ✅ Yes |
| Demo 3 | cmd | ◆ **Task 4.6** | ✅ Yes |

Start in the project folder:

```cmd
cd C:\path\to\7. billbox
```

All three demos use `broken_total.txt` (items sum to 885, printed total 985) —
the receipt with a real mistake to catch.

---

## Demo 1 ◆ Task 4.6 — The anti-pattern: self-review

Run the self-review version:

```cmd
python review_self.py
```

**What it does:** in **one conversation**, Claude first extracts the receipt, then
is asked to review its *own* extraction.

**What to look for:** the reviewer is the **same instance** that did the
extraction, so it carries all the reasoning it used. It may notice the 885-vs-985
mismatch — or it may gloss over it, because it's checking work it already
"believes" in. It's the writer-missing-their-own-typos problem.

> Run it a few times. Self-review is *inconsistent* at catching its own mistakes —
> that inconsistency is the point.

---

## Demo 2 ◆ Task 4.6 — The fix: an independent instance

Run the independent-review version:

```cmd
python review_independent.py
```

**What it does:** the extraction is produced in one conversation, then a
**completely separate** conversation reviews it — a fresh instance that never saw
how the extraction was made.

**What to look for:** instance B has no reasoning to defend, so it just checks the
numbers — and **reliably catches the 885-vs-985 mismatch**. That's the core lesson
of Task 4.6: to catch subtle errors, use a **separate instance without the
generator's context**.

Notice it also reports a **confidence** level. A low-confidence review is your
signal to route that receipt to a human. That's **calibrated routing** — let the
model tell you which results need a closer look.

---

## Demo 3 ◆ Task 4.6 — Multi-pass: local + integration

Run the multi-pass version:

```cmd
python multi_pass_review.py
```

**What it does:** reviews several receipts in **two kinds of pass**:

- **Local passes** — each receipt reviewed on its own, one at a time, with full
  attention.
- **An integration pass** — one look *across* all receipts for issues that only
  appear in aggregate (duplicates, the same merchant with wildly different totals,
  dates out of order).

**What to look for:** no receipt gets skimmed (each had its own focused pass), and
cross-receipt issues still get caught (the integration pass). One giant prompt
reviewing everything at once would dilute attention — reviewing some receipts
carefully and skimming others, sometimes even contradicting itself.

---

## Why this matters (the one-line takeaway)

> **A fresh reviewer beats self-review, and focused passes beat one giant prompt.**
> Independence catches what self-review defends; splitting the work keeps attention
> from diluting.

---

## Quick recap

| Demo | Task | Script | Shows |
|------|------|--------|-------|
| 1 | ◆ 4.6 | `review_self.py` | Same instance reviewing itself → misses its own errors |
| 2 | ◆ 4.6 | `review_independent.py` | Fresh instance → catches the mismatch + reports confidence |
| 3 | ◆ 4.6 | `multi_pass_review.py` | Local passes + integration pass → no attention dilution |

---

*CCAR-F · Domain 4 · BillBox · ANKIT MISTRY*
