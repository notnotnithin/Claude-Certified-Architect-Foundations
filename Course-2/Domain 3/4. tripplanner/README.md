# Part 3 — Plan Mode & Iterative Refinement

### Domain 3: Claude Code Configuration & Workflows · Tasks 3.4 + 3.5

---

## Where we are

- **Part 0** (`1. tripplanner`) — installed Claude Code, ran the app.
- **Part 1** (`2. tripplanner`) — memory & rules.
- **Part 2** (`3. tripplanner`) — commands & skills.
- **Part 3** (`4. tripplanner`, this folder) — **how you drive Claude.**

Parts 1 and 2 were about **configuring** Claude Code — files that shape how it
behaves. Part 3 is different: it's about **how you work with it**, moment to
moment. Everything from Parts 1 and 2 is carried forward unchanged.

---

## The one big idea of Part 3

> **The same request, asked differently, gives very different results.**

Two halves share that idea:

- **◆ Task 3.4 — Plan mode vs direct execution:** *how much thinking before doing?*
- **◆ Task 3.5 — Iterative refinement:** *how do I ask so I get what I want?*

---

## How Part 3 runs — two tools, three blocks

You will switch tools exactly **twice**. `DEMO-PROMPTS.md` announces every switch.

| Block | Where | Task | Needs API key? |
|-------|-------|------|----------------|
| **Block 1** — Demos 1–3 | Claude Code | ◆ **3.4** | ❌ No |
| **Block 2** — Demo 4 | cmd (a script) | ◆ **3.5** | ✅ **Yes** |
| **Block 3** — Demos 5–7 | Claude Code | ◆ **3.5** | ❌ No |

**Why two tools?**

- **Plan mode is a Claude Code feature** — it doesn't exist anywhere else.
- **Comparing two prompts fairly needs a fresh start each time.** Claude Code
  remembers what you already said, which would spoil the comparison — so that one
  demo uses a script.

**Why only Block 2 needs a key:** Claude Code runs on your Claude Pro login. A
plain Python script can't use that login, so it talks to the API directly and needs
its own key. Blocks 1 and 3 need nothing extra.

The tool switch at Block 1 → 2 is also the **task switch**: Block 1 is all of Task
3.4; everything after is Task 3.5.

---

## Half 1 ◆ Task 3.4 — Plan mode vs direct execution

**This is a judgment, not a setting.** There's no file to configure and no script
to run — you decide, before you ask.

The full guide is **`PLAN-MODE-GUIDE.md`**. Read it — it's short. Its core is one
question:

> **Do I already know exactly what needs to change?**

- **Yes, and it's small** → **direct execution**.
- **No — it's big, or several approaches could work** → **plan mode**.

In plan mode (**Shift+Tab** in Claude Code), Claude explores and **proposes a plan
without changing any files**, and waits for your approval. That's what prevents
expensive rework on big changes.

The guide walks three real TripPlanner scenarios:

| Scenario | Verdict |
|---|---|
| Reject stops over 30 nights | Direct — one file, one obvious change |
| Store each stop as its own file | Plan — many files, many valid designs |
| Make the parser understand natural language | Plan to decide, then execute to build |

It also covers the **Explore subagent**, which keeps verbose exploration out of your
main chat — the same idea as `context: fork` from Part 2.

---

## Half 2 ◆ Task 3.5 — Iterative refinement

Four techniques for steering Claude. The first is the big one.

### 1. Concrete input/output examples — the headline (Demo 4, in cmd)

When a prose description gets interpreted inconsistently, **showing examples beats
describing harder.**

This is where we fix a real problem in our own project. Remember the limitation our
analyze-codebase skill flagged in Part 2? Our parser only understands rigid text
like `"Jaipur 2026-10-02 3"`. It breaks on how people actually type:

- `"3 nights in Jaipur from Oct 2"` — natural language date
- `"New York 2026-11-01 2"` — a two-word place name
- `"two nights at Goa starting 5 Nov 2026"` — a spelled-out number

**`refine_prompt.py`** sends those **same 3 inputs** to the **same model** twice:

- **Attempt 1 — weak prompt:** a prose description. Reasonable-sounding, but the
  model must guess the key names, the date format, and whether to add commentary.
  The shapes wobble.
- **Attempt 2 — better prompt:** the same request **plus 3 worked examples**
  covering exactly the tricky cases. The shape locks in.

The script prints a `USABLE:` verdict per reply — can the app actually read this
JSON, with the right keys, a real date, and a number for nights? That turns "looks
fine" into a clear PASS/FAIL on screen.

> A fair point for students: the model is genuinely capable, so the weak prompt
> sometimes produces a good answer anyway. The lesson isn't that vague prompts
> *always* fail — it's that they aren't **reliable**. Run it twice and you'll see
> the inconsistency.

**Setup for this demo only** (Block 2 needs a key; the other blocks don't):

```cmd
copy .env.example .env
```

Paste your key from https://console.anthropic.com/ → API Keys into `.env`, then:

```cmd
pip install -r requirements.txt
python refine_prompt.py
```

Your `.env` is already in `.gitignore`.

### 2. Test-driven iteration (Demo 5)

Write the tests **first**, so "correct" is defined before any code exists. Then
paste failures back to guide the fix.

### 3. The interview pattern (Demo 6)

When you're not sure what you want, ask Claude to **interview you** first. It
surfaces questions you hadn't considered — before you build the wrong thing.

### 4. All at once, or one at a time? (Demo 7)

- **Problems that interact** → report them **together**, so Claude sees the whole
  picture and fixes the shared cause once.
- **Independent problems** → fix them **one at a time**, keeping each change clean.

---

## Your folder layout

```
4. tripplanner/
├── PLAN-MODE-GUIDE.md          ← NEW: the Task 3.4 decision guide
├── refine_prompt.py            ← NEW: the live-API demo (Task 3.5)
├── .env.example                ← NEW: copy to .env (Block 2 only)
├── DEMO-PROMPTS.md             ← the 7 demos, in 3 signposted blocks
├── README.md                   ← this guide
│
│   ── carried forward, unchanged ──
├── CLAUDE.md                    (Part 1)
├── standards/dates.md           (Part 1)
├── destinations/CLAUDE.md       (Part 1)
├── .claude/rules/               (Part 1)
├── .claude/commands/            (Part 2)
├── .claude/skills/              (Part 2)
├── user-level-CLAUDE-template/  (Part 1)
├── cli.py, destinations/, parsing/, storage/, tests/
└── .gitignore
```

---

## Exam objective coverage

**◆ Task 3.4 — Determine when to use plan mode vs direct execution**

- ✅ Plan mode for complex/large-scale/multi-approach/architectural work:
  `PLAN-MODE-GUIDE.md` + Demo 2.
- ✅ Direct execution for simple, well-scoped changes: the guide + Demo 1.
- ✅ Plan mode enables safe exploration before committing, preventing rework: the
  guide; Demo 2 shows nothing changes until you approve.
- ✅ The Explore subagent for isolating verbose discovery: the guide's companion
  section, linked back to `context: fork`.
- ✅ Selecting plan mode for architectural implications: scenario 2.
- ✅ Selecting direct execution for well-understood changes: scenario 1 + self-test.
- ✅ Combining plan mode for investigation with direct execution for
  implementation: scenario 3 + Demo 3.

**◆ Task 3.5 — Apply iterative refinement techniques**

- ✅ Concrete input/output examples as the most effective fix for inconsistent
  prose: `refine_prompt.py` + Demo 4.
- ✅ Test-driven iteration (tests first, share failures): Demo 5.
- ✅ The interview pattern: Demo 6.
- ✅ All issues in one message (interacting) vs sequentially (independent): Demo 7.
- ✅ Providing 2–3 concrete examples to clarify transformation requirements: the
  better prompt uses exactly 3.
- ✅ Providing specific test cases with example input and expected output for edge
  cases: the 3 inputs are edge cases (natural date, multi-word place, spelled-out
  number).

---

## What's next

**Part 4 — CI/CD (Task 3.6).** Running Claude Code with no human in the loop: `-p`
for non-interactive mode, `--output-format json` with `--json-schema` for
machine-readable results, and why an independent review instance beats asking the
same session to review its own work.

See you in Part 4.

---

*CCA-Foundations · Domain 3 · Part 3 — ANKIT MISTRY*
