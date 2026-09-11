"""
answer_no_confidence.py   (the ANTI-PATTERN)
==================================================================
Part 5 demo - Task 5.5, the WRONG way: trust every answer equally

ScholarDesk answers questions from its sources. The lazy approach is to treat EVERY
answer as equally trustworthy and send them all straight to the user - no matter how
well (or poorly) the sources actually supported the answer.

WHY THIS IS THE ANTI-PATTERN
----------------------------
Some questions are clearly answered by the sources; others are only partly covered,
or not covered at all. If the assistant sounds equally confident on all of them, a
shaky answer goes out looking just as authoritative as a solid one. Nobody knows
which answers to double-check, so weakly-supported answers reach the user unnoticed.

This script asks a few questions and just prints the answers, flat, with no signal
about which ones are risky.

HOW TO RUN (from the project root, in cmd):

    python answer_no_confidence.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scholardesk._shared import ask_claude, source_path, list_sources


def load_all_sources():
    out = []
    for name in list_sources():
        with open(source_path(name), encoding="utf-8") as f:
            out.append(f.read())
    return "\n\n".join(out)


QUESTIONS = [
    "What is the running cost per km of an electric two-wheeler?",  # clearly covered
    "How many public charging points does Pune have?",             # clearly covered
    "What is the 5-year resale value of an electric scooter?",      # NOT in the sources
]

SYSTEM = """You are ScholarDesk, a research assistant. Answer the user's question
using the sources. Give a direct answer."""


def main():
    sources = load_all_sources()
    system = SYSTEM + "\n\nSOURCES:\n" + sources

    print("\n" + "=" * 64)
    print("  NO CONFIDENCE  (every answer treated equally - the anti-pattern)")
    print("=" * 64)

    for q in QUESTIONS:
        answer = ask_claude(system, [{"role": "user", "content": q}])
        print(f"\nQ: {q}")
        print(f"A: {answer}")

    print("\n" + "-" * 64)
    print("""  Every answer went straight out, looking equally confident - even
  the resale-value one, which the sources don't cover at all. There's
  no signal telling anyone which answer to double-check, so a shaky
  answer reaches the user looking authoritative.

  The fix: have the assistant report its confidence, and route the shaky
  ones to a human. See answer_with_confidence.py.""")


if __name__ == "__main__":
    main()
