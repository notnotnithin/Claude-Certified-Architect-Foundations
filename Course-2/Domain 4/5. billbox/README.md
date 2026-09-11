# Part 4 — Validation, Retry & Feedback Loops

### Domain 4: Prompt Engineering & Structured Output · Task 4.4

---

## Where we are

- **Part 3** (`4. billbox`) — tool_use + schema: the output *shape* is guaranteed.
- **Part 4** (`5. billbox`, this folder) — validation: the output *meaning* is
  checked.

Part 3 ended with an honest limit: a schema guarantees valid **syntax**, but not
valid **semantics**. The JSON is always the right shape — but whether the numbers
are *correct* is a separate problem. Part 4 solves that problem.

> **Read** in **VS Code**. **Run** in **cmd**. You need your API key (Part 0).

---

## The one big idea of Part 4

> **A schema checks the shape. Validation checks the meaning. Retry fixes what's
> fixable — and gives up on what isn't.**

---

## Why the schema isn't enough

Take `broken_total.txt`: its line items sum to **885**, but the printed total says
**985**. The schema is perfectly happy — `985` is a valid number in a valid shape.
So with no validation (`extract_no_validation.py`), that wrong total sails straight
into our data. Nobody noticed the numbers don't add up.

That's a **semantic error**. A JSON schema can't catch it, because it only checks
*shape*, not *arithmetic*. We need a separate validation step.

---

## Validation with Pydantic

`billbox/receipt_model.py` is a Pydantic model that checks the *meaning* of an
extraction:

- Do the line items actually sum to the stated total (within ₹1 for rounding)?
- Is the total actually present at all?

When a check fails, it raises a **specific** error message — and that message is the
key to the retry.

---

## The retry-with-feedback loop

`extract_with_validation.py` runs the loop: extract → validate → if it fails, send
the failure **back to Claude with the exact error** → try again.

The magic is in *what* we send back. Not "try again" — the **specific reason**:

> "Your previous extraction was rejected: line items sum to 885 but stated_total is
> 985. Re-read the receipt carefully..."

That precise feedback is what lets Claude correct itself, instead of making the same
mistake again.

---

## The crucial judgement: when retry WON'T help

This is the part the exam stresses most, and it's easy to miss.

**Retry helps** when the error is about *format* or *interpretation* — the
information is there, Claude just got it wrong. `broken_total.txt` is this case:
told the exact discrepancy, Claude re-reads and fixes it.

**Retry is useless** when the information is *genuinely absent from the document*.
`missing_total.txt` is torn — there is no total anywhere on it. No amount of
re-asking can invent one. A good loop **recognises this and stops**, routing to a
human, rather than burning attempts (and money) asking for something that isn't
there.

```
broken_total:  Attempt 1 rejected -> retry with error -> Attempt 2 VALID
missing_total: Attempt 1 rejected -> info is absent -> give up, route to human
```

Telling these two apart — *fixable* vs *absent* — is the heart of Task 4.4.

---

## The self-correction pattern (calculated vs stated)

Open `schemas/receipt_schema_v2.json`. We now extract **both**:

- `stated_total` — the total printed on the receipt
- `calculated_total` — the sum Claude computes from the line items
- `conflict_detected` — a flag set when they disagree

Asking for both, side by side, lets a mismatch surface automatically — that's the
"calculated vs stated" self-correction pattern the exam describes. It's the same
idea as a `conflict_detected` boolean for inconsistent source data.

---

## The demo

```cmd
python extract_no_validation.py     # bad total passes the schema unnoticed
python extract_with_validation.py   # validate -> retry with feedback -> fix, or give up
```

Full walkthrough in **`DEMO-PROMPTS.md`**.

---

## Your folder layout

```
5. billbox/
├── extract_no_validation.py    ← NEW: ❌ trust the output blindly
├── extract_with_validation.py  ← NEW: ✅ validate + retry with feedback
├── billbox/
│   └── receipt_model.py        ← NEW: Pydantic semantic validation
├── schemas/
│   ├── receipt_schema.json      (from Part 3)
│   └── receipt_schema_v2.json  ← NEW: adds stated/calculated total + conflict flag
├── receipts/
│   ├── broken_total.txt        ← NEW: items don't sum to total (retry fixes)
│   ├── missing_total.txt       ← NEW: no total at all (retry can't help)
│   └── ... (4 from before)
├── DEMO-PROMPTS.md, README.md
├── requirements.txt, .env.example, .gitignore
```

`pydantic` is in `requirements.txt` (installed since Part 0's setup).

---

## Exam objective coverage

**◆ Task 4.4 — Implement validation, retry, and feedback loops for extraction quality**

- ✅ Retry-with-error-feedback (append the specific validation error on retry):
  the loop in `extract_with_validation.py`.
- ✅ The limits of retry — useless when information is absent vs fixable format
  errors: `missing_total.txt` (gives up) vs `broken_total.txt` (retries).
- ✅ Semantic validation errors vs schema syntax errors: the Pydantic model catches
  what the schema can't.
- ✅ Follow-up requests including the original document, the failed extraction, and
  the specific error: exactly what the retry message contains.
- ✅ Identifying when retries will be ineffective: the "missing" branch stops early.
- ✅ Self-correction flows — calculated_total vs stated_total, conflict_detected:
  `receipt_schema_v2.json` + the model's `totals_must_agree` check.

> The exam also mentions a `detected_pattern` field for tracking *which* code
> constructs trigger findings, to analyse false-positive patterns over time. In
> BillBox terms that's the same idea as our `conflict_detected` flag: a structured
> marker on each extraction that lets you analyse where problems cluster. We keep
> it as `conflict_detected` since that's the natural fit for receipts.

---

## What's next

**Part 5 — Batch processing (Task 4.5).** So far we've handled receipts one at a
time. When you have a hundred to process overnight, the Message Batches API gives
50% cost savings — with trade-offs (up to 24 hours, no latency guarantee) that make
it right for some jobs and wrong for others.

See you in Part 5.

---

*CCAR-F · Domain 4 · Part 4 — ANKIT MISTRY*
