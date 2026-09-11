# Part 1 — Live Demo Prompts (run inside Claude Code)

This file gives you the exact prompts to type **inside Claude Code**, in order.
Each prompt shows one concept from Tasks 3.1 and 3.3. Read the explanation, type
the prompt, and watch Claude respond.

> **How to work:** open this file and the `README.md` in **VS Code** to read.
> Type the prompts in **Claude Code** (started from **cmd**). Start Claude Code
> from inside the `2. tripplanner` folder:
>
> ```cmd
> cd C:\path\to\DOMAIN 3\2. tripplanner
> claude
> ```

---

## Demo 1 — See the CLAUDE.md hierarchy with `/memory`

Claude Code loads memory from up to three levels. The built-in `/memory` command
lists them. Inside Claude Code, type:

```
/memory
```

**What to look for:** it lists the memory files currently loaded. You should see:

- the **project-level** `CLAUDE.md` (at the root of `2. tripplanner`), and
- the **directory-level** `CLAUDE.md` (inside `destinations/`) when relevant, and
- the **user-level** `CLAUDE.md` **if** you set one up (see the
  `user-level-CLAUDE-template` folder).

This is the single clearest way to *show* the hierarchy. Everything else in this
demo builds on it.

---

## Demo 2 — Prove the PROJECT-LEVEL file is loaded

Ask Claude directly:

```
Which CLAUDE.md files are you currently using, and what does the project-level one tell you?
```

**What to look for:** Claude names the project-level `CLAUDE.md` and repeats its
standards (Python 3.8+, docstrings, raise ValueError on bad input, utf-8, the
parsing -> destinations -> storage layering). That proves the project-level memory
loaded and is guiding Claude.

---

## Demo 3 — See the `@import` expand

Our project `CLAUDE.md` ends with `@standards/dates.md`. Ask:

```
What date-format rules are you following, and which file do they come from?
```

**What to look for:** Claude explains the `YYYY-MM-DD` rule and says it comes from
`standards/dates.md`, which the project `CLAUDE.md` pulls in with `@import`. This
shows how imports keep the main memory file short while still loading the details.

---

## Demo 4 — See the DIRECTORY-LEVEL file (only inside `destinations/`)

The `destinations/` folder has its OWN `CLAUDE.md` with extra rules. Ask Claude to
work there:

```
I'm about to add a new function in destinations/stops.py. What extra rules apply in the destinations folder specifically?
```

**What to look for:** Claude mentions the directory-level rules — e.g. every
stop-related function needs a one-line usage example in its docstring, place names
stored trimmed, no abbreviations. These are the rules from
`destinations/CLAUDE.md`.

Now contrast with a different folder:

```
And if I edit storage/trip_store.py instead, do those destinations rules still apply?
```

**What to look for:** Claude explains the destinations rules do **not** apply in
`storage/` — directory-level memory only applies inside its own folder. That is
the whole point of the third level.

---

## Demo 5 — See a PATH-SCOPED rule switch on (test files)

We have a rule, `.claude/rules/testing.md`, scoped to `paths: ["**/test_*.py"]`.
It should apply to any test file, wherever it lives. Ask:

```
Add a new test to tests/test_stops.py that checks make_stop rejects zero nights. Follow our testing conventions.
```

**What to look for:** Claude writes a single-behaviour test with a clear name, a
happy/sad path style, matching the conventions in `testing.md`. The rule switched
on because the file matches the glob.

Now the key moment — a test file in a **different folder**:

```
Now add a similar test to destinations/test_date_beside_module.py. Same conventions.
```

**What to look for:** Claude follows the **same** testing conventions, even though
this file is in `destinations/`, not `tests/`. One glob rule (`**/test_*.py`)
covers test files **wherever they live** — something a folder-bound CLAUDE.md
could not do cleanly. This is the headline lesson of Task 3.3.

---

## Demo 6 — See a path rule stay OFF when it shouldn't apply

Ask Claude to touch a plain, non-test file outside `storage/`:

```
In destinations/stops.py, are the storage-folder rules or the testing rules active right now?
```

**What to look for:** Claude explains that neither the `storage/**/*.py` rule nor
the `**/test_*.py` rule applies to `destinations/stops.py`. Path rules load **only**
for files they match, which keeps Claude focused and saves tokens. Rules staying
*off* is just as important as them switching *on*.

---

## Quick recap of what each prompt proved

| Demo | Prompt shows | Concept |
|------|--------------|---------|
| 1 | `/memory` lists loaded files | The hierarchy (user/project/directory) |
| 2 | Claude repeats project standards | Project-level CLAUDE.md |
| 3 | Claude cites `standards/dates.md` | `@import` |
| 4 | Extra rules only in `destinations/` | Directory-level CLAUDE.md |
| 5 | Same test rule in two folders | Path-scoped glob rule (by name) |
| 6 | No rule applies to a plain file | Rules load only when matching |

---

*CCA-Foundations · Domain 3 · TripPlanner · ANKIT MISTRY*
