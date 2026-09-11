# Part 0 — Setup & First Run

### Domain 3: Claude Code Configuration & Workflows · The TripPlanner Project

---

## Welcome

This is **Part 0** of our Domain 3 journey. Across this domain we build one small
Python project — **TripPlanner** — and slowly configure **Claude Code** around it,
learning every Domain 3 exam concept along the way.

Part 0 has one job: **get you from nothing to a working setup.**

By the end of this part you will have:

1. Claude Code installed and logged in.
2. The TripPlanner project open in VS Code.
3. The TripPlanner app running in your terminal (cmd).
4. Claude Code reading the project for the first time.

There is **no exam objective in Part 0** — it is the on-ramp. The real exam
concepts start in Part 1. But a clean setup here makes every later part smooth.

> **How to use this course (important):**
> You will **read** all the explanations here in **VS Code** (this `README.md`
> file), and you will **run** the commands in **Windows Command Prompt (cmd)**.
> Read in VS Code, run in cmd. That pattern repeats in every part.

---

## The two tools, in plain words

Before we install anything, let's be clear about two different things, because
beginners often mix them up.

- **VS Code** is a text editor. It's where you *read and write files*. Think of
  it as a very smart notepad for code.
- **Claude Code** is a separate AI assistant that runs *in your terminal*. You
  talk to it in plain English ("add a validation check", "explain this file")
  and it reads and edits your project files for you.

They are different programs. In this course you use VS Code to read the lessons,
and Claude Code (plus plain Python) in the terminal to do the work.

> There is also a **VS Code extension** for Claude Code that puts it inside the
> editor. We use the **terminal** version in this course because Domain 3 is all
> about configuration files and commands, and the terminal makes those visible.

---

## What Domain 3 is really about (the big picture)

Here is the mental model for the whole domain. Keep it in your head:

> **Claude Code is only as good as the configuration you give it.**

Out of the box, Claude Code is a capable assistant that reads your code. But on a
*real team*, you want it to:

- know your project's coding standards **automatically** (Part 1),
- offer **reusable commands** everyone can run, like `/trip-review` (Part 2),
- know **when to plan** a big change vs just doing a small one, and how you
  **steer** it toward the output you want (Part 3),
- run **without a human** inside your CI/CD pipeline (Part 4).

Every one of those is a *configuration* skill, not a coding skill. That's why we
need only a tiny app underneath. TripPlanner is that tiny app.

Here's the road map for the whole domain:

```
   Part 0  ──►  Setup & first run              (you are here)
   Part 1  ──►  Memory & rules                 (Tasks 3.1 + 3.3)
   Part 2  ──►  Commands & skills              (Task 3.2)
   Part 3  ──►  Plan mode & refinement         (Tasks 3.4 + 3.5)
   Part 4  ──►  CI/CD                           (Task 3.6)
```

---

## Meet TripPlanner

TripPlanner is a **tiny command-line app** that remembers the stops on a trip.
You add a place with a date and how many nights you'll stay; it saves your trip
and can list it back in date order.

Asha is planning a trip and uses TripPlanner to keep her stops organised. That's
the whole app. It is deliberately small — **the point of Domain 3 is configuring
Claude Code, not building a big program.**

### How the project is laid out

```
tripplanner/
├── cli.py                  ← the commands you type (add, list)
├── destinations/
│   ├── stops.py            ← builds and validates one stop
│   └── test_date_beside_module.py   ← a test sitting NEXT TO its code
├── storage/
│   └── trip_store.py       ← saves/loads the trip as JSON
├── parsing/
│   └── free_text.py        ← turns your text into a stop (upgraded in Part 3)
├── tests/
│   └── test_stops.py       ← tests in the usual tests/ folder
└── .gitignore
```

Two small design choices matter for later parts, so notice them now:

1. **The job is split into small modules** (`parsing` → `destinations` →
   `storage`). This gives Claude Code predictable places to look. In Part 1 we
   attach different rules to different folders.
2. **Test files live in two places** — some in `tests/`, and one *beside* the
   code it tests (`destinations/test_date_beside_module.py`). Real projects look
   like this. In Part 1 (Task 3.3) we use a single glob rule,
   `paths: ["**/test_*.py"]`, that catches test files **wherever they live** —
   something a folder-bound file cannot do cleanly. That scattered test file is
   deliberate proof.

You don't need to memorise the code. Just know what each folder is *for*.

---

## Step 1 — Check your prerequisites

Open **Command Prompt (cmd)** and check the two basics.

**a) Python** (the app is written in Python):

```cmd
python --version
```

You want Python **3.8 or higher** (for example `Python 3.12.3`). If you see
`'python' is not recognized`, install Python from https://www.python.org/ and
tick **"Add Python to PATH"** during install.

**b) A terminal you're comfortable in.** We use **cmd** throughout. Everything
also works in PowerShell, but the exact commands for setting variables differ, so
we stick to cmd to keep things predictable.

---

## Step 2 — Install Claude Code

> Claude Code details change often, so if anything below looks different on your
> machine, the official guide is the source of truth:
> **https://code.claude.com/docs** (Setup page).

There are **two ways** to install on Windows. Pick one.

### Option A — Native installer (simplest, no Node.js)

The native installer is self-contained — it does **not** need Node.js. In
**PowerShell** (just for this one command), run:

```powershell
irm https://claude.ai/install.ps1 | iex
```

Or in **cmd**:

```cmd
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

### Option B — npm (if you already use Node.js)

If you already have **Node.js 22 or later**, you can install via npm:

```cmd
npm install -g @anthropic-ai/claude-code
```

Check your Node version first with `node --version`. Older versions may print a
warning; 22+ avoids it.

### A note for WSL2 users

If you develop inside **WSL2** (Ubuntu on Windows), install Claude Code *inside*
your WSL environment, and keep your project inside the WSL filesystem (e.g.
`~/projects/tripplanner`) rather than under `/mnt/c/...`. File operations are
faster and avoid line-ending issues. Everything in this course works the same in
a WSL terminal as in cmd.

### Verify the install

Close and reopen your terminal, then run:

```cmd
claude --version
```

Seeing a version number means Claude Code is installed. If you get "not
recognized", close **all** terminal windows and open a fresh one so your PATH
refreshes, then try again. You can also run `claude doctor` to check the health
of your install.

---

## Step 3 — Log in

Claude Code needs an Anthropic account (a Claude Pro/Max subscription, or API
credits). Start the login flow:

```cmd
claude
```

The first time, it walks you through authentication — usually opening your
browser to log in to your Anthropic account. Follow the prompts. Once you're
logged in, you'll land at the Claude Code prompt (a `>` waiting for your
instruction). Type `/exit` to leave it for now.

> If your team uses an API key instead, you can set `ANTHROPIC_API_KEY` as an
> environment variable. For personal use, the browser login is simplest.

---

## Step 4 — Open TripPlanner in VS Code

1. Unzip the Part 0 folder somewhere easy to find, e.g. `C:\cca\`.
2. Open **VS Code**.
3. **File → Open Folder…** and choose the `tripplanner` folder.
4. You should see the folder tree on the left, matching the layout above.

Reading the code in VS Code (with its colours and file tree) is much easier than
reading it in a terminal. This is your "read" tool.

---

## Step 5 — Run TripPlanner in cmd

Now the fun part — see the app work. Open **cmd**, and move into the project
folder (adjust the path to wherever you unzipped it):

```cmd
cd C:\cca\tripplanner
```

**Ask for help** (no arguments):

```cmd
python cli.py
```

You'll see:

```
TripPlanner - a tiny trip itinerary tracker

Commands:
   python cli.py add "<place> <YYYY-MM-DD> <nights>"   Add a stop
   python cli.py list                                 Show the trip
```

**List the trip** (it's empty at first):

```cmd
python cli.py list
```

```
Your trip is empty. Add a stop, for example:
   python cli.py add "Jaipur 2026-10-02 3"
```

**Add a few stops:**

```cmd
python cli.py add "Jaipur 2026-10-02 3"
python cli.py add "Goa 2026-10-05 2"
python cli.py add "Udaipur 2026-09-28 1"
```

Each one confirms:

```
Added: 3 night(s) in Jaipur from 2026-10-02
Added: 2 night(s) in Goa from 2026-10-05
Added: 1 night(s) in Udaipur from 2026-09-28
```

**List the trip again:**

```cmd
python cli.py list
```

```
Your trip:
----------------------------------------
1. Udaipur
   arrive 2026-09-28, stay 1 night(s)
2. Jaipur
   arrive 2026-10-02, stay 3 night(s)
3. Goa
   arrive 2026-10-05, stay 2 night(s)
----------------------------------------
Total stops: 3
```

Notice Udaipur jumped to the top — the app **sorts by date**, so the trip reads
in the order you'll actually travel. Your stops are saved in a new file,
`my_trip.json`, which you can open in VS Code to see the raw data.

### See the friendly error handling

TripPlanner checks your input and explains problems instead of crashing:

```cmd
python cli.py add "Jaipur 02-10-2026 3"
```

```
Could not add that stop.
   Date must look like YYYY-MM-DD (example: 2026-10-02), got: '02-10-2026'
```

That clear-error habit matters later: in Part 3 we point to this exact date check
as an example of a **small, well-scoped change** (direct execution) versus a big
architectural one (plan mode).

---

## Step 6 — Let Claude Code read the project

Now connect the two. From inside `tripplanner`, start Claude Code:

```cmd
claude
```

At the prompt, ask it something simple about the project — in plain English:

```
> What does this project do? Give me a two-line summary.
```

Claude Code will read the files and answer. Try one more:

```
> Which file is responsible for saving the trip to disk?
```

It should point you to `storage/trip_store.py`. That's the whole idea of Claude
Code: you ask in plain English, it reads your actual files and answers. Type
`/exit` when you're done.

**You've now done everything Part 0 needed.** Claude Code is installed, logged in,
and reading TripPlanner; the app runs; and the project is open in VS Code.

---

## Optional — set up a virtual environment (recommended)

A **virtual environment** ("venv") keeps this project's Python packages separate
from the rest of your system. Part 0 needs no packages, but Part 3 will, so
setting this up now saves time.

From the folder that contains `requirements.txt` (one level **above**
`tripplanner`):

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Your prompt will show `(.venv)` when the environment is active. To turn it off,
type `deactivate`. If `pip install` fails because you're offline, don't worry —
Part 0 and the app don't need those packages; they're only for Part 3.

---

## What's in this folder

| File / folder | What it is |
|---|---|
| `README.md` | This guide (you're reading it) |
| `requirements.txt` | Python packages for later parts (not needed yet) |
| `tripplanner/cli.py` | The command-line app — `add` and `list` |
| `tripplanner/destinations/stops.py` | Builds and validates a stop |
| `tripplanner/destinations/test_date_beside_module.py` | A test beside its code |
| `tripplanner/storage/trip_store.py` | Saves/loads the trip as JSON |
| `tripplanner/parsing/free_text.py` | Text → stop (upgraded to a live AI call in Part 3) |
| `tripplanner/tests/test_stops.py` | Tests in the usual `tests/` folder |
| `tripplanner/.gitignore` | Files Git should ignore |

---

## Copy-paste command reference

Everything you type in this part, in one place:

```cmd
:: check prerequisites
python --version
claude --version

:: move into the project (adjust the path)
cd C:\cca\tripplanner

:: run the app
python cli.py
python cli.py list
python cli.py add "Jaipur 2026-10-02 3"
python cli.py add "Goa 2026-10-05 2"
python cli.py add "Udaipur 2026-09-28 1"
python cli.py list

:: let Claude Code read the project
claude
::   > What does this project do? Give me a two-line summary.
::   > Which file is responsible for saving the trip to disk?
::   /exit

:: optional venv (run from the folder with requirements.txt)
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## What's next

**Part 1 — Memory & rules (Tasks 3.1 + 3.3).** We teach Claude Code your
project's standards *automatically*: the `CLAUDE.md` hierarchy (user vs project
vs directory), the `@import` syntax, and `.claude/rules/` files with glob
patterns that load the right rules for the right files. You'll run a small Python
script that shows *exactly* which instructions a Claude Code session would load —
so the "invisible" configuration becomes visible.

See you in Part 1.

---

*CCA-Foundations · Domain 3 · Part 0 — ANKIT MISTRY*
