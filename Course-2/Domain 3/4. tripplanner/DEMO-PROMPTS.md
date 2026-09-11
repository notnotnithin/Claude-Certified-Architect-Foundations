# Part 3 — Live Demo Guide

### Tasks 3.4 + 3.5

---

## Read this first — the map of Part 3

**Part 3 uses two tools, in three blocks.** You will switch tools exactly **twice**,
and this guide tells you every time.

| Block | Where you work | Task covered | Needs API key? |
|-------|----------------|--------------|----------------|
| **Block 1** — Demos 1–3 | Claude Code | ◆ **Task 3.4** | ❌ No |
| **Block 2** — Demo 4 | cmd (a script) | ◆ **Task 3.5** | ✅ **Yes** |
| **Block 3** — Demos 5–7 | Claude Code | ◆ **Task 3.5** | ❌ No |

**Why two tools?**

- **Plan mode is a Claude Code feature.** It doesn't exist anywhere else, so
  Block 1 must happen there.
- **Comparing two prompts fairly needs a fresh start each time.** Claude Code
  remembers what you already said, which would spoil the comparison — so Block 2
  uses a small script instead.
- **Blocks 1 and 3 use your Claude Pro login. Only Block 2 needs an API key**,
  because a plain Python script can't use your Claude Code subscription.

Notice the tool switch at Block 1 → 2 is also the **task switch**: everything in
Block 1 is Task 3.4, and everything after it is Task 3.5.

Start in the project folder:

```cmd
cd C:\path\to\DOMAIN 3\4. tripplanner
```

---

```
+======================================================+
|  BLOCK 1 — in CLAUDE CODE              # TASK 3.4    |
|  Plan mode vs direct execution                       |
|                                                      |
|  Why here: plan mode is a Claude Code feature.       |
|  There is nothing to run in Python.                  |
|  No API key needed - your Claude Pro login is used.  |
+======================================================+
```

Read `PLAN-MODE-GUIDE.md` first — it explains the decision. Then start Claude Code:

```cmd
claude
```

## Demo 1 ◆ Task 3.4 — Direct execution (a small, clear change)

The task is tiny and there's one obvious way to do it. No planning needed.

```
In destinations/stops.py, make make_stop reject more than 30 nights, following our existing error style.
```

**What to look for:** Claude just does it — one focused edit, matching the
`ValueError` style already in the file (our CLAUDE.md standard from Part 1). Fast,
no ceremony. That's direct execution earning its place.

---

## Demo 2 ◆ Task 3.4 — Plan mode (a big, open change)

Now a change with real design decisions. **Press Shift+Tab** until Claude Code
shows it's in plan mode. Then:

```
I want to change storage so each stop is saved as its own file in a folder, instead of one my_trip.json. Explore the code and propose an approach before changing anything.
```

**What to look for:**
- Claude **reads** the code first.
- It returns a **plan**: which files it would touch, naming options, what happens
  to existing saved trips, trade-offs.
- **Nothing has been changed yet** — it waits for your approval.

That last point is the whole value: you can disagree *before* any work is wasted.

---

## Demo 3 ◆ Task 3.4 — Plan first, then execute

The most realistic pattern. Still in plan mode:

```
Our parser in parsing/free_text.py only handles rigid "place date nights" text. I want it to understand natural language. Explore the options and recommend one, with trade-offs. Don't change anything yet.
```

**What to look for:** Claude lays out the approaches and recommends one.

Then **leave plan mode** (Shift+Tab) and ask it to implement the chosen approach
directly. Plan to *decide*, execute to *build* — you don't live in plan mode.

> **That's the end of Task 3.4.** Everything from here is Task 3.5.
>
> **Now leave Claude Code** — type `/exit`. The next demo runs in cmd.

---

```
+======================================================+
|  BLOCK 2 — in CMD                      # TASK 3.5    |
|  Iterative refinement - the headline                 |
|                                                      |
|  Why here: to compare two prompts FAIRLY, each needs |
|  a fresh start. Claude Code remembers what you       |
|  already said, which would spoil the comparison.     |
|                                                      |
|  *** THIS BLOCK NEEDS AN API KEY ***                 |
+======================================================+
```

## Why this block needs a key (and the others don't)

You're already logged into Claude Code — so why a key?

Because `refine_prompt.py` is a **plain Python script**, not Claude Code. It can't
use your Claude Pro subscription login. It talks to the Anthropic API directly, so
it needs its own key. Blocks 1 and 3 don't need one.

## One-time setup

1. Copy the example env file:

   ```cmd
   copy .env.example .env
   ```

2. Open `.env` in VS Code and paste your key from
   https://console.anthropic.com/ → API Keys:

   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

3. Install the packages (from the folder that has `requirements.txt`):

   ```cmd
   pip install -r requirements.txt
   ```

Your `.env` is already in `.gitignore`, so your key won't be committed.

---

## Demo 4 ◆ Task 3.5 — Prose vs examples (the live API demo)

This is the one demo in Domain 3 that calls the Claude API directly.

```cmd
python refine_prompt.py
```

**What it does:** sends the **same 3 messy inputs** to the **same model** with two
different prompts:

- **Attempt 1 (weak):** a prose description. The replies wobble — different key
  names, different date formats, sometimes chat around the JSON. The `USABLE:`
  line shows the failures.
- **Attempt 2 (better):** the same request **plus 3 concrete input/output
  examples**. The replies snap into the same clean shape every time.

The 3 inputs are exactly the cases that break our old parser — a natural-language
date, a two-word place name, and a spelled-out number. (Our analyze-codebase skill
flagged this very limitation back in Part 2.)

**The lesson:** nothing changed except the prompt. When prose is interpreted
inconsistently, **concrete input/output examples are the most effective fix.**

> The model is genuinely capable, so the weak prompt may sometimes produce a decent
> answer anyway. The point isn't that vague prompts *always* fail — it's that they
> aren't **reliable**. Run it twice and you'll see the wobble.

> **Now start Claude Code again** — the last three demos are back in conversation.
>
> ```cmd
> claude
> ```

---

```
+======================================================+
|  BLOCK 3 — back in CLAUDE CODE         # TASK 3.5    |
|  Iterative refinement - conversation techniques      |
|                                                      |
|  Why here: these are ways of TALKING to Claude, so   |
|  we practise them in a real conversation.            |
|  No API key needed - back on your Claude Pro login.  |
+======================================================+
```

## Demo 5 ◆ Task 3.5 — Test-driven iteration

Write the tests **first**, then let failures guide the work.

```
Write tests first for a new function that formats a stop as "Jaipur (3 nights from 2026-10-02)". Cover a normal stop, a one-night stop, and a multi-word place name. Don't write the function yet.
```

Then:

```
Now write the function to make those tests pass.
```

**What to look for:** the tests define "correct" **before** any implementation
exists, so there's no arguing later about what it should do. If a test fails, paste
the failure back and Claude fixes it — that's the iteration loop.

---

## Demo 6 ◆ Task 3.5 — The interview pattern

When you're unsure what you even want, have Claude ask **you** first.

```
I want to add a "remove a stop" command to TripPlanner. Before writing any code, interview me: ask the questions you need answered to build it properly.
```

**What to look for:** Claude asks things you may not have considered — remove by
number or by place name? what if two stops share a place? confirm before deleting?
what if the trip is empty? Answering those *first* prevents building the wrong
thing.

---

## Demo 7 ◆ Task 3.5 — All at once, or one at a time?

**Interacting problems → one message.** If fixes affect each other, give them
together:

```
Two related problems in the parser: it can't handle multi-word places, and it can't handle spelled-out numbers like "two". Fix both together, since the same splitting logic causes both.
```

**Independent problems → one at a time.** If they're unrelated, fixing them
separately keeps each change clean and easy to review.

**What to look for:** in the first case Claude reworks the shared logic **once**,
rather than patching it twice and possibly fighting itself.

---

## Quick recap

| Demo | Task | Where | Shows |
|------|------|-------|-------|
| 1 | ◆ 3.4 | Claude Code | Small change, done immediately — direct execution |
| 2 | ◆ 3.4 | Claude Code | Explore → plan → wait for approval — plan mode |
| 3 | ◆ 3.4 | Claude Code | Plan to decide, execute to build |
| 4 | ◆ 3.5 | **cmd (API key)** | Same model, better prompt, better output |
| 5 | ◆ 3.5 | Claude Code | Tests define correct up front |
| 6 | ◆ 3.5 | Claude Code | Claude interviews you |
| 7 | ◆ 3.5 | Claude Code | Related fixes together |

---

*CCA-Foundations · Domain 3 · TripPlanner · ANKIT MISTRY*
