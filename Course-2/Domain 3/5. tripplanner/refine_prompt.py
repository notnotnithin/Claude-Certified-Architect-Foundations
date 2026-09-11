"""
refine_prompt.py
==================================================================
Part 3 live demo — Iterative refinement with concrete examples (Task 3.5)

THE PROBLEM WE ARE SOLVING
--------------------------
In Part 0 we wrote a simple parser in parsing/free_text.py. It only understands
rigid input like:

    "Jaipur 2026-10-02 3"

If Asha types how people actually talk -- "3 nights in Jaipur from Oct 2" or
"New York 2026-11-01 2" (a two-word place name) -- the old parser breaks. In
Part 2, our analyze-codebase skill even flagged this exact limitation.

Now we fix it by asking Claude to do the parsing. But HOW we ask matters enormously.

WHAT THIS SCRIPT SHOWS
----------------------
The same messy inputs, sent to the same model, with TWO different prompts:

  ATTEMPT 1 (weak)  : a prose description of what we want.
  ATTEMPT 2 (better): the same request PLUS 3 concrete input/output examples.

Watch how the weak prompt gives inconsistent shapes and formats, while the
example-driven prompt produces the same clean structure every time. That is the
lesson of Task 3.5: when prose is interpreted inconsistently, concrete
input/output examples are the most effective fix.

BEFORE YOU RUN
--------------
1. Put your API key in a .env file next to this script:

       ANTHROPIC_API_KEY=sk-ant-your-key-here

2. Install the packages (from the folder with requirements.txt):

       pip install -r requirements.txt

3. Run it:

       python refine_prompt.py
"""

import os
import json

from dotenv import load_dotenv
import anthropic

# Every file that creates an Anthropic client must load the .env ITSELF.
# If we relied on another module to do it, this file could run first and find
# no API key.
load_dotenv()

MODEL = "claude-sonnet-4-6"

# The messy, realistic inputs Asha might actually type. The old rigid parser
# fails on every one of these.
TEST_INPUTS = [
    "3 nights in Jaipur from Oct 2",
    "New York 2026-11-01 2",
    "two nights at Goa starting 5 Nov 2026",
]


# ------------------------------------------------------------------
# ATTEMPT 1 — the WEAK prompt (prose only)
# ------------------------------------------------------------------
# This describes what we want in plain English. It sounds reasonable! But it
# leaves the model to guess the field names, the date format, and the shape of
# the answer. Different inputs will come back in different shapes.
WEAK_PROMPT = """You are helping a trip planner app.

Read the user's text and pull out the place, the date, and how many nights they
are staying. Return the result as JSON."""


# ------------------------------------------------------------------
# ATTEMPT 2 — the BETTER prompt (same request + concrete examples)
# ------------------------------------------------------------------
# Same goal, but now we SHOW the model exactly what we want with 3 worked
# examples. Notice we deliberately include:
#   - a natural-language date ("Oct 2")  -> shows the YYYY-MM-DD conversion
#   - a two-word place ("New York")      -> shows multi-word places are fine
#   - a spelled-out number ("two")       -> shows words become integers
# These are the exact cases that used to break us.
BETTER_PROMPT = """You are helping a trip planner app.

Read the user's text and pull out the place, the date, and how many nights they
are staying. Return ONLY a JSON object, no other text.

Use exactly these keys: "place", "date", "nights".
- "place"  : a string, the full place name (may be more than one word)
- "date"   : a string in YYYY-MM-DD form
- "nights" : a whole number

Here are examples of exactly what to return:

Input: "2 nights in Pune from Dec 5 2026"
Output: {"place": "Pune", "date": "2026-12-05", "nights": 2}

Input: "San Francisco 2026-03-14 4"
Output: {"place": "San Francisco", "date": "2026-03-14", "nights": 4}

Input: "three nights at Kochi starting 9 Jan 2027"
Output: {"place": "Kochi", "date": "2027-01-09", "nights": 3}"""


def ask_claude(system_prompt, user_text):
    """
    Send one request to Claude and return the raw text of the reply.

    We keep this tiny on purpose: the LESSON is the prompt, not the plumbing.
    """
    client = anthropic.Anthropic()

    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=system_prompt,
        messages=[{"role": "user", "content": user_text}],
    )

    # The reply comes back as a list of blocks; we want the text.
    parts = []
    for block in response.content:
        if block.type == "text":
            parts.append(block.text)
    return "".join(parts).strip()


def show_attempt(title, system_prompt):
    """Run every test input against one prompt and print what came back."""
    print()
    print("=" * 66)
    print(f"  {title}")
    print("=" * 66)

    for user_text in TEST_INPUTS:
        print(f"\n  INPUT : {user_text}")
        try:
            reply = ask_claude(system_prompt, user_text)
        except Exception as e:
            print(f"  ERROR : {e}")
            continue

        print(f"  OUTPUT: {reply}")

        # Can our app actually USE this reply? That is the real test.
        # We try to read it as JSON with the exact keys the app needs.
        verdict = check_usable(reply)
        print(f"  USABLE: {verdict}")


def check_usable(reply):
    """
    Check whether a reply is something the app could actually use:
    valid JSON, with exactly the keys place/date/nights, and nights a number.

    This is what turns "looks fine" into a clear PASS/FAIL on screen.
    """
    text = reply.strip()

    # Models sometimes wrap JSON in ```json fences. Strip them if present.
    if text.startswith("```"):
        text = text.strip("`")
        if text.lower().startswith("json"):
            text = text[4:]
        text = text.strip()

    try:
        data = json.loads(text)
    except Exception:
        return "NO  - not clean JSON the app can read"

    if not isinstance(data, dict):
        return "NO  - JSON is not an object"

    missing = [k for k in ("place", "date", "nights") if k not in data]
    if missing:
        return f"NO  - missing key(s): {', '.join(missing)}"

    if not isinstance(data["nights"], int):
        return f"NO  - 'nights' is {type(data['nights']).__name__}, not a number"

    date = str(data["date"])
    if len(date) != 10 or date[4] != "-" or date[7] != "-":
        return f"NO  - 'date' is not YYYY-MM-DD ({date})"

    return "YES - the app can use this as-is"


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\nNo API key found.")
        print("Create a .env file next to this script containing:")
        print("    ANTHROPIC_API_KEY=sk-ant-your-key-here\n")
        return

    print("\nSame model. Same inputs. Two different prompts.")
    print("Watch what changes.")

    show_attempt("ATTEMPT 1 - WEAK PROMPT (prose description only)", WEAK_PROMPT)
    show_attempt("ATTEMPT 2 - BETTER PROMPT (prose + 3 concrete examples)", BETTER_PROMPT)

    print()
    print("=" * 66)
    print("  WHAT TO NOTICE")
    print("=" * 66)
    print("""
  The weak prompt is not 'wrong' - it is just vague. The model has to guess
  the key names, the date format, and whether to add extra commentary. Guesses
  vary from input to input, so the app cannot rely on the answer.

  The better prompt changed nothing about the model or the task. It simply
  SHOWED the model 3 worked examples covering the tricky cases (a natural
  date, a two-word place, a spelled-out number). Now the shape is consistent.

  That is Task 3.5: when a prose description is interpreted inconsistently,
  concrete input/output examples are the most effective fix.
""")


if __name__ == "__main__":
    main()
