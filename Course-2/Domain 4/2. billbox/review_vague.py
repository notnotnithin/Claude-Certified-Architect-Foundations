"""
review_vague.py   (the ANTI-PATTERN)
==================================================================
Part 1 demo - Task 4.1, the WRONG way: vague criteria

BillBox needs to review a receipt and report problems worth a human's attention.
The obvious first attempt is to just... ask it to find problems. That's what this
script does. It sounds reasonable, but watch what happens.

WHY THIS IS THE ANTI-PATTERN
----------------------------
The prompt below uses vague, open-ended language:

    "Review this receipt and report any problems or anything that looks off."

Plus the classic non-fixes the exam warns about:

    "Be conservative and only report high-confidence issues."

These feel helpful but don't actually tell Claude WHAT counts as a problem. So it
guesses - and it tends to flag lots of harmless things: rounded numbers, a tip
line, a friendly "thank you", an abbreviation. Those are FALSE POSITIVES. When a
tool cries wolf like this, people stop trusting it.

HOW TO RUN (from the project root, in cmd):

    python review_vague.py
"""

import os
import sys

# Make the 'billbox' package importable when running from the project root.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from billbox._shared import ask_claude, load_receipt

# The vague criteria. Note the "be conservative" line - the exam specifically
# calls this out as something that does NOT improve precision.
VAGUE_SYSTEM = """You are reviewing a shop receipt.

Review this receipt and report any problems or anything that looks off or
unusual. Be conservative and only report high-confidence issues."""


def main():
    receipt = load_receipt("grocery_receipt.txt")

    print("\n" + "=" * 64)
    print("  VAGUE CRITERIA  (the anti-pattern)")
    print("=" * 64)
    print("\nReviewing grocery_receipt.txt with vague instructions...\n")

    reply = ask_claude(VAGUE_SYSTEM, receipt)
    print(reply)

    print("\n" + "-" * 64)
    print("""  Look at what it flagged. With no clear definition of a "problem",
  Claude often reports harmless things - rounded prices, the tip or
  thank-you line, an abbreviation. Those are FALSE POSITIVES.

  "Be conservative" did not help: it is not a real criterion, just a
  vague hope. Compare this with review_explicit.py.""")


if __name__ == "__main__":
    main()
