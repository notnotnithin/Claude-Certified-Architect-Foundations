# Plan Mode vs Direct Execution — The Decision Guide

### Task 3.4

---

## First, an honest word

Everything else in this course has been a file you can run or a command you can
type. **This one is different.** Plan mode vs direct execution is a **judgment
call** — a decision *you* make before you ask Claude to do anything. There is no
script that can make that decision for you, and pretending otherwise would teach
you the wrong thing.

So this page is a **decision guide** with worked examples from our own TripPlanner
project. Read it, then practise the three scenarios live in Claude Code.

---

## The two ways to work

**Direct execution** — you ask, Claude does it. Straight away.

**Plan mode** — Claude first *explores and proposes a plan*, and does not change
any files until you approve. You enter it with **Shift+Tab** in Claude Code (press
until you see plan mode indicated), or by asking Claude to plan before acting.

---

## The one question that decides it

> **Do I already know exactly what needs to change?**

- **Yes, and it's small** → **direct execution**. Planning would be overhead.
- **No — it's big, or there are several sensible ways to do it** → **plan mode**.
  Exploring first prevents expensive rework.

That's it. Everything below is just this question applied to real situations.

---

## When to use each

| Use **direct execution** when… | Use **plan mode** when… |
|---|---|
| The change is small and well understood | The change is large-scale |
| One file, or one function | Many files are affected |
| There's one obvious right answer | There are several valid approaches |
| You have a clear error/stack trace | It's an architectural decision |
| e.g. "add a validation check" | e.g. "restructure how we store data" |

**The cost of getting it wrong:** if you use direct execution on a big
architectural change, Claude starts editing files based on an incomplete picture.
When it discovers a dependency halfway through, you get rework — and a messy
half-changed codebase. Plan mode exists to avoid exactly that.

---

## Worked scenario 1 — Direct execution ✅

> **The task:** "TripPlanner should reject a trip stop with more than 30 nights."

**Think it through:**
- How many files? **One** (`destinations/stops.py`).
- How many sensible approaches? **One** — add a check next to the existing
  `nights < 1` check.
- Do we know exactly what to change? **Yes.**

**Verdict: direct execution.** Entering plan mode here would waste your time
producing a plan for a two-line change.

**Try it in Claude Code:**

```
In destinations/stops.py, make make_stop reject more than 30 nights, following our existing error style.
```

---

## Worked scenario 2 — Plan mode ✅

> **The task:** "Store the trip in a folder of one-file-per-stop instead of a
> single `my_trip.json`."

**Think it through:**
- How many files? **Several** — `storage/trip_store.py` for sure, plus anything
  that reads or writes trips, plus the tests, plus `.gitignore`.
- How many sensible approaches? **Several** — one file per stop named by date? by
  place? by an id? What happens to existing saved trips?
- Do we know exactly what to change? **No** — we'd be discovering as we go.

**Verdict: plan mode.** This is an architectural change with real design choices.
Let Claude explore and propose before touching anything.

**Try it in Claude Code:**

Press **Shift+Tab** until plan mode is on, then:

```
I want to change storage so each stop is saved as its own file in a folder, instead of one my_trip.json. Explore the code and propose an approach before changing anything.
```

**What to look for:** Claude reads the code, then comes back with a *plan* — the
files it would touch, the naming scheme options, the trade-offs, what happens to
old data — and waits for your approval. **Nothing has been changed yet.** That's
the whole value: you get to disagree *before* any work is wasted.

---

## Worked scenario 3 — Plan first, then execute ✅

> **The task:** "Make the parser understand natural language like '3 nights in
> Jaipur from Oct 2'."

(This is the very limitation our analyze-codebase skill flagged in Part 2.)

**Think it through:**
- How many approaches? **Several** — more clever string rules? a date library?
  ask Claude to parse it?
- Do we know which is right? **Not yet** — they have very different consequences.

**Verdict: plan mode to decide the approach, then direct execution to build it.**

This combination is extremely common in real work: **plan to investigate, execute
to implement.** You don't stay in plan mode forever — you use it to remove the
uncertainty, then switch to direct execution once the path is clear.

**Try it in Claude Code:**

In plan mode:

```
Our parser in parsing/free_text.py only handles rigid "place date nights" text. I want it to understand natural language. Explore the options and recommend one, with trade-offs. Don't change anything yet.
```

Then, once you've picked an approach, leave plan mode and ask Claude to implement
it directly.

---

## The Explore subagent — a companion idea

When Claude explores a codebase, it reads a *lot*. That reading can fill up your
conversation with detail you don't need.

Claude Code can delegate that noisy exploration to an **Explore subagent**, which
goes off, reads everything in its own space, and returns just a **summary**.

If that sounds familiar, it should — it's the **same idea as `context: fork`** from
Part 2. Verbose work happens somewhere else; only the summary comes back. This is
why exploration during plan mode doesn't drown your main chat.

---

## Quick self-test

For each, decide before reading the answer:

1. *"Fix the typo in the help message in `cli.py`."*
   → **Direct.** One file, one obvious change.

2. *"Add multi-user support so several people can each have their own trip."*
   → **Plan.** Touches storage, CLI, probably every module. Many valid designs.

3. *"`validate_date` crashes on `None` — here's the stack trace."*
   → **Direct.** Clear error, clear location, one fix.

4. *"Should we keep JSON, or move to a small database?"*
   → **Plan.** A pure architectural decision with trade-offs.

Notice the pattern: **the size of the typing isn't what matters — the size of the
uncertainty is.**

---

*CCA-Foundations · Domain 3 · TripPlanner · ANKIT MISTRY*
