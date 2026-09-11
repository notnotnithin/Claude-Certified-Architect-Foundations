# Part 1 — Explicit Criteria

### Domain 4: Prompt Engineering & Structured Output · Task 4.1

---

## Where we are

- **Part 0** (`1. billbox`) — set up the project and saw the messy receipts.
- **Part 1** (`2. billbox`, this folder) — BillBox's **first real request to
  Claude**, and the single biggest lever for reliable output: **explicit
  criteria**.

The Part 0 app is unchanged. Part 1 adds two small scripts that call the Claude
API — so from here on you'll need your API key (set up in Part 0).

> **Read** in **VS Code** (this file and `DEMO-PROMPTS.md`). **Run** in **cmd**.

---

## The one big idea of Part 1

> **Tell Claude exactly what counts — don't make it guess.**

When you ask Claude to review something with a **vague** instruction ("find any
problems"), it has to guess what a "problem" is. It guesses generously, and flags
harmless things — **false positives**. When you give it **explicit criteria**
(exactly what to report, exactly what to ignore), the false positives disappear.

That's Task 4.1 in one sentence.

---

## Why vague instructions fail

Here's the tempting first attempt (our `review_vague.py`):

> "Review this receipt and report any problems or anything that looks off. Be
> conservative and only report high-confidence issues."

It sounds careful. But it's a trap:

- **"Anything that looks off"** has no definition, so Claude invents concerns —
  a rounded price, a "thank you" line, an abbreviation.
- **"Be conservative"** feels like a safety net, but it isn't a real criterion.
  The exam specifically warns that softeners like "be conservative" or "only
  high-confidence findings" **do not** improve precision.

The result is a tool that cries wolf. And when a review tool flags too many
non-issues, people **stop trusting even its correct findings**. That's the real
cost of false positives.

---

## Why explicit criteria work

Here's the fix (our `review_explicit.py`). The prompt now says exactly:

**Report only these:**
- `TOTAL_MISMATCH` (high) — printed total ≠ subtotal + taxes, off by > ₹1
- `MISSING_GST` (medium) — no GST/GSTIN number anywhere
- `MISSING_DATE` (medium) — no date
- `MISSING_TOTAL` (high) — no final total

**Ignore these (they are NOT problems):**
- rounded prices, tip lines, thank-you messages, abbreviations, payment method

Three things make this work, and they map straight to the exam's skills for 4.1:

1. **Specific things to report** — categorical criteria, not "anything off."
2. **An explicit ignore-list** — the direct cure for false positives.
3. **Defined severity** (high/medium/low with concrete meaning) — so
   classification is consistent, not a guess.

---

## The demo

Two scripts, same receipt, same model — only the criteria change.

```cmd
python review_vague.py       # flags harmless things (false positives)
python review_explicit.py    # only reports what matches the criteria
```

Full walkthrough in **`DEMO-PROMPTS.md`**.

> The grocery receipt is actually clean, so the explicit version likely says
> "No issues found" — while the vague version invents problems. That contrast
> *is* the lesson.

---

## A note on "temporarily disabling a category"

The exam also mentions a real-world tactic: if one category of finding is
producing too many false positives, you **temporarily switch it off** while you
improve its wording — rather than letting it erode trust in the good categories.

In BillBox terms: if `MISSING_GST` were firing on receipts that legitimately
don't need a GST number, you'd remove that one rule from the criteria list until
you'd refined it, keeping the reliable rules working. It's the same idea as our
explicit ignore-list, applied one category at a time.

---

## Your folder layout

```
2. billbox/
├── review_vague.py         ← NEW: ❌ vague criteria (anti-pattern)
├── review_explicit.py      ← NEW: ✅ explicit criteria
├── DEMO-PROMPTS.md         ← how to run + what to notice
├── README.md               ← this guide
├── billbox/
│   ├── _shared.py          ← NEW: tiny API helper (keeps scripts focused)
│   ├── cli.py, reader.py   ← unchanged from Part 0
├── receipts/               ← unchanged from Part 0
├── requirements.txt, .env.example, .gitignore
```

`.env` (your key) stays out of version control via `.gitignore`.

---

## Exam objective coverage

**◆ Task 4.1 — Design prompts with explicit criteria to improve precision and reduce false positives**

- ✅ Explicit criteria over vague instructions: `review_vague.py` vs
  `review_explicit.py`.
- ✅ Why "be conservative" / "only high-confidence" fail to improve precision:
  built into the vague prompt and explained.
- ✅ Impact of false positives on trust: the "cries wolf" point in the README and
  demo.
- ✅ Writing specific criteria defining what to report vs skip: the explicit
  report-list and ignore-list.
- ✅ Temporarily disabling high-false-positive categories: the dedicated note
  above.
- ✅ Defining explicit severity criteria: the high/medium/low levels with concrete
  meaning.

---

## What's next

**Part 2 — Few-shot prompting (Task 4.2).** Explicit criteria tell Claude the
rules; few-shot examples *show* Claude the format. We use BillBox's three
different receipt layouts to teach Claude to extract the same clean fields from
any of them.

See you in Part 2.

---

*CCAR-F · Domain 4 · Part 1 — ANKIT MISTRY*
