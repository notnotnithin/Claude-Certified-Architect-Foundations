# Part 5 — Batch Processing

### Domain 4: Prompt Engineering & Structured Output · Task 4.5

---

## Where we are

- **Parts 1–4** — got *one* receipt extracted reliably: explicit criteria,
  few-shot, structured output, validation.
- **Part 5** (`6. billbox`, this folder) — now do it for **a hundred at once**,
  cheaply, with the **Message Batches API**.

> **Read** in **VS Code**. **Run** in **cmd**. You need your API key (Part 0).

---

## The one big idea of Part 5

> **Batch trades speed for cost.** Send many requests as one job: 50% cheaper, but
> processed within 24 hours with no guarantee of when.

That single trade-off decides everything about when batch is right.

---

## An honest note about this part

A real batch can take **up to 24 hours**. You can't sit and wait for that on
camera. So Part 5 is built to teach the whole idea **without waiting**:

- `submit_batch.py` submits a **real** batch (you'll see the batch id and status).
- `check_batch.py sample` reads a **pre-saved** results file, so you can show the
  "read and sort the results" step **immediately** — exactly what you'd see once a
  real batch finished.

Nothing is faked. The sample file simply stands in for a batch that completed
earlier, so the lesson doesn't depend on a 24-hour wait.

---

## How batch works

**1. Submit many requests as one batch.** Each request carries a **`custom_id`** —
a label you choose. BillBox uses the receipt's filename. That id is critical
because **results can come back in any order**; the `custom_id` is how you match
each result to the receipt it came from.

**2. Wait.** The batch processes asynchronously — usually much faster than 24
hours, but with **no latency guarantee**.

**3. Read results.** When the batch has `ended`, you read the results (a JSONL
stream), matching each back by `custom_id`, and separate the successes from the
failures.

---

## Handling partial failures the right way

In our sample results, two of eight receipts failed — one hit a context limit, one
expired. The **right** response is *not* to re-run the whole batch. It's to:

1. find the failed items by `custom_id`,
2. fix whatever caused the failure (e.g. chunk a receipt that was too long),
3. submit a **new batch containing only those failed items**.

You don't pay again for the ones that already succeeded. Matching by `custom_id`
is what makes this precise.

---

## When to use batch — and when not

The decision is one question: **is anyone waiting on this result?**

| Situation | Use |
|-----------|-----|
| Overnight processing of the day's receipts | ✅ **Batch** — cheap, not urgent |
| A weekly bulk report | ✅ **Batch** |
| A user just uploaded a receipt and is watching | ❌ **Normal API** — batch could take hours |
| A blocking pre-merge check | ❌ **Normal API** |

**A limit worth knowing:** a single batch request **can't do multi-turn tool
calling** — it can't run a tool mid-request and continue with the result. So the
validation-retry loop from Part 4 lives in the *normal* API, not inside one batch
request. Each batch request runs once, independently.

---

## Refine on a sample first (a cost-saving habit)

Every request in a batch uses the same prompt. If the prompt is weak, you pay to
re-run the whole batch. So the smart pattern is: **perfect the prompt on a few
receipts with the normal API first**, then batch the rest once you're confident.
Cheap iteration up front saves expensive re-runs later.

---

## The demo

```cmd
python generate_receipts.py       # make ~100 sample receipts (once)
python submit_batch.py            # submit them all as one batch (real)
python check_batch.py sample      # read pre-saved results (no waiting)
python check_batch.py <batch_id>  # ...or check your real batch later
```

Full walkthrough in **`DEMO-PROMPTS.md`**.

---

## Your folder layout

```
6. billbox/
├── generate_receipts.py       ← NEW: makes ~100 sample receipts
├── submit_batch.py            ← NEW: submits them as one batch (with custom_ids)
├── check_batch.py             ← NEW: reads results, sorts succeeded/failed
├── sample_batch_results.jsonl ← NEW: pre-saved results (for the demo)
├── receipts_bulk/             ← NEW: created by generate_receipts.py (~100 files)
├── DEMO-PROMPTS.md, README.md
├── billbox/                   ← unchanged (cli, reader, _shared, receipt_model)
├── receipts/, schemas/        ← unchanged
├── requirements.txt, .env.example, .gitignore
```

---

## Exam objective coverage

**◆ Task 4.5 — Design efficient batch processing strategies**

- ✅ Message Batches API — 50% cost, up to 24h window, no latency SLA: explained
  throughout; `submit_batch.py` states it on submission.
- ✅ Batch appropriate for non-blocking/latency-tolerant work, wrong for blocking:
  the "when to use" table.
- ✅ No multi-turn tool calling within a single batch request: the "a limit worth
  knowing" note.
- ✅ `custom_id` for correlating request and response: used as the receipt filename
  throughout; `check_batch.py` matches on it.
- ✅ Matching API approach to latency needs (sync vs batch): the decision table.
- ✅ Handling failures by resubmitting only failed docs by `custom_id`: Demo 3 and
  the sample's two failures.
- ✅ Refining the prompt on a sample before batching large volumes: the dedicated
  section.

> The exam also mentions calculating batch *submission frequency* to meet an SLA
> (e.g. 4-hour submission windows to guarantee a 30-hour SLA with 24-hour
> processing). That's an arithmetic planning point rather than something to run;
> the idea is simply: if processing can take up to 24h and you must deliver within
> 30h, submit at least every 6h so no item ever risks missing the deadline.

---

## What's next

**Part 6 — Multi-instance & multi-pass review (Task 4.6).** The finale. A model
that just did the work is a weak reviewer of its own work — so we bring in a fresh,
independent instance to check it, and split big reviews into focused passes.

See you in Part 6.

---

*CCAR-F · Domain 4 · Part 5 — ANKIT MISTRY*
