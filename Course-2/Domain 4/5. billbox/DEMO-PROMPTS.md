# Part 4 — Live Demo Guide

### Task 4.4 — Validation, Retry & Feedback Loops

---

## Read this first — the map of Part 4

Two scripts, run in cmd. Part 3 guaranteed the *shape*; Part 4 checks the
*meaning*. You need your API key (from Part 0).

| Step | Where | Task | Needs API key? |
|------|-------|------|----------------|
| Demo 1 | cmd | ◆ **Task 4.4** | ✅ Yes |
| Demo 2 | cmd | ◆ **Task 4.4** | ✅ Yes |

Start in the project folder:

```cmd
cd C:\path\to\5. billbox
```

This part adds two receipts built to trigger the two outcomes:
- `broken_total.txt` — line items sum to **885**, but the printed total says
  **985** (a fixable discrepancy).
- `missing_total.txt` — the receipt is torn; there's **no total at all** (info
  genuinely absent).

---

## Demo 1 ◆ Task 4.4 — The anti-pattern: trust the output

Run the no-validation version:

```cmd
python extract_no_validation.py
```

**What it does:** extracts `broken_total.txt` with the guaranteed schema from
Part 3, and trusts whatever comes back.

**What to look for:** the shape is perfect, so the bad total sails straight
through. The line items don't add up to the stated total, but nobody checked — a
100-rupee error just entered our data. **A JSON schema checks shape, not whether
the numbers are right.** That's a *semantic* error, and it needs a different tool.

---

## Demo 2 ◆ Task 4.4 — The fix: validate, then retry with feedback

Run the validation version:

```cmd
python extract_with_validation.py
```

**What it does:** after extracting, it validates the data with a Pydantic model
(`billbox/receipt_model.py`) that checks the line items actually sum to the total.
If validation fails, it sends the failure **back to Claude with the exact error**
and lets it try again.

Watch the two receipts behave differently:

**`broken_total.txt` — retry HELPS:**
```
Attempt 1: rejected - Line items sum to 885.00, but stated_total is 985.0...
   -> A fixable discrepancy. Retrying with the exact error...
Attempt 2: VALID.
```
Told the *specific* discrepancy, Claude re-reads and corrects itself — flagging
the conflict and fixing the numbers.

**`missing_total.txt` — retry CANNOT help:**
```
Attempt 1: rejected - stated_total is missing...
   -> The total is ABSENT from the receipt. Retrying cannot invent it.
      Giving up (this needs a human).
```
The information simply isn't in the document. A good loop **recognises this and
stops**, instead of looping forever asking for something that isn't there.

---

## The two things that make this work

1. **Feed back the SPECIFIC error.** Not "try again" — the *exact* reason
   ("line items sum to 885 but total says 985"). That's what lets Claude correct
   itself precisely.

2. **Know when NOT to retry.** Format and semantic errors → retry can fix them.
   Missing information → retry is useless; stop and route to a human. Telling these
   apart is the heart of Task 4.4.

---

## The self-correction pattern in the schema

Open `schemas/receipt_schema_v2.json`. Notice we now ask Claude to extract **both**
`stated_total` (what's printed) **and** `calculated_total` (the sum it computes),
plus a `conflict_detected` flag. Extracting both lets us — and Claude — spot a
mismatch automatically. That's the "calculated vs stated" self-correction pattern
the exam describes.

---

## Why this matters (the one-line takeaway)

> **A schema guarantees valid shape; validation guarantees valid meaning.** Retry
> with the specific error to fix what's fixable — and give up gracefully on what
> isn't.

---

## Quick recap

| Demo | Task | Script | Shows |
|------|------|--------|-------|
| 1 | ◆ 4.4 | `extract_no_validation.py` | Bad numbers pass the schema unnoticed |
| 2 | ◆ 4.4 | `extract_with_validation.py` | Validate → retry with feedback → fix, or give up if info absent |

---

*CCAR-F · Domain 4 · BillBox · ANKIT MISTRY*
