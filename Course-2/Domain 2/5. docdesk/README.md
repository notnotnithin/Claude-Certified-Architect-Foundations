# Demo 5 — Built-in Tools: Grep, Glob, Read, Write, Edit (DocDesk)

The final demo in **Domain 2: Tool Design & MCP Integration**. It teaches the
five **built-in tools** Claude Code uses to explore and edit a codebase — and,
most importantly, **which tool to pick for which job.**
Maps to **Task Statement 2.5 — Select and apply built-in tools effectively.**

> **One tool at a time.** Unlike other demos, this one has **five tiny scripts —
> one per tool.** You run one, teach that tool, read its self-explaining output,
> then move to the next. No API key, no `pip install`, no `.env`. Pure Python
> standard library — it runs instantly and offline.

> **These are teaching stand-ins.** The real Grep/Glob/Read/Write/Edit live
> *inside Claude Code*, and you can't call them from an outside script. So each
> script here rebuilds a tiny honest version of the tool, so you can SEE its
> behaviour. In real Claude Code you never write these — Claude picks them for
> you. What matters for the exam is knowing **which tool is the right choice.**

---

## The five tools at a glance

| Tool | What it does | Reach for it when... |
|------|--------------|----------------------|
| **Glob** | finds files by their **name** | you want files by name/type (all test files, all `.md`) |
| **Grep** | finds **text inside** files | you want to find WHERE some text appears (a function, an error) |
| **Read** | opens **one whole file** | you've found the file and want to understand it |
| **Write** | creates or **replaces a whole file** | you're making a new file or replacing one entirely |
| **Edit** | changes a **small part** of a file (by unique text) | you want a targeted tweak and the target text is unique |

---

## How to run — one command per tool

Run them in this order (each is standalone and safe to re-run):

```bash
python glob_demo.py     # Tool 1: find files by name
python grep_demo.py     # Tool 2: find text inside files
python read_demo.py     # Tool 3: open one whole file
python write_demo.py    # Tool 4: create/replace a whole file
python edit_demo.py     # Tool 5: change a small part (+ the fallback rule)
```

Each script prints the same simple shape:
**what the tool does → what I'm asking it → the result → when to use it.**
So the output explains itself — you can read it aloud as you teach.

---

## What each script shows (and how to explain the output)

### `glob_demo.py` — Glob (find files by NAME)
Asks two things: "find all test files" and "find every Python file."
The output is a **list of file names**. Point out: Glob only looked at
*names* — it never opened the files.
**Lesson:** use Glob when you know the file's name or type.

### `grep_demo.py` — Grep (find TEXT inside files)
Asks: "where does `search_documents` appear?" and "where is the message
`No matching documents`?" The output shows **file : line : the matching text**.
Point out: Grep looked *inside* the files.
**Lesson:** use Grep when you know the text but not which file it's in.

### `read_demo.py` — Read (open ONE file)
Asks: "open `docdesk/store.py`." The output is the **whole file with line
numbers**. Point out: you use Read *after* Grep/Glob told you which file.
**Lesson:** Grep/Glob find the file; Read opens it.

### `write_demo.py` — Write (create/replace a whole file)
Asks: "create `scratch.txt` with a shopping list." It **really creates the
file** — open `scratch.txt` in the folder to prove it. The output shows the new
contents.
**Lesson:** use Write to make a new file or replace one completely.

### `edit_demo.py` — Edit (small change) + the fallback
This is the most important one. It uses a real file `scratch_edit.txt` and shows
**two cases**:
- **Case 1 — unique text:** change `owner: team-a` → `owner: team-b`. The text
  appears once, so **Edit works.**
- **Case 2 — non-unique text:** change `status: active` → `status: paused`, but
  that text appears **twice**. **Edit refuses** (it can't tell which one), so the
  script **falls back to Read + Write** (read the whole file, change it, write it
  back).

**Lesson:** Edit needs a **unique** anchor. If the text isn't unique, use
Read + Write instead.

---

## The two decisions the exam tests most

**1. Grep vs Glob — contents vs filename.**
- Searching *inside* files (find callers of a function) → **Grep**.
- Finding files *by name* (all `**/*.test.tsx`) → **Glob**.

**2. Edit vs Read+Write — the fallback rule.**
- **Edit** needs a **unique** piece of text to anchor the change.
- If that text appears more than once, Edit can't run → **Read + Write** instead.

Also good to know: a smart way to explore a big codebase is **Grep to find an
entry point, then Read that file and follow its imports** — instead of reading
every file up front.

---

## Files

| File | Job |
|------|-----|
| `glob_demo.py` | Tool 1 — Glob (find files by name). |
| `grep_demo.py` | Tool 2 — Grep (find text inside files). |
| `read_demo.py` | Tool 3 — Read (open one whole file). |
| `write_demo.py` | Tool 4 — Write (create/replace a whole file; makes `scratch.txt`). |
| `edit_demo.py` | Tool 5 — Edit + Read/Write fallback (uses `scratch_edit.txt`). |
| `sample_repo/` | A tiny codebase (`docdesk/` + `tests/`) the Glob/Grep/Read demos explore. |
| `.gitignore` | Ignores the generated scratch files. |

`requirements.txt` (outside) needs nothing — pure standard library.

The `write_demo.py` and `edit_demo.py` scripts only ever create/modify
`scratch.txt` and `scratch_edit.txt` in this folder. They **never** touch the
`sample_repo` files, so everything is safe to run as many times as you like.

---

## Key takeaways

- **Glob = filenames. Grep = contents.** (The most common exam distinction.)
- **Read** opens a file you've found; **Write** creates/replaces a whole file.
- **Edit** needs a **unique** anchor; if not unique, **Read + Write**.
- In real Claude Code you don't call these — Claude does. Your job (and the
  exam's) is knowing **which choice is correct**.
