# Part 2 — Commands & Skills

### Domain 3: Claude Code Configuration & Workflows · Task 3.2

---

## Where we are

- **Part 0** (`1. tripplanner`) — installed Claude Code, ran the app.
- **Part 1** (`2. tripplanner`) — memory & rules (CLAUDE.md hierarchy, `@import`,
  path rules).
- **Part 2** (`3. tripplanner`, this folder) — **commands & skills**.

The Python app is still **unchanged**, and Part 1's config (CLAUDE.md, standards,
`.claude/rules/`, the directory-level file) is **carried forward**. Part 2 adds two
new kinds of configuration on top: a **slash command** and a **skill**.

> **Read** in **VS Code** (this file and `DEMO-PROMPTS.md`).
> **Run** by typing in **Claude Code**.

---

## The one big idea of Part 2

> **Reusable actions you invoke on demand.**

Part 1 was about instructions Claude *always* follows. Part 2 is about actions you
**call when you want them**:

- a **slash command** — a saved prompt you run with `/name`, like `/trip-review`.
- a **skill** — a packaged task with its own settings, like `analyze-codebase`.

This is all of **Task 3.2**.

---

## Concept 1 — Custom slash commands

A slash command is a saved instruction you invoke with `/name`. Ours lives in:

```
.claude/commands/trip-review.md
```

Because it sits in `.claude/commands/` **inside the repo**, it is shared through
version control — every teammate who clones TripPlanner gets `/trip-review`
automatically. (A personal command would go in `~/.claude/commands/` instead, and
would **not** be shared.)

| Command location | Shared with the team? |
|------------------|----------------------|
| `.claude/commands/` (in the repo) | ✅ Yes — project-scoped |
| `~/.claude/commands/` (home folder) | ❌ No — personal |

Open `trip-review.md` in VS Code. Notice the frontmatter at the top:

```yaml
---
description: Run TripPlanner's standard code-review checklist on a file
argument-hint: <path-to-file>
---
```

- `description` — the one-line summary shown in the command list.
- `argument-hint` — tells the developer what to pass (here, a file path). If you
  run `/trip-review` with no argument, Claude Code shows this hint.

The body is the actual checklist. You write it **once**; anyone runs it with one
line.

---

## Concept 2 — Skills

A skill is a packaged task with its own configuration. Ours lives in:

```
.claude/skills/analyze-codebase/SKILL.md
```

It produces a full structural map of the project — deliberately **verbose**. Open
it in VS Code and look at the frontmatter, because every line teaches a concept:

```yaml
---
name: analyze-codebase
description: Produce a full structural analysis of the TripPlanner project...
context: fork
allowed-tools: ["Read", "Grep", "Glob"]
argument-hint: [optional-folder-to-focus-on]
---
```

### `context: fork` — isolate verbose output

This is the key idea. `context: fork` runs the skill in an **isolated sub-agent
context**. The long analysis it produces does **not** pollute your main chat — only
a short summary comes back. Without `fork`, that wall of detail would fill your main
conversation and crowd out everything else. With `fork`, your main chat stays clean.

This is exactly why a *codebase analysis* is the perfect skill for `fork`: it's
noisy on purpose, and you only want the summary back.

### `allowed-tools` — a safety boundary

```yaml
allowed-tools: ["Read", "Grep", "Glob"]
```

While the skill runs, it may only **read and search**. It cannot Write, Edit, or run
Bash. A read-only analysis skill has no business changing files, so we lock it down.
Even if someone asks the skill to delete a folder, it can't — the tools simply aren't
available to it.

### `argument-hint` — prompt for parameters

```yaml
argument-hint: [optional-folder-to-focus-on]
```

Reminds the developer they can pass a folder to narrow the analysis.

---

## Concept 3 — Skill vs CLAUDE.md (when to use which)

Both shape Claude's behaviour, but they're for different things:

| | CLAUDE.md | Skill |
|--|-----------|-------|
| When it loads | **always** (every session) | **on demand** (when you invoke it) |
| Good for | universal standards | occasional, heavy, or specialised tasks |
| Example | "always use utf-8" | "analyze the whole codebase" |

Rule of thumb: **always-on standards → CLAUDE.md. Occasional actions → a skill.**

---

## Your folder layout

```
3. tripplanner/
├── .claude/
│   ├── commands/
│   │   └── trip-review.md          ← NEW: /trip-review slash command
│   ├── skills/
│   │   └── analyze-codebase/
│   │       └── SKILL.md            ← NEW: skill with context: fork, allowed-tools
│   └── rules/                       ← from Part 1 (testing.md, storage.md)
├── CLAUDE.md                        ← from Part 1 (project-level)
├── standards/dates.md               ← from Part 1 (imported)
├── destinations/CLAUDE.md           ← from Part 1 (directory-level)
├── user-level-CLAUDE-template/      ← from Part 1 (reference)
├── DEMO-PROMPTS.md                  ← the prompts to type in Claude Code
├── README.md                        ← this guide
│
│   ── unchanged app code ──
├── cli.py
├── destinations/  parsing/  storage/  tests/
└── .gitignore
```

`requirements.txt` and `venv` stay in the `DOMAIN 3` root, outside this folder.

---

## How to run the demo

1. Open cmd and go into the folder:

   ```cmd
   cd C:\path\to\DOMAIN 3\3. tripplanner
   ```

2. Start Claude Code:

   ```cmd
   claude
   ```

3. Open **`DEMO-PROMPTS.md`** and follow it in order. It walks through:
   - seeing `/trip-review` in the command list and running it,
   - the `argument-hint` showing when you invoke with no argument,
   - running the `analyze-codebase` skill and watching `context: fork` return only
     a short summary,
   - `allowed-tools` refusing a destructive action,
   - and the skill-vs-CLAUDE.md rule of thumb.

---

## Exam objective coverage

**Task 3.2 — Create and configure custom slash commands and skills**

- ✅ Project-scoped commands in `.claude/commands/` vs user-scoped in
  `~/.claude/commands/`: explained in Concept 1, `/trip-review` is project-scoped.
- ✅ Skills in `.claude/skills/` with `SKILL.md` frontmatter: `analyze-codebase`.
- ✅ `context: fork` for isolated sub-agent context: Concept 2 + Demo 4.
- ✅ `allowed-tools` to restrict tool access: Concept 2 + Demo 5.
- ✅ `argument-hint` to prompt for parameters: both the command and the skill; Demo 3.
- ✅ Creating project-scoped slash commands for team-wide availability: `/trip-review`.
- ✅ Using `context: fork` to isolate verbose output: the codebase-analysis skill.
- ✅ Configuring `allowed-tools` to prevent destructive actions: read-only tool set.
- ✅ Choosing skills (on-demand) vs CLAUDE.md (always-loaded): Concept 3 + Demo 6.

---

## What's next

**Part 3 — Plan mode & iterative refinement (Tasks 3.4 + 3.5).** When to let Claude
plan a big change vs just do a small one, and how to steer it with concrete
input/output examples — including the one demo in this domain that calls the real
Claude API.

See you in Part 3.

---

*CCA-Foundations · Domain 3 · Part 2 — ANKIT MISTRY*
