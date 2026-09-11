"""
ambiguity.py
==================================================================
Part 2 demo - Task 5.2: an ambiguous query -> ask, don't guess

A user asks ScholarDesk: "What's the cost?" But the sources cover several different
"costs": the purchase price of the vehicle, the running cost per km, and battery
replacement cost. The question matches MORE THAN ONE thing. What now?

THE WRONG WAY (a heuristic guess): just pick one meaning - say, whichever appears
first in the sources - and answer that. If the user meant a different cost, the
answer is confidently about the wrong thing, and they may not even notice.

THE RIGHT WAY: recognise the ambiguity and ASK which cost they mean, briefly listing
the options the sources can actually answer. One short clarifying question gets it
right.

This script shows both, using a query that maps to several distinct topics. It does
NOT call the API - it's about the decision logic when a query is ambiguous.

HOW TO RUN (from the project root, in cmd):

    python ambiguity.py
"""

import os
import sys

# The user's ambiguous query.
QUERY = "What's the cost?"

# The distinct "cost" topics the sources can actually answer.
POSSIBLE_MEANINGS = [
    "the on-road purchase price of the vehicle (about Rs 1.10 lakh)",
    "the running cost per km (about Rs 0.25/km)",
    "battery replacement cost (a long-term expense)",
]


def wrong_guess():
    """ANTI-PATTERN: pick one meaning and answer it, hoping it's the right one."""
    return ("(guessing) I'll assume you mean the purchase price: about Rs 1.10 lakh "
            "on-road. [If they actually meant running cost or battery cost, this "
            "answer is confidently about the wrong thing.]")


def right_clarify():
    """RIGHT WAY: ask which cost they mean, listing what the sources can answer."""
    lines = ["Your question could mean a few different things the sources cover. "
             "Which cost do you mean?"]
    for i, m in enumerate(POSSIBLE_MEANINGS, 1):
        lines.append(f"   {i}. {m}")
    return "\n".join(lines)


def main():
    print("\n" + "=" * 64)
    print("  AMBIGUOUS QUERY: 'What's the cost?'")
    print("=" * 64)

    print(f"\nUser: {QUERY}")
    print("\nThe sources cover several different 'costs':")
    for m in POSSIBLE_MEANINGS:
        print(f"  - {m}")

    print("\n[ANTI-PATTERN] heuristic guess:")
    print("  " + wrong_guess())

    print("\n[RIGHT WAY] ask which one they mean:")
    print("  " + right_clarify().replace("\n", "\n  "))

    print("\n" + "-" * 64)
    print("""  When one query matches several distinct answers, the safe move is to
  ASK which one - not to pick a meaning by a heuristic. Guessing risks
  confidently answering the wrong question. One short clarification gets
  it right.""")


if __name__ == "__main__":
    main()
