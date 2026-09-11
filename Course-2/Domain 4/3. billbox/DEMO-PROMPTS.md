# Part 2 — Live Demo Guide

### Task 4.2 — Few-Shot Prompting

---

## Read this first — the map of Part 2

Two scripts, run in cmd, compared side by side. You need your API key (from Part 0).

| Step | Where | Task | Needs API key? |
|------|-------|------|----------------|
| Demo 1 | cmd | ◆ **Task 4.2** | ✅ Yes |
| Demo 2 | cmd | ◆ **Task 4.2** | ✅ Yes |

Start in the project folder:

```cmd
cd C:\path\to\3. billbox
```

This part uses **four** receipts — the three from before plus a new tricky one,
`handwritten_style.txt`, with an informal layout (`dt 10-oct-26`, `90/-`,
`total abt 374`, `no gst`). It's there to test whether Claude can handle a format
it hasn't been shown.

---

## Demo 1 ◆ Task 4.2 — The anti-pattern: zero-shot

Run the version with **no examples**:

```cmd
python extract_zero_shot.py
```

**What it does:** asks Claude to pull merchant, date, and total from each of the
four receipts — using instructions only, no examples.

**What to look for:** read the four answers top to bottom and compare their
**shapes**:

- the **date** format probably changes between receipts (`02/10/2026` in one,
  `10-oct-26` in another),
- the **total** may be a plain number in one and a string like `"Rs. 374"` in
  another,
- the **merchant** may include the address sometimes and not others.

Same fields, **inconsistent shapes**. Downstream code that expects one shape will
break on this. The messy `handwritten_style.txt` is where it wobbles most.

---

## Demo 2 ◆ Task 4.2 — The fix: few-shot

Now the version **with examples**:

```cmd
python extract_few_shot.py
```

**What it does:** same four receipts, same model — but the prompt first **shows**
Claude three worked examples of exactly the output shape we want. The examples are
chosen to cover the tricky cases:

- a date written as words → normalise to `YYYY-MM-DD`
- an informal amount like `320/-` → a plain number
- a receipt with **no GST** → return `null` instead of inventing one

**What to look for:** every answer now comes back in the **same shape** — date as
`YYYY-MM-DD`, total as a plain number, missing GST as `null`. Even the messy
`handwritten_style.txt` — a format the examples never showed exactly — is handled
correctly. That's **generalisation**: the examples taught the *pattern*, not a
fixed template.

---

## Why this matters (the one-line takeaway)

> **Showing beats telling.** 2–4 worked examples make Claude's output consistent
> across formats — including messy ones it has never seen — far more reliably than
> instructions alone.

The examples also do a second job: they **reduce hallucination**. By showing a
"no GST → null" example, we teach Claude to leave a field empty rather than invent
a value. That's the fix for made-up data in extraction.

---

## Quick recap

| Demo | Task | Script | Shows |
|------|------|--------|-------|
| 1 | ◆ 4.2 | `extract_zero_shot.py` | No examples → inconsistent shapes |
| 2 | ◆ 4.2 | `extract_few_shot.py` | 3 examples → consistent output, even on novel formats |

---

*CCAR-F · Domain 4 · BillBox · ANKIT MISTRY*
