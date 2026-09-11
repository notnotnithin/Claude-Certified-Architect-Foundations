# Part 0 — Setup & First Run

### Domain 5: Context Management & Reliability · The ScholarDesk Project

---

## Welcome to Domain 5

This is **Part 0** of Domain 5. Across this domain we build one project —
**ScholarDesk**, a research assistant — and make it **reliable**: good at long
research sessions, honest about what it's unsure of, and careful to say **which
source each fact came from**. Those reliability skills are exactly what the Domain 5
exam tests.

Part 0 has one job: **get you set up and meet ScholarDesk.**

By the end of this part you will have:

1. The ScholarDesk project open in VS Code.
2. Your API key ready.
3. ScholarDesk answering a question from a source document.

There is **no exam objective in Part 0** — it's the on-ramp. The real concepts start
in Part 1.

> **How to use this course:** **read** these explanations in **VS Code** (this
> `README.md`), and **run** the commands in your terminal (**cmd** on Windows).

---

## Which tools does Domain 5 use?

Two tools you already know — no new ones:

| Parts | Tool | Like which domain |
|-------|------|-------------------|
| 0, 1, 2, 3, 5, 6 | **Claude API** — Python scripts in VS Code, run in cmd | Domain 4 |
| 4 | **Claude Code** — the CLI tool | Domain 3 |

So **six of the seven parts use the API** (you'll need your `sk-ant-` key, set up
below). **Only Part 4** switches to Claude Code, because that part is about exploring
a codebase — a Claude Code skill, not an API call. We'll flag that clearly when we
get there. The **chat window (claude.ai) is not used** in any part.

---

## Meet ScholarDesk

ScholarDesk is a **research assistant**. You ask it a question, and it answers using
**source documents** — short briefs, reports, notes. Its job is to read sources and
give you a clear, factual, **cited** answer.

Asha is researching electric vehicles in India, and she's gathered a few short source
documents. ScholarDesk helps her pull answers out of them.

Right now (Part 0) ScholarDesk is deliberately simple — it answers from **one** source
at a time. The big theme of Domain 5 is doing this **reliably**, and especially
combining **several** sources while tracking where each fact came from:

```
   Part 1  ──►  Keep key findings across a long research session   (5.1)
   Part 2  ──►  Escalate to a human expert when sources fall short (5.2)
   Part 3  ──►  Handle a source that fails to load                 (5.3)
   Part 4  ──►  Explore ScholarDesk's own code (Claude Code)       (5.4)
   Part 5  ──►  Rate confidence per finding, route weak ones       (5.5)
   Part 6  ──►  Combine many sources, cite each, flag conflicts    (5.6)
```

### How the project is laid out

```
1. scholardesk/
├── scholardesk/
│   ├── ask.py          ← ask a question of a source
│   └── _shared.py      ← a small API helper
├── sources/
│   ├── ev_adoption_report.txt   ← EV sales & adoption
│   ├── ev_cost_brief.txt        ← EV ownership costs
│   └── ev_charging_note.txt     ← charging infrastructure
├── requirements.txt
├── .env.example
└── .gitignore
```

The `sources/` folder is ScholarDesk's world — the documents it reads. Notice each
source has a **publication date** in its header. That small detail matters a lot in
Part 6, where dates help tell an *updated* fact apart from a *contradiction*.

---

## Step 1 — Check Python

Open **cmd** and check Python is installed:

```cmd
python --version
```

You want Python **3.8 or higher**. If you see `'python' is not recognized`, install
it from https://www.python.org/ and tick **"Add Python to PATH"**.

---

## Step 2 — Open ScholarDesk in VS Code

1. Unzip the Part 0 folder somewhere easy, e.g. `C:\cca\`.
2. Open **VS Code** → **File → Open Folder…** → choose the `1. scholardesk` folder.
3. You'll see the layout above in the file tree.

---

## Step 3 — Get your API key ready

ScholarDesk calls the Claude API, so it needs a key.

1. Go to https://console.anthropic.com/ → **API Keys** → create a key (starts with
   `sk-ant-`). You may need to add a little credit under **Billing**.
2. In the project folder, copy the example env file:

   ```cmd
   copy .env.example .env
   ```

3. Open the new `.env` in VS Code and paste your key:

   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

Your `.env` is already in `.gitignore`, so your key will never be committed.

> **Already did Domain 4?** You can reuse the same key — just make a fresh `.env`
> here from `.env.example`.

---

## Step 4 — Install the packages

From the project folder (a virtual environment is recommended):

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Your prompt shows `(.venv)` when active. This installs `anthropic`, `python-dotenv`,
and `pydantic`.

---

## Step 5 — Talk to ScholarDesk

First, see the sources:

```cmd
python scholardesk/ask.py list
```

```
Sources available:
   - ev_adoption_report.txt
   - ev_charging_note.txt
   - ev_cost_brief.txt

Total: 3 sources
```

Now ask a question of one source:

```cmd
python scholardesk/ask.py ev_cost_brief.txt "How much does an electric scooter cost in Pune?"
```

```
Question: How much does an electric scooter cost in Pune?
(from ev_cost_brief.txt)

ScholarDesk: An electric two-wheeler costs about Rs 1.10 lakh on-road in Pune...
```

Try a few more:

```cmd
python scholardesk/ask.py ev_charging_note.txt "How many public chargers does Pune have?"
python scholardesk/ask.py ev_adoption_report.txt "How many EVs were sold in India?"
python scholardesk/ask.py ev_cost_brief.txt "What is the resale value of an EV?"
```

Notice the last one — the cost brief doesn't mention resale value, so ScholarDesk
should say it **can't find that in the source** rather than inventing a number. That
honesty is the first small taste of reliability, which the rest of Domain 5 builds on.

> **One source at a time — for now.** Part 0 reads a single source on purpose.
> Combining several sources into one cited answer is the domain's big finale (Part 6).

---

## What's in this folder

| File / folder | What it is |
|---|---|
| `README.md` | This guide |
| `scholardesk/ask.py` | Ask a question of a source |
| `scholardesk/_shared.py` | A small API helper used across the domain |
| `sources/*.txt` | Three short EV source documents (each dated) |
| `requirements.txt` | Packages |
| `.env.example` | Copy to `.env` and add your key |
| `.gitignore` | Files Git ignores (including `.env`) |

---

## Copy-paste command reference

```cmd
:: check Python
python --version

:: move into the project (adjust the path)
cd C:\cca\1. scholardesk

:: set up your API key (once)
copy .env.example .env
::   then paste your key into .env in VS Code

:: install packages (venv recommended)
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

:: talk to ScholarDesk
python scholardesk/ask.py list
python scholardesk/ask.py ev_cost_brief.txt "How much does an electric scooter cost in Pune?"
```

---

## What's next

**Part 1 — Context management (Task 5.1).** In a long research session, the important
findings (exact figures, dates, source names) get buried or summarised away. We teach
ScholarDesk to keep a "findings" block that survives the whole session — and to trim
bloated inputs before they crowd everything out.

See you in Part 1.

---

*CCAR-F · Domain 5 · Part 0 — ANKIT MISTRY*
