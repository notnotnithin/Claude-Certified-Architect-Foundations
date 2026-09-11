# Part 5 — Live Demo Guide

### Task 4.5 — Batch Processing

---

## Read this first — the map of Part 5

Three scripts, run in cmd. This part processes **many** receipts at once, cheaply.
You need your API key (from Part 0).

| Step | Where | Task | Needs API key? |
|------|-------|------|----------------|
| Demo 1 | cmd | ◆ **Task 4.5** | ✅ Yes (submit) |
| Demo 2 | cmd | ◆ **Task 4.5** | ✅ Yes (real) / ❌ No (sample) |
| Demo 3 | cmd | ◆ **Task 4.5** | ❌ No (concept) |

Start in the project folder:

```cmd
cd C:\path\to\6. billbox
```

> **Honest heads-up:** a real batch can take **up to 24 hours**. So this part is
> built so you can teach the whole idea **without waiting** — you submit a real
> batch (Demo 1), then read a **pre-saved** result to show the "read results" step
> immediately (Demo 2, `sample` mode). Nothing is faked — the sample simply stands
> in for a batch that finished earlier.

---

## Demo 1 ◆ Task 4.5 — Submit 100 receipts as one batch

First make the pile of receipts (once):

```cmd
python generate_receipts.py
```

This writes ~100 sample receipts into `receipts_bulk/`. Then submit them all as a
single batch:

```cmd
python submit_batch.py
```

**What to look for:**
- It builds **one request per receipt**, each with a unique **`custom_id`** (the
  filename) — that id is how we match a result back to its receipt later.
- It prints a **Batch ID** and a status. **Save that ID.**
- It reminds you the batch can take up to 24 hours.

**The trade-off (this is the whole lesson):** the batch is **50% cheaper** than
normal calls, but it's processed **within 24 hours with no latency guarantee**.
That's a great deal for an overnight job, and a terrible deal for anything a user
is waiting on right now.

---

## Demo 2 ◆ Task 4.5 — Read the results

In real life you'd come back later and run:

```cmd
python check_batch.py msgbatch_YOUR_ID_HERE
```

If it's not finished, it tells you so and asks you to come back later. To
**demonstrate the finished state right now**, use the pre-saved sample:

```cmd
python check_batch.py sample
```

**What to look for:**
- results are matched back to receipts by **`custom_id`** (order isn't guaranteed,
  so the id is essential),
- they're sorted into **succeeded** and **failed**,
- and it shows an example extracted result.

In the sample, two receipts failed — one hit a context limit, one expired.

---

## Demo 3 ◆ Task 4.5 — Handle failures the right way

Look at what `check_batch.py sample` says about the failures:

> These custom_ids FAILED and should be resubmitted... resubmit ONLY these — not
> the whole batch.

**That's the key skill:** when part of a batch fails, you **resubmit only the
failed items**, matched by `custom_id` — after fixing whatever caused the failure
(for example, chunking a receipt that was too long to fit). You don't re-run the
whole batch and pay for the 98 that already worked.

---

## When to use batch — and when NOT to

This is the decision the exam tests. Ask: **is anyone waiting on this result?**

| Situation | Use |
|-----------|-----|
| Overnight processing of yesterday's receipts | ✅ **Batch** (cheap, no rush) |
| Weekly bulk report | ✅ **Batch** |
| A user just uploaded a receipt and is watching the screen | ❌ **Normal API** (batch could take hours) |
| A pre-merge check blocking a developer | ❌ **Normal API** |

One more limit to know: a batch request **can't do multi-turn tool calling** — it
can't run a tool mid-request and continue. Each request is processed once,
independently. So the validation-retry loop from Part 4 belongs in the *normal*
API, not inside a single batch request.

---

## A smart habit: refine on a sample first

Before sending 100 (or 10,000) receipts, run your prompt on a **small sample** with
the normal API and get it right. Every receipt in a batch uses the same prompt — so
a weak prompt means paying to re-run the whole batch. Perfect the prompt cheaply on
a few, *then* batch the rest.

---

## Why this matters (the one-line takeaway)

> **Batch trades speed for cost.** Use it for large, non-urgent jobs; match results
> by `custom_id`; and resubmit only what failed.

---

## Quick recap

| Demo | Task | Script | Shows |
|------|------|--------|-------|
| 1 | ◆ 4.5 | `submit_batch.py` | Submit 100 receipts, one batch, custom_ids |
| 2 | ◆ 4.5 | `check_batch.py sample` | Read results, match by custom_id, sort succeeded/failed |
| 3 | ◆ 4.5 | (same output) | Resubmit only the failed ones |

---

*CCAR-F · Domain 4 · BillBox · ANKIT MISTRY*
