# Part 1 — Live Demo Guide

### Task 4.1 — Explicit Criteria

---

## Read this first — the map of Part 1

Part 1 is simple: **two scripts, run in cmd, compared side by side.** No tool
switching. You need your API key set up (from Part 0).

| Step | Where | Task | Needs API key? |
|------|-------|------|----------------|
| Demo 1 | cmd | ◆ **Task 4.1** | ✅ Yes |
| Demo 2 | cmd | ◆ **Task 4.1** | ✅ Yes |

Start in the project folder:

```cmd
cd C:\path\to\2. billbox
```

If you haven't set your key yet:

```cmd
copy .env.example .env
```

...then paste your `sk-ant-...` key into `.env`. And install packages once:

```cmd
pip install -r requirements.txt
```

---

## Demo 1 ◆ Task 4.1 — The anti-pattern: vague criteria

Run the vague version first:

```cmd
python review_vague.py
```

**What it does:** asks Claude to "review this receipt and report any problems or
anything that looks off," and adds the classic non-fix "be conservative and only
report high-confidence issues."

**What to look for:** Claude flags **harmless things** — a rounded price, the
"thank you" line, an abbreviation, the payment method. These are **false
positives**. The receipt is fine, but the vague prompt made Claude hunt for
"anything off," so it invents concerns.

Notice "be conservative" didn't save it. The exam calls this out directly: vague
softeners like "be conservative" or "only high-confidence findings" **don't**
improve precision, because they aren't real criteria — just hopes.

> Run it two or three times. Because the criteria are vague, you may get slightly
> different flags each time. That inconsistency is part of the problem.

---

## Demo 2 ◆ Task 4.1 — The fix: explicit criteria

Now the explicit version:

```cmd
python review_explicit.py
```

**What it does:** same receipt, same model — but the prompt now says **exactly**
what counts as a problem and what to ignore:

- **Report only:** total mismatch, missing GST number, missing date, missing
  total — each with a severity (high/medium/low).
- **Ignore:** rounded prices, tip lines, thank-you messages, abbreviations,
  payment method.

**What to look for:** the harmless flags are **gone**. Claude only reports things
that match the explicit list — and for the clean grocery receipt, it likely says
"No issues found." That's the goal: **fewer false positives, so people trust the
tool.**

---

## See it on the other receipts

Open `review_explicit.py` in VS Code and change the filename in `main()`:

```python
receipt = load_receipt("restaurant_bill.txt")   # or utility_bill.txt
```

Run it again. The explicit criteria travel cleanly to any receipt — that's the
strength of defining *what* a problem is instead of hoping Claude guesses.

---

## Why this matters (the one-line takeaway)

> **Explicit categorical criteria beat vague instructions every time.** Telling
> Claude exactly what to report *and what to ignore* is the single biggest lever
> for cutting false positives.

---

## Quick recap

| Demo | Task | Script | Shows |
|------|------|--------|-------|
| 1 | ◆ 4.1 | `review_vague.py` | Vague criteria → false positives |
| 2 | ◆ 4.1 | `review_explicit.py` | Explicit criteria → clean, trustworthy output |

---

*CCAR-F · Domain 4 · BillBox · ANKIT MISTRY*
