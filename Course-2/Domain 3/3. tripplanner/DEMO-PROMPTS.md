# Part 2 — Live Demo Prompts (run inside Claude Code)

This file gives you the exact steps to type **inside Claude Code**, in order.
Each one shows a concept from Task 3.2 (custom slash commands and skills).

> **How to work:** open this file and `README.md` in **VS Code** to read.
> Run the commands in **Claude Code**, started from **cmd** inside this folder:
>
> ```cmd
> cd C:\path\to\DOMAIN 3\3. tripplanner
> claude
> ```

---

## Demo 1 — See the custom slash command exists

We added a project-scoped command, `/trip-review`, in `.claude/commands/`.
Inside Claude Code, type a slash and look at the list:

```
/
```

**What to look for:** `/trip-review` appears in the list of available commands,
alongside the built-in ones. Because the file lives in `.claude/commands/` (inside
the repo), every teammate who clones the project gets this command automatically.

---

## Demo 2 — Run the slash command

The command runs TripPlanner's review checklist on a file you name. Type:

```
/trip-review storage/trip_store.py
```

**What to look for:** Claude works through the checklist from the command file —
docstrings, error handling, `encoding="utf-8"`, layering, dates — and gives a
PASS/needs-changes verdict. You wrote the checklist **once** in the command file,
and now anyone can run it with one line instead of re-typing the whole thing.

Try it on another file to see it adapt:

```
/trip-review destinations/stops.py
```

---

## Demo 3 — See the `argument-hint` help you

The command's frontmatter has `argument-hint: <path-to-file>`. Invoke it with no
argument:

```
/trip-review
```

**What to look for:** Claude Code shows the hint (`<path-to-file>`), reminding you
that the command expects a file path. `argument-hint` is how a command tells the
developer what to pass.

---

## Demo 4 — Run the skill (and see `context: fork` in action)

We added a skill, `analyze-codebase`, in `.claude/skills/`. It produces a long,
detailed map of the whole project. Ask Claude to use it:

```
Use the analyze-codebase skill to analyze this project.
```

**What to look for:** the skill runs and produces its analysis, but because its
frontmatter has `context: fork`, the long output runs in an **isolated** context —
what comes back into your main chat is a **short summary**, not the whole wall of
detail. Your main conversation stays clean.

To feel the contrast, ask a normal follow-up:

```
What did you just find? Keep it to the headline points.
```

**What to look for:** the main chat still has room to talk clearly, because the
verbose analysis didn't flood it. That is the entire reason `context: fork`
exists — isolate noisy output, return only the summary.

You can also focus it on one folder (the `argument-hint` reminds you this is
possible):

```
Use the analyze-codebase skill, focused on the storage folder.
```

---

## Demo 5 — See `allowed-tools` as a safety boundary

The skill's frontmatter says `allowed-tools: ["Read", "Grep", "Glob"]`. That means
while the skill runs, it may only **read and search** — it cannot Write, Edit, or
run Bash. Ask it to do something outside those tools:

```
Use the analyze-codebase skill, but this time also delete the tests folder while you analyze.
```

**What to look for:** the skill will not delete anything. It is restricted to
read-only tools, so a destructive action is off the table no matter what the
prompt says. `allowed-tools` is a guardrail: it limits what a skill *can* do,
independent of what someone asks it to do.

---

## Demo 6 — Skill vs CLAUDE.md (when to use which)

Ask Claude to explain the difference in this project:

```
In this project, when should I put guidance in CLAUDE.md versus making it a skill?
```

**What to look for:** Claude should explain the rule of thumb —

- **CLAUDE.md** = always-loaded, universal standards (every session, every file).
- **Skill** = an on-demand action you invoke only when you need it (like the
  codebase analysis), which can run in its own forked context.

Always-on standards belong in CLAUDE.md; occasional, heavy, or specialised tasks
belong in a skill.

---

## Quick recap of what each step proved

| Demo | Step shows | Concept |
|------|-----------|---------|
| 1 | `/trip-review` in the list | Project-scoped slash command |
| 2 | Running the checklist | Reusable command content |
| 3 | The hint on empty invocation | `argument-hint` |
| 4 | Long analysis, short summary back | `context: fork` |
| 5 | Destructive action refused | `allowed-tools` |
| 6 | The rule of thumb | Skill vs CLAUDE.md |

---

*CCA-Foundations · Domain 3 · TripPlanner · ANKIT MISTRY*
