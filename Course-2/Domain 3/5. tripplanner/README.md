# Part 4 — CI/CD

### Domain 3: Claude Code Configuration & Workflows · Task 3.6

---

## Where we are

- **Part 0** (`1. tripplanner`) — installed Claude Code, ran the app.
- **Part 1** (`2. tripplanner`) — memory & rules.
- **Part 2** (`3. tripplanner`) — commands & skills.
- **Part 3** (`4. tripplanner`) — plan mode & refinement.
- **Part 4** (`5. tripplanner`, this folder) — **CI/CD.** The finale.

Everything from Parts 1–3 is carried forward unchanged.

---

## The one big idea of Part 4

> **Running Claude Code when nobody is watching.**

Every part so far assumed **you** were sitting there — typing, reading, approving.
Part 4 removes the human. In a CI/CD pipeline, Claude Code runs automatically when
someone opens a pull request, and a **machine** acts on the result.

That changes three things:

1. It can't open a chat interface (nobody's there) → **`-p`**
2. It can't return prose (a machine must read it) → **`--output-format json` +
   `--json-schema`**
3. It can't ask permission (nobody's there to click yes) → **`--allowedTools`**

---

## How Part 4 runs — two tools, three blocks

You will switch tools exactly **twice**. `DEMO-PROMPTS.md` announces every switch.

| Block | Where | Task | Needs API key? |
|-------|-------|------|----------------|
| **Block 1** — Demos 1–3 | cmd (`claude -p`) | ◆ **3.6** | ❌ No |
| **Block 2** — Demos 4–5 | cmd (a script) | ◆ **3.6** | ❌ No |
| **Block 3** — Demos 6–7 | Claude Code | ◆ **3.6** | ❌ No |

**No API key needed anywhere in Part 4** — `claude -p` uses your normal Claude Pro
login. (Only Part 3's script needed a key, because a plain Python script can't use
that login.)

**Why the split:** Block 1 must be in cmd because the whole point is running
*without* the chat. Block 2 is a script because in real CI a *machine* decides
pass/fail. Block 3 returns to Claude Code because the independent-reviewer idea is
best explored in conversation.

---

## Concept 1 ◆ Task 3.6 — `-p` for non-interactive mode

If a pipeline runs plain `claude "Review this file"`, Claude Code opens its **chat
interface and waits for a human**. In CI, the job hangs until it times out.

Adding **`-p`** (or `--print`) runs the prompt once, prints the answer to standard
output, and **exits**:

```cmd
claude -p "In one sentence, what does storage/trip_store.py do?"
```

That's the foundation of everything else in this part.

---

## Concept 2 ◆ Task 3.6 — Structured output for machines

A human can read prose. A pipeline can't act on it reliably. You cannot write "fail
the build if there's a serious bug" against a paragraph of English.

So we ask for **JSON in a shape we define ourselves**:

```cmd
claude -p "Review storage/trip_store.py against our project standards." --output-format json --json-schema ci/review-schema.json --allowedTools "Read,Grep,Glob" --max-turns 5 > ci/review-output.json
```

| Flag | Why |
|------|-----|
| `-p` | non-interactive |
| `--output-format json` | structured data, not prose |
| `--json-schema ci/review-schema.json` | **our exact shape** |
| `--allowedTools "Read,Grep,Glob"` | pre-approve tools — headless can't ask |
| `--max-turns 5` | cap the work so a stuck run can't spin |

Open `ci/review-schema.json` in VS Code: it declares that every finding must have a
file, line, severity (`high`/`medium`/`low`), issue, and suggestion, plus an overall
verdict. The findings come back inside a **`structured_output`** field, next to
metadata like `session_id` and `total_cost_usd`.

`--allowedTools` deserves a note. Interactively, Claude asks "may I read this file?"
and you click yes. **Headless, there is nobody to ask** — so without pre-approved
tools, the run stalls.

---

## Concept 3 ◆ Task 3.6 — The machine decides

`ci/ci_review.py` is the next pipeline step. It reads the JSON and:

1. prints each finding as a PR comment would look,
2. counts them by severity,
3. **exits 0 (pass) or 1 (fail)** so CI can block the merge.

```cmd
python ci\ci_review.py ci\sample-review.json
echo %ERRORLEVEL%
```

That exit code is the punchline of the whole part. A non-zero exit means **the build
fails and the pull request is blocked** — an automatic decision, made from structured
data, with no human involved. That's *why* we asked for JSON.

---

## Concept 4 ◆ Task 3.6 — CLAUDE.md is what makes CI reviews useful

How did Claude know what "our project standards" are? **From `CLAUDE.md`** — written
back in Part 1.

`claude -p` loads the same project context an interactive session would: your
`CLAUDE.md`, its `@import`, your `.claude/rules/`. That's why the CI review checks
for utf-8 encoding, clear `ValueError` messages, and `YYYY-MM-DD` dates.

**Document your standards once; every CI run applies them.** Part 1's work is what
gives Part 4 its teeth.

---

## Concept 5 ◆ Task 3.6 — Why an independent reviewer beats self-review

A session that just wrote code is a **weak reviewer of that same code**. It holds the
reasoning that produced it — it "knows why" every choice was made, so it's unlikely
to question them. Same reason a writer misses their own typos.

A **fresh instance** has no such attachment. It never saw the reasoning; it only sees
the code. It asks the awkward questions.

**This is a hidden strength of CI:** every CI run is a brand-new instance with no
memory of who wrote the code or why. It's an independent reviewer *by design*.
Demos 6 and 7 let you feel the difference.

---

## Your folder layout

```
5. tripplanner/
├── ci/
│   ├── review-schema.json      ← NEW: the shape we demand back
│   ├── ci_review.py            ← NEW: JSON → PR comments → pass/fail
│   └── sample-review.json      ← NEW: sample output to practise on
├── .github/workflows/
│   └── claude-review.yml       ← NEW: a real CI pipeline
├── DEMO-PROMPTS.md             ← the 7 demos, in 3 signposted blocks
├── README.md                   ← this guide
│
│   ── carried forward, unchanged ──
├── CLAUDE.md, standards/, destinations/CLAUDE.md   (Part 1)
├── .claude/rules/, .claude/commands/, .claude/skills/  (Parts 1-2)
├── PLAN-MODE-GUIDE.md, refine_prompt.py, .env.example  (Part 3)
├── user-level-CLAUDE-template/
├── cli.py, destinations/, parsing/, storage/, tests/
└── .gitignore
```

---

## Exam objective coverage

**◆ Task 3.6 — Integrate Claude Code into CI/CD pipelines**

- ✅ The `-p` / `--print` flag for non-interactive mode: Concept 1 + Demos 1–2.
- ✅ `--output-format json` and `--json-schema` for structured CI output:
  Concept 2 + Demo 3.
- ✅ CLAUDE.md as the mechanism for providing project context to CI-invoked Claude
  Code: Concept 4 + Demo 5.
- ✅ Session context isolation — why the session that generated code reviews it
  poorly vs an independent instance: Concept 5 + Demos 6–7.
- ✅ Running Claude Code in CI with `-p` to prevent interactive hangs: Demos 1–2.
- ✅ Using `--output-format json` with `--json-schema` for machine-parseable
  findings posted as PR comments: Demo 3 + Demo 4.
- ✅ Documenting standards in CLAUDE.md to improve output quality: Concept 4 + Demo 5.
- ✅ A real pipeline wiring it together: `.github/workflows/claude-review.yml`.

---

## Domain 3 complete — what you've built

Look back at the five folders side by side. Starting from a plain Python app, you
have:

| Part | What you added | Tasks |
|------|----------------|-------|
| 0 | A working Claude Code setup | — |
| 1 | Memory & rules — CLAUDE.md hierarchy, `@import`, path globs | 3.1, 3.3 |
| 2 | Commands & skills — `/trip-review`, `context: fork`, `allowed-tools` | 3.2 |
| 3 | Plan mode & refinement — when to plan, how to steer | 3.4, 3.5 |
| 4 | CI/CD — `-p`, JSON schemas, independent review | 3.6 |

**All six Domain 3 task statements, on one project.**

And notice how the parts connect: Part 1's `CLAUDE.md` is what makes Part 4's CI
reviews project-aware. Part 2's `context: fork` is the same idea as Part 3's Explore
subagent. Part 2's skill *found* the parser bug that Part 3 *fixed*. That's not a
coincidence — it's how these features are meant to work together on a real project.

---

*CCA-Foundations · Domain 3 · Part 4 — ANKIT MISTRY*
