# Part 3 — Structured Output with tool_use + JSON Schemas

### Domain 4: Prompt Engineering & Structured Output · Task 4.3

---

## Where we are

- **Part 1** (`2. billbox`) — explicit criteria (the rules).
- **Part 2** (`3. billbox`) — few-shot (the format, *usually* right).
- **Part 3** (`4. billbox`, this folder) — tool_use + JSON schema (the format,
  **guaranteed** right). **This is the core of Domain 4.**

Few-shot made the output shape *usually* correct. "Usually" isn't good enough for
a pipeline. Part 3 makes it *always* correct.

> **Read** in **VS Code**. **Run** in **cmd**. You need your API key (Part 0).

---

## The one big idea of Part 3

> **Give Claude a tool whose input is a JSON schema, and the output is guaranteed
> to match that schema.**

Instead of asking for JSON as text and hoping it parses, you define a **tool**. Its
`input_schema` is a strict JSON schema. When Claude "calls" the tool, the data it
fills in **must** match the schema — so JSON syntax errors become **impossible**.

The exam calls this the **most reliable** approach for structured output.

---

## Why text JSON isn't enough

Our `extract_text_json.py` shows the weakness. Ask Claude to "return JSON" as text,
and even when the content is right, the *wrapping* can break `json.loads`:

- a `Here's the JSON:` preamble
- ` ```json ` code fences around the object
- a trailing comment after the closing brace

You can write cleanup code to strip all that — but it stays fragile and breaks
eventually. It's the wrong foundation for a pipeline.

---

## The fix: tool_use

Our `extract_structured.py` defines a tool:

```python
EXTRACT_TOOL = {
    "name": "save_receipt",
    "description": "Save the structured data extracted from a receipt.",
    "input_schema": RECEIPT_SCHEMA,   # our JSON schema
}
```

When Claude calls `save_receipt`, its input is guaranteed schema-shaped. We read it
straight off the `tool_use` block as clean Python — **no `json.loads`, no cleanup,
no possible syntax error.**

---

## The three `tool_choice` modes (the exam tests this)

`tool_choice` controls whether and which tool Claude uses:

| Mode | Meaning | For extraction |
|------|---------|----------------|
| **forced** `{"type":"tool","name":"save_receipt"}` | must call *this* tool | ✅ best — always runs |
| **any** `{"type":"any"}` | must use *some* tool | ✅ with one tool, guarantees output |
| **auto** `{"type":"auto"}` | Claude decides — may just chat | ❌ risky — might skip the tool |

`extract_structured.py` runs all three so you can see the difference. The lesson:
for guaranteed extraction, use **forced** or **any** — never `auto`, because `auto`
lets Claude reply in text instead of using the tool.

---

## Schema design choices (open `schemas/receipt_schema.json`)

The schema demonstrates three patterns the exam highlights:

1. **Nullable fields prevent fabrication.** `gst_number` is typed
   `["string", "null"]`, so Claude returns `null` when there's no GST number
   instead of inventing a plausible one.

2. **Enum with an escape hatch.** `category` is an enum —
   `grocery / restaurant / utility / other` — a fixed set of valid choices, plus
   `"other"` for anything unexpected.

3. **The "other + detail" pattern.** `category_detail` is a free-text field used
   only when `category` is `"other"`. This is how you keep a category extensible
   without loosening the whole enum.

The **prompt** still carries format-normalisation rules (date → `YYYY-MM-DD`, total
→ plain number). That's the division of labour: the **schema guarantees the shape**,
the **prompt guides the content**.

---

## The honest limit: syntax vs semantics

This is important, and the exam tests it directly:

> A strict schema eliminates **syntax** errors — but not **semantic** ones.

The output is always *valid JSON in the right shape*. But whether `total` is the
*correct* number, or whether the line items actually sum to it, is a **different
problem**. The schema can't catch that. **Part 4 (validation) is where we catch
semantic errors.**

---

## The demo

```cmd
python extract_text_json.py     # text JSON -> can fail to parse
python extract_structured.py    # tool_use + schema -> guaranteed shape, all 3 tool_choice modes
```

Full walkthrough in **`DEMO-PROMPTS.md`**.

---

## Your folder layout

```
4. billbox/
├── extract_text_json.py     ← NEW: ❌ JSON as text (can fail to parse)
├── extract_structured.py    ← NEW: ✅ tool_use + schema (guaranteed)
├── schemas/
│   └── receipt_schema.json  ← NEW: the extraction schema (nullable, enum+other)
├── DEMO-PROMPTS.md          ← how to run + what to notice
├── README.md                ← this guide
├── billbox/
│   └── _shared.py           ← now also has extract_with_tool() helper
├── receipts/                ← unchanged (4 receipts)
├── requirements.txt, .env.example, .gitignore
```

---

## Exam objective coverage

**◆ Task 4.3 — Enforce structured output using tool use and JSON schemas**

- ✅ tool_use with JSON schemas as most reliable, eliminating syntax errors:
  `extract_structured.py` vs `extract_text_json.py`.
- ✅ The distinction between `tool_choice` auto / any / forced: all three run in
  `extract_structured.py`, with a table explaining each.
- ✅ Strict schemas eliminate syntax but not semantic errors: the "syntax vs
  semantics" section (and the bridge to Part 4).
- ✅ Schema design — required vs optional, enum with "other" + detail: the
  `receipt_schema.json` walkthrough.
- ✅ Defining extraction tools with JSON schemas and reading the tool_use response:
  the `save_receipt` tool + `extract_with_tool` helper.
- ✅ `tool_choice: "any"` to guarantee structured output: section [B].
- ✅ Forcing a specific tool: section [A], `{"type":"tool","name":"save_receipt"}`.
- ✅ Nullable fields to prevent hallucination: `gst_number`.
- ✅ Enum + "other" + detail for extensible categories: `category` / `category_detail`.
- ✅ Format-normalisation rules in the prompt alongside a strict schema: the SYSTEM
  prompt's date/total rules.

---

## What's next

**Part 4 — Validation, retry & feedback loops (Task 4.4).** The schema guarantees
the *shape*, but not that the numbers are *right*. Part 4 catches semantic errors —
like line items that don't sum to the total — and retries with specific feedback,
while knowing when a retry can't possibly help.

See you in Part 4.

---

*CCAR-F · Domain 4 · Part 3 — ANKIT MISTRY*
