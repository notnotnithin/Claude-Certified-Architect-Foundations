# Part 0 — Setup & First Run

### Domain 4: Prompt Engineering & Structured Output · The BillBox Project

---

## Welcome to Domain 4

This is **Part 0** of Domain 4. Across this domain we build one small project —
**BillBox** — and teach it to read messy receipts and pull out clean, structured
data. Along the way you'll learn every Domain 4 exam concept.

Part 0 has one job: **get you set up and see the raw material** BillBox starts
from.

By the end of this part you will have:

1. The BillBox project open in VS Code.
2. Your API key ready (you'll need it from Part 1 onward).
3. BillBox running in your terminal, showing you the messy receipts.

There is **no exam objective in Part 0** — it's the on-ramp. The real concepts
start in Part 1.

> **How to use this course:** **read** these explanations in **VS Code** (this
> `README.md`), and **run** the commands in your terminal (**cmd** on Windows).
> Read in VS Code, run in cmd. That pattern repeats in every part.

---

## One important note before we start

Domain 4 is different from Domain 3 in one big way.

Domain 3 (Claude Code) mostly ran inside the Claude Code chat, using your Claude
Pro login. **Domain 4 is about the Claude API** — writing small Python programs
that send receipts to Claude and get structured data back. That means:

> **From Part 1 onward, every demo needs an Anthropic API key.**

So we set that up now, in Part 0, and you won't have to think about it again.

---

## What is BillBox?

BillBox is a **receipt extractor**. You give it a messy receipt as plain text —
a grocery bill, a restaurant bill, an electricity bill — and it pulls out clean,
structured data:

```
   messy receipt text   ───►   BillBox   ───►   { "merchant": "FreshMart",
                                                   "date": "2026-10-02",
                                                   "total": 1194.90, ... }
```

Asha runs a small business in Pune and wants to digitise her pile of paper
receipts instead of typing them in by hand. BillBox is how she does it.

The app is deliberately small — **the point of Domain 4 is learning how to get
reliable structured data out of Claude, not building a big app.**

### How the project is laid out

```
1. billbox/
├── billbox/
│   ├── cli.py          ← the commands you type (list, show)
│   └── reader.py       ← loads a receipt from disk
├── receipts/
│   ├── grocery_receipt.txt    ← a supermarket bill
│   ├── restaurant_bill.txt    ← a restaurant bill (different format)
│   └── utility_bill.txt       ← an electricity bill (different again)
├── requirements.txt
├── .env.example
└── .gitignore
```

Notice the **three receipts are all in different formats** — a supermarket lays
things out differently from a restaurant, which differs again from a utility
bill. That variety is deliberate: in Part 2 we use it to teach few-shot
prompting, where examples help Claude handle every format reliably.

---

## Step 1 — Check Python

Open **cmd** and check Python is installed:

```cmd
python --version
```

You want Python **3.8 or higher**. If you see `'python' is not recognized`,
install it from https://www.python.org/ and tick **"Add Python to PATH"** during
install.

---

## Step 2 — Open BillBox in VS Code

1. Unzip the Part 0 folder somewhere easy, e.g. `C:\cca\`.
2. Open **VS Code** → **File → Open Folder…** → choose the `1. billbox` folder.
3. You'll see the layout above in the file tree on the left.

---

## Step 3 — See the receipts (no AI yet)

Open **cmd** and move into the project folder (adjust the path to where you
unzipped it):

```cmd
cd C:\cca\1. billbox
```

**List the receipts:**

```cmd
python billbox/cli.py list
```

```
Receipts available:
   - grocery_receipt.txt
   - restaurant_bill.txt
   - utility_bill.txt

Total: 3 receipts
```

**Show one receipt's raw text:**

```cmd
python billbox/cli.py show grocery_receipt.txt
```

```
============================================
  RAW TEXT: grocery_receipt.txt
============================================
FreshMart Supermarket
Shop 12, FC Road, Pune 411005
GSTIN: 27ABCDE1234F1Z5
--------------------------------
Date: 02/10/2026    Bill No: 4471

Toor Dal 1kg           Rs. 145.00
Basmati Rice 5kg       Rs. 480.00
...
Total:                Rs. 1194.90
```

Try the other two as well:

```cmd
python billbox/cli.py show restaurant_bill.txt
python billbox/cli.py show utility_bill.txt
```

**Look at how different they are.** One uses "Rs.", another splits CGST and SGST,
the third lists energy charges. A human can read all three easily — but getting a
program to pull the *same* clean fields out of *every* format is exactly the
challenge Domain 4 teaches you to solve.

---

## Step 4 — Get your API key ready (for Part 1 onward)

Part 0 doesn't call the API, but Part 1 does — so let's prepare now.

1. Go to https://console.anthropic.com/ → **API Keys** → create a key. It starts
   with `sk-ant-`. You may need to add a little credit under **Billing**.
2. In the project folder, copy the example env file:

   ```cmd
   copy .env.example .env
   ```

3. Open the new `.env` file in VS Code and paste your key:

   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

Your `.env` is already listed in `.gitignore`, so your key will never be
committed. **Do this once and you're set for all of Domain 4.**

> **Why a key and not my Claude Pro login?** These demos are small Python
> programs that talk to the Claude API directly. They can't use the Claude Code
> or Claude.ai subscription login — that's only for those apps. The API key is
> how your own programs authenticate. Usage for this course is small.

---

## Step 5 — Set up a virtual environment (recommended)

A **virtual environment** ("venv") keeps this project's packages separate from
the rest of your system. From the project folder:

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Your prompt shows `(.venv)` when it's active. To turn it off, type `deactivate`.
This installs `anthropic`, `python-dotenv`, and `pydantic` — all used from Part 1
onward. (Part 0 itself needs none of them.)

---

## What's in this folder

| File / folder | What it is |
|---|---|
| `README.md` | This guide |
| `billbox/cli.py` | The commands — `list` and `show` |
| `billbox/reader.py` | Loads a receipt from disk |
| `receipts/*.txt` | Three sample receipts, in three different formats |
| `requirements.txt` | Packages for later parts |
| `.env.example` | Copy to `.env` and add your key |
| `.gitignore` | Files Git should ignore (including `.env`) |

---

## Copy-paste command reference

```cmd
:: check Python
python --version

:: move into the project (adjust the path)
cd C:\cca\1. billbox

:: see the receipts
python billbox/cli.py list
python billbox/cli.py show grocery_receipt.txt
python billbox/cli.py show restaurant_bill.txt
python billbox/cli.py show utility_bill.txt

:: set up your API key (once)
copy .env.example .env
::   then paste your key into .env in VS Code

:: optional venv + install packages
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## What's next

**Part 1 — Explicit criteria (Task 4.1).** We make BillBox's first real request to
Claude, and learn the single biggest lever for reliable output: giving Claude
**explicit, precise criteria** instead of vague instructions. You'll see the same
receipt reviewed two ways — vague vs explicit — and watch the false-positives
disappear.

See you in Part 1.

---

*CCAR-F · Domain 4 · Part 0 — ANKIT MISTRY*
