# Part 4 — Live Demo Guide

### Task 3.6

---

## Read this first — the map of Part 4

**Part 4 uses two tools, in three blocks.** You will switch tools exactly **twice**,
and this guide tells you every time.

| Block | Where you work | Task covered | Needs API key? |
|-------|----------------|--------------|----------------|
| **Block 1** — Demos 1–3 | cmd (`claude -p`) | ◆ **Task 3.6** | ❌ No |
| **Block 2** — Demos 4–5 | cmd (a script) | ◆ **Task 3.6** | ❌ No |
| **Block 3** — Demos 6–7 | Claude Code | ◆ **Task 3.6** | ❌ No |

**Good news: no API key anywhere in Part 4.** `claude -p` uses your normal Claude
Pro login, just like the interactive session. (Only Part 3's script needed a key.)

**Why the blocks are split this way:**

- **Block 1 is cmd** because the whole point of Task 3.6 is running Claude Code
  **without** the interactive interface. You have to leave the chat to see it.
- **Block 2 is a script** because in real CI, a *machine* reads Claude's output and
  decides pass/fail. That's a Python step, not a conversation.
- **Block 3 goes back to Claude Code** to understand *why* CI uses a separate,
  independent review — which is a concept best explored in conversation.

Start in the project folder:

```cmd
cd C:\path\to\DOMAIN 3\5. tripplanner
```

---

```
+======================================================+
|  BLOCK 1 - in CMD                      # TASK 3.6    |
|  Running Claude Code with no human                   |
|                                                      |
|  Why here: the point of this task is running Claude  |
|  Code WITHOUT the chat interface. You must leave     |
|  the chat to see it.                                 |
|  No API key needed - your Claude Pro login is used.  |
+======================================================+
```

## Demo 1 ◆ Task 3.6 — The problem: an interactive command hangs

In a CI pipeline there is **no human sitting there to answer questions**. Imagine
the pipeline ran this:

```cmd
claude "Review storage/trip_store.py"
```

**What happens:** Claude Code opens its **interactive chat interface** and waits for
you. In CI that means the job **hangs forever** until it times out. Nobody is there
to type.

Try it, see the chat open, then type `/exit`. That's the problem we're solving.

---

## Demo 2 ◆ Task 3.6 — The fix: the `-p` flag

Add **`-p`** (or `--print`). It runs the prompt once, prints the answer, and
**exits** — no chat, no waiting.

```cmd
claude -p "In one sentence, what does storage/trip_store.py do?"
```

**What to look for:** the answer prints straight into your terminal and you get your
command prompt back immediately. **No interface, no waiting.** That's the single
most important fact of Task 3.6: **`-p` is how Claude Code runs in a pipeline.**

---

## Demo 3 ◆ Task 3.6 — Machine-readable output: JSON + a schema

Plain English is fine for a human, but CI needs to *act* on the result. You cannot
reliably write "fail the build if there's a serious bug" against a paragraph of
prose. So we ask for **structured JSON in a shape we define**.

Look at `ci/review-schema.json` in VS Code first — it defines exactly what we want
back: a list of findings, each with a file, line, severity, issue, and suggestion,
plus an overall verdict.

Now run the review and save the output:

```cmd
claude -p "Review storage/trip_store.py against our project standards. Report every issue you find." --output-format json --json-schema ci/review-schema.json --allowedTools "Read,Grep,Glob" --max-turns 5 > ci/review-output.json
```

**What each flag does:**

| Flag | Why it's there |
|------|----------------|
| `-p` | non-interactive — required in CI |
| `--output-format json` | return structured data, not prose |
| `--json-schema ci/review-schema.json` | return it in **our exact shape** |
| `--allowedTools "Read,Grep,Glob"` | pre-approve tools — headless can't ask permission |
| `--max-turns 5` | cap the work so a stuck run can't spin forever |

Open `ci/review-output.json` in VS Code. Notice the findings sit inside a
**`structured_output`** field, alongside metadata like `session_id` and
`total_cost_usd` (CI teams track cost per run).

> `--allowedTools` matters more than it looks. In the chat, Claude asks "can I read
> this file?" and you click yes. **In headless mode there is nobody to ask** — so
> without pre-approved tools, the run just stops.

> **Now on to Block 2** — same terminal, but now a script reads that JSON.

---

```
+======================================================+
|  BLOCK 2 - in CMD (a script)           # TASK 3.6    |
|  Turning findings into a pass/fail decision          |
|                                                      |
|  Why here: in real CI, a MACHINE reads Claude's      |
|  output and decides whether to block the merge.      |
|  That is a script step, not a conversation.          |
|  No API key needed - it only reads a file.           |
+======================================================+
```

## Demo 4 ◆ Task 3.6 — Findings become PR comments

`ci/ci_review.py` is the pipeline's next step. It reads the JSON and prints what CI
would post on the pull request.

Run it on the sample file first (this works even if Demo 3 didn't run):

```cmd
python ci\ci_review.py ci\sample-review.json
```

**What to look for:**
- each finding formatted like a PR comment, with severity, file, and line,
- a count by severity,
- the run's cost,
- and a **RESULT: FAIL**, because there's a high-severity finding.

Check the exit code — this is the bit that matters:

```cmd
echo %ERRORLEVEL%
```

It prints **`1`**. In CI, a non-zero exit code means **the build fails and the merge
is blocked**. That's the payoff of the whole part: because we asked for *structured*
data, a machine could make that decision automatically.

Now run it on your real output from Demo 3:

```cmd
python ci\ci_review.py ci\review-output.json
```

---

## Demo 5 ◆ Task 3.6 — Why CLAUDE.md matters in CI

Ask yourself: in Demo 3, how did Claude know what "our project standards" even are?

**From `CLAUDE.md`** — the file we wrote back in Part 1. `claude -p` loads the same
project context an interactive session would: your `CLAUDE.md`, your `@import`, your
`.claude/rules/`.

That's why the review knew to check for utf-8 encoding, clear `ValueError` messages,
and the `YYYY-MM-DD` date rule. **Your Part 1 configuration is what makes CI reviews
useful.** Without it, Claude would only apply generic advice.

Try it — compare a review with your standards to one without:

```cmd
claude -p "Review storage/trip_store.py. What project-specific standards are you checking it against, and where did they come from?"
```

**What to look for:** Claude names your CLAUDE.md standards. The lesson: **document
your standards once, and every CI run applies them.**

> **Now start Claude Code** for the last block:
>
> ```cmd
> claude
> ```

---

```
+======================================================+
|  BLOCK 3 - in CLAUDE CODE              # TASK 3.6    |
|  Why CI uses a separate, independent reviewer        |
|                                                      |
|  Why here: this is a concept about how sessions      |
|  think, best explored in conversation.               |
|  No API key needed - your Claude Pro login is used.  |
+======================================================+
```

## Demo 6 ◆ Task 3.6 — The self-review problem

Ask Claude to write something, then immediately review its own work:

```
Write a small function in a new file scratch_demo.py that calculates the total nights across all stops in a trip.
```

Then, in the **same session**:

```
Now review that function you just wrote. What's wrong with it?
```

**What to look for:** Claude will likely defend or lightly polish its own work. It
**already holds the reasoning** that produced the code — it "knows why" it made each
choice, so it's less likely to question them.

This is the concept: **a session that generated code is a weak reviewer of that same
code.** It isn't a flaw in the model; it's the same reason a writer misses their own
typos.

---

## Demo 7 ◆ Task 3.6 — The fix: an independent reviewer

Now get a **fresh** opinion. Exit this session:

```
/exit
```

And review the same file from a **brand-new, independent run** that never saw the
reasoning behind it:

```cmd
claude -p "Review scratch_demo.py. Be critical: what problems do you see?"
```

**What to look for:** the fresh instance often catches more, and questions choices
the original session took for granted. It has **no attachment to the reasoning** —
it only sees the code.

**That's why CI reviews are valuable:** every CI run is a brand-new instance with no
memory of who wrote the code or why. It's an independent reviewer by design.

(Delete `scratch_demo.py` when you're done — it was only for this demo.)

---

## Bonus — what this looks like in a real pipeline

Open `.github/workflows/claude-review.yml` in VS Code. It's a real GitHub Actions
workflow wiring together everything you just ran by hand:

1. check out the code,
2. install Claude Code,
3. run `claude -p ... --output-format json --json-schema ...`,
4. run `ci_review.py` on the result — and **fail the build** if it exits non-zero.

One difference to notice: in CI there's no browser to log in with, so it
authenticates with an API key stored in the repository's **secrets** — never pasted
into the file.

---

## Quick recap

| Demo | Task | Where | Shows |
|------|------|-------|-------|
| 1 | ◆ 3.6 | cmd | An interactive call hangs in CI |
| 2 | ◆ 3.6 | cmd | `-p` runs once and exits |
| 3 | ◆ 3.6 | cmd | `--output-format json` + `--json-schema` |
| 4 | ◆ 3.6 | cmd (script) | JSON → PR comments → exit code → pass/fail |
| 5 | ◆ 3.6 | cmd | CLAUDE.md gives CI your project standards |
| 6 | ◆ 3.6 | Claude Code | A session reviewing its own code is weak |
| 7 | ◆ 3.6 | cmd | An independent instance reviews better |

---

*CCA-Foundations · Domain 3 · TripPlanner · ANKIT MISTRY*
