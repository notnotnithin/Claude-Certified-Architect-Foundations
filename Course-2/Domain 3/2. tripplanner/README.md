# Part 1 — Memory & Rules

### Domain 3: Claude Code Configuration & Workflows · Tasks 3.1 + 3.3

---

## Where we are

In **Part 0** (`1. tripplanner`) you installed Claude Code and ran the TripPlanner
app. This is **Part 1** (`2. tripplanner`). The Python app is **exactly the same**
— we did not change a single line of it. What's new is a layer of **configuration
files** that teach Claude Code how to behave on this project.

> **Read** the explanations in **VS Code** (this file and `DEMO-PROMPTS.md`).
> **Run** the demo by typing prompts inside **Claude Code**.

---

## The one big idea of Part 1

> **How does Claude Code decide which instructions to follow?**

When you open Claude Code in a project, it reads a set of **memory** and **rule**
files and follows them. Part 1 is about writing those files correctly so that:

- the whole team automatically gets the project's standards, and
- the *right* rules load for the *right* files.

This covers two exam task statements at once:

- **Task 3.1** — CLAUDE.md hierarchy, `@import`, `.claude/rules/`, `/memory`.
- **Task 3.3** — path-specific rules with glob patterns.

---

## The CLAUDE.md hierarchy — three levels

`CLAUDE.md` is a plain-English file that tells Claude Code how to work. There are
**three levels**, and they all load together (lower levels add to higher ones):

```
   USER-LEVEL       ~/.claude/CLAUDE.md            your machine, every project
        +
   PROJECT-LEVEL    CLAUDE.md  (at project root)   committed, whole team
        +
   DIRECTORY-LEVEL  destinations/CLAUDE.md         only inside that folder
```

| Level | Lives where | Shared with the team? | Applies to |
|-------|-------------|----------------------|-----------|
| **User** | your home folder (`~/.claude/`) | ❌ No — personal | every project you open |
| **Project** | the repo root | ✅ Yes — committed to git | the whole project |
| **Directory** | a subfolder in the repo | ✅ Yes | only that folder |

This Part 1 folder gives you **all three**:

- **Project-level:** `CLAUDE.md` at the root of `2. tripplanner`.
- **Directory-level:** `destinations/CLAUDE.md` (extra rules just for that folder).
- **User-level:** a ready-to-use template in `user-level-CLAUDE-template/`, which
  you copy into your home folder (see below).

---

## Where is the user-level CLAUDE.md, and how do I create it?

It lives in your home folder, **outside** any project:

```
Windows :  C:\Users\<YourName>\.claude\CLAUDE.md
Mac/Linux: ~/.claude/CLAUDE.md
```

The `.claude` folder is created when you install Claude Code. The `CLAUDE.md`
inside it usually does **not** exist yet — you create it. The easiest way is to
start Claude Code, run `/memory`, and choose the **user** option, which
opens/creates the file for you. Full step-by-step instructions and a ready-made
template are in the **`user-level-CLAUDE-template/`** folder.

---

## Modular memory with `@import`

A giant CLAUDE.md is hard to maintain. The `@import` syntax keeps it short by
pulling in other files. Look at the bottom of `CLAUDE.md`:

```
@standards/dates.md
```

That line pulls in `standards/dates.md` when Claude loads the project memory, so
the date rules live in one reusable file. Open `standards/dates.md` in VS Code to
see what gets imported.

---

## Path-specific rules with globs (Task 3.3)

Some conventions only matter for **certain files**. Our testing conventions only
matter for **test files** — but test files are spread across the project (some in
`tests/`, one beside its code in `destinations/test_date_beside_module.py`).

A directory-level CLAUDE.md can't handle that cleanly: a file in `tests/` wouldn't
cover the test inside `destinations/`. The clean solution is a rule file with a
**glob pattern**. Open `.claude/rules/testing.md`:

```yaml
---
paths: ["**/test_*.py"]
---
```

`**/test_*.py` means "any `test_*.py` file, in any folder." So this **one** rule
covers **every** test file, wherever it lives — and it does **not** load for
non-test files.

We also ship `.claude/rules/storage.md`, scoped by **location**:

```yaml
---
paths: ["storage/**/*.py"]
---
```

- `**/test_*.py` → select files by **name**, wherever they are.
- `storage/**/*.py` → select files by **location**.

---

## Your folder layout

```
2. tripplanner/
├── CLAUDE.md                       ← PROJECT-LEVEL memory (+ @import)
├── standards/
│   └── dates.md                    ← imported by CLAUDE.md
├── .claude/
│   └── rules/
│       ├── testing.md              ← path rule: **/test_*.py  (by name)
│       └── storage.md              ← path rule: storage/**/*.py (by location)
├── destinations/
│   └── CLAUDE.md                   ← DIRECTORY-LEVEL memory (folder-only)
├── user-level-CLAUDE-template/     ← USER-LEVEL template + how-to
│   ├── CLAUDE.md
│   └── HOW-TO-INSTALL.md
├── DEMO-PROMPTS.md                 ← the prompts to type in Claude Code
├── README.md                       ← this guide
│
│   ── unchanged app code from Part 0 ──
├── cli.py
├── destinations/  (stops.py, test_date_beside_module.py, ...)
├── parsing/
├── storage/
├── tests/
└── .gitignore
```

`requirements.txt` and `venv` stay in the `DOMAIN 3` root, outside this folder.

---

## How to run the demo

Everything in Part 1 is demonstrated by typing prompts **inside Claude Code** — so
students see the concepts live, not through a helper script.

1. Open a terminal (cmd) and go into the folder:

   ```cmd
   cd C:\path\to\DOMAIN 3\2. tripplanner
   ```

2. (Optional but recommended) set up your user-level file first — see
   `user-level-CLAUDE-template/HOW-TO-INSTALL.md`.

3. Start Claude Code:

   ```cmd
   claude
   ```

4. Open **`DEMO-PROMPTS.md`** and type each prompt in order. It walks through:
   - `/memory` to see the hierarchy,
   - proving the project-level file loaded,
   - watching the `@import` expand,
   - seeing the directory-level rules apply only in `destinations/`,
   - a path rule switching on for test files in two different folders,
   - and a path rule staying off for a plain file.

---

## Exam objective coverage

**Task 3.1 — CLAUDE.md hierarchy, scoping, modular organization**

- ✅ Hierarchy: **user / project / directory** — all three exist as real files and
  are shown live via `/memory` and prompts.
- ✅ User-level not shared via version control: explained, with a template you
  install into your home folder.
- ✅ `@import` for modular CLAUDE.md: `@standards/dates.md`, shown in Demo 3.
- ✅ `.claude/rules/` as an alternative to a monolithic CLAUDE.md: the rules folder.
- ✅ Diagnosing hierarchy issues: `/memory` shows exactly which files load.
- ✅ Using `@import` to include relevant standards: the dates file.
- ✅ Splitting CLAUDE.md into topic files in `.claude/rules/`: `testing.md`,
  `storage.md`.
- ✅ Using `/memory` to verify loaded files: Demo 1.

**Task 3.3 — Path-specific rules for conditional convention loading**

- ✅ `.claude/rules/` files with YAML `paths` globs: both rule files.
- ✅ Path rules load only when editing matching files: Demo 6.
- ✅ Glob rules beat directory CLAUDE.md for conventions spanning directories:
  Demo 5 (same rule, two folders).
- ✅ Creating rules with `paths:` scoping: `testing.md`, `storage.md`.
- ✅ Globs applying by file type regardless of location (`**/test_*.py`): Demo 5.
- ✅ Choosing path rules over subdirectory CLAUDE.md when files are spread out:
  explained in the path-rules section.

---

## What's next

**Part 2 — Commands & skills (Task 3.2).** We add reusable actions: a
`/trip-review` slash command in `.claude/commands/`, and a skill in
`.claude/skills/` with `context: fork`, `allowed-tools`, and `argument-hint`.

See you in Part 2.

---

*CCA-Foundations · Domain 3 · Part 1 — ANKIT MISTRY*
