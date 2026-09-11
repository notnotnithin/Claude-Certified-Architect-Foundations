# Part 2 — Few-Shot Prompting

### Domain 4: Prompt Engineering & Structured Output · Task 4.2

---

## Where we are

- **Part 0** (`1. billbox`) — set up, saw the receipts.
- **Part 1** (`2. billbox`) — explicit criteria: tell Claude exactly the *rules*.
- **Part 2** (`3. billbox`, this folder) — few-shot: *show* Claude exactly the
  *shape* you want back.

Part 1 was about the **rules**. Part 2 is about the **format**. Together they're
the two halves of "asking well."

> **Read** in **VS Code**. **Run** in **cmd**. You need your API key (Part 0).

---

## The one big idea of Part 2

> **Showing beats telling.**

When you *describe* the output you want ("return it as JSON"), Claude has to guess
the exact shape — and it guesses differently for different inputs. When you *show*
a few worked examples, every answer comes back the same way. That's few-shot
prompting, and the exam calls it the **most effective** technique for consistent,
well-formatted output.

---

## The problem: same fields, different shapes

BillBox needs the **same three fields** — merchant, date, total — out of **every**
receipt, no matter the layout. But our receipts are laid out very differently:

- `grocery_receipt.txt` — `Date: 02/10/2026`, `Rs. 1194.90`
- `restaurant_bill.txt` — `05 Oct 2026`, `Grand Total: 1202.26`
- `utility_bill.txt` — `01 Sep - 30 Sep 2026`, `Amount Payable: Rs 1748.00`
- `handwritten_style.txt` — `dt 10-oct-26`, `total abt 374 rupees`, `no gst`

With **zero-shot** (instructions only), Claude returns these in inconsistent
shapes — the date format drifts, the total is sometimes a number and sometimes a
string, the merchant sometimes drags the address along. Downstream code that
expects one shape breaks.

That last receipt, `handwritten_style.txt`, is deliberately messy — an informal
"kirana store" bill. It's the stress test: can Claude handle a format nobody
showed it?

---

## The fix: show 2–4 examples

Our `extract_few_shot.py` puts three worked examples in the prompt before asking
for a new extraction. Each example is chosen on purpose to teach a tricky case:

| Example shows | Teaches |
|---------------|---------|
| A date written as words (`3-mar-26`) | normalise to `YYYY-MM-DD` |
| An informal amount (`320/-`) | return a plain number, no `Rs.`/`/-` |
| A receipt with **no GST** | return `null`, don't invent a value |

Because the examples *show* the shape rather than just describe it, every answer
comes back the same way — **even for the messy handwritten receipt the examples
never showed exactly**. That's the key property: few-shot examples teach
**judgement that generalises to new patterns**, not just a fixed template.

---

## Two jobs few-shot does at once

1. **Consistency** — every output has the same keys, same date format, same number
   style. That's what makes the result usable by the next step in a pipeline.

2. **Less hallucination** — by including a "no GST → `null`" example, we teach
   Claude to leave a field empty instead of inventing a plausible-looking value.
   Showing an empty-field case is the direct fix for made-up data in extraction.

---

## The demo

```cmd
python extract_zero_shot.py    # no examples -> inconsistent shapes
python extract_few_shot.py     # 3 examples  -> consistent output, even on novel formats
```

Full walkthrough in **`DEMO-PROMPTS.md`**.

> This is our first taste of getting *structured* data out. It's still done with
> examples and instructions, so the shape is *usually* right. In **Part 3** we
> make it **guaranteed** right, using tool_use with a JSON schema.

---

## Your folder layout

```
3. billbox/
├── extract_zero_shot.py    ← NEW: ❌ no examples (anti-pattern)
├── extract_few_shot.py     ← NEW: ✅ 3 examples
├── DEMO-PROMPTS.md         ← how to run + what to notice
├── README.md               ← this guide
├── receipts/
│   ├── grocery_receipt.txt, restaurant_bill.txt, utility_bill.txt  (from Part 0)
│   └── handwritten_style.txt   ← NEW: a tricky informal format
├── billbox/                ← unchanged (cli.py, reader.py, _shared.py)
├── requirements.txt, .env.example, .gitignore
```

---

## Exam objective coverage

**◆ Task 4.2 — Apply few-shot prompting to improve output consistency and quality**

- ✅ Few-shot as the most effective technique for consistent, formatted output:
  `extract_zero_shot.py` vs `extract_few_shot.py`.
- ✅ Demonstrating handling of ambiguous/varied cases: the three examples target
  word-dates, informal amounts, and missing GST.
- ✅ Generalising to novel patterns: the messy `handwritten_style.txt` is handled
  correctly though no example matched it exactly.
- ✅ Reducing hallucination in extraction: the "no GST → null" example teaches
  Claude not to invent values.
- ✅ Creating 2–4 targeted examples: exactly three, each covering a distinct tricky
  case.
- ✅ Examples that demonstrate the desired output format: fixed keys, `YYYY-MM-DD`
  dates, plain-number totals.
- ✅ Handling varied document structures: four genuinely different receipt layouts.
- ✅ Addressing empty/null extraction of fields: the `gst_number: null` case.

---

## What's next

**Part 3 — Structured output with tool_use + JSON schemas (Task 4.3).** Few-shot
makes the shape *usually* right. Part 3 makes it *guaranteed* right — Claude calls
a tool whose input is a strict JSON schema, so the output is always
schema-compliant. We'll also cover `tool_choice`: auto vs any vs forced.

See you in Part 3.

---

*CCAR-F · Domain 4 · Part 2 — ANKIT MISTRY*
