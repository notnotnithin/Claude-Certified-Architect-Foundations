# Part 3 — Live Demo Guide

### Task 4.3 — Structured Output with tool_use + JSON Schemas

---

## Read this first — the map of Part 3

Two scripts, run in cmd. This is the **core** of Domain 4 — where extraction goes
from *usually* right to *guaranteed* right. You need your API key (from Part 0).

| Step | Where | Task | Needs API key? |
|------|-------|------|----------------|
| Demo 1 | cmd | ◆ **Task 4.3** | ✅ Yes |
| Demo 2 | cmd | ◆ **Task 4.3** | ✅ Yes |

Start in the project folder:

```cmd
cd C:\path\to\4. billbox
```

---

## Demo 1 ◆ Task 4.3 — The anti-pattern: JSON as text

Run the text version:

```cmd
python extract_text_json.py
```

**What it does:** asks Claude to "return JSON," gets the reply as plain text, and
tries to `json.loads` it.

**What to look for:** even when the *content* is correct, the *wrapping* can break
the parse — a `Here's the JSON:` preamble, ` ```json ` code fences, or a trailing
note. When that happens you'll see `PARSE FAILED`. You can write cleanup code to
cope, but it stays fragile. This is the problem Demo 2 removes entirely.

> Because Sonnet is good, the parse may succeed on some runs. Run it a few times —
> the point is that text output is *not guaranteed* to parse, and "not guaranteed"
> is unacceptable in a pipeline.

---

## Demo 2 ◆ Task 4.3 — The fix: tool_use with a JSON schema

Run the structured version:

```cmd
python extract_structured.py
```

**What it does:** gives Claude a **tool** (`save_receipt`) whose `input_schema` is
our JSON schema (`schemas/receipt_schema.json`). When Claude "calls" the tool, the
data it fills in is **guaranteed to match the schema** — no preamble, no fences, no
syntax errors possible.

The script walks all **three `tool_choice` modes**, which the exam tests directly:

| Mode | Meaning | Use for extraction? |
|------|---------|--------------------|
| **`{"type": "tool", "name": ...}`** (forced) | must call *this* tool | ✅ best — always runs |
| **`{"type": "any"}`** | must use *some* tool | ✅ with one tool, also guarantees output |
| **`{"type": "auto"}`** | Claude decides — may just chat | ❌ risky — might skip the tool |

**What to look for:**
- **[A] forced** and **[B] any** — every receipt comes back as clean structured
  data. No parsing, no possible breakage.
- **[C] auto** — Claude *may* choose to reply in text instead of using the tool.
  That's exactly why `auto` is the wrong choice when you *need* structured output.

---

## Look at the schema

Open `schemas/receipt_schema.json` in VS Code. Notice three design choices the
exam highlights:

- **`gst_number` is nullable** (`["string", "null"]`) — so Claude returns `null`
  instead of inventing a number when there's no GST.
- **`category` is an enum with `"other"`** — a fixed set of choices, plus an escape
  hatch.
- **`category_detail`** — the paired free-text field used only when category is
  `"other"`. That's the "enum + other + detail" pattern for extensible categories.

---

## Why this matters (the one-line takeaway)

> **tool_use with a JSON schema is the most reliable way to get structured output.**
> It eliminates JSON syntax errors entirely — the shape is *guaranteed*.

**One honest caveat, and the exam tests it:** a strict schema removes **syntax**
errors, not **semantic** ones. The output is always *valid JSON in the right shape*
— but whether `total` is the *correct* number is a different question. That's what
Part 4 (validation) tackles.

---

## Quick recap

| Demo | Task | Script | Shows |
|------|------|--------|-------|
| 1 | ◆ 4.3 | `extract_text_json.py` | Text JSON can fail to parse |
| 2 | ◆ 4.3 | `extract_structured.py` | tool_use + schema = guaranteed shape; all 3 tool_choice modes |

---

*CCAR-F · Domain 4 · BillBox · ANKIT MISTRY*
