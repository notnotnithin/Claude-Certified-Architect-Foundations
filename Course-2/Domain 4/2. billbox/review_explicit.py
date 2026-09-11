"""
review_explicit.py   (the RIGHT way)
==================================================================
Part 1 demo - Task 4.1, the RIGHT way: explicit criteria

Same receipt, same model. The only thing that changes is the prompt: instead of
"find any problems", we tell Claude EXACTLY what counts as a problem and what to
ignore. That precision is the whole lesson of Task 4.1.

WHY THIS WORKS
--------------
The prompt below does three things the vague version didn't:

  1. It lists the SPECIFIC things to report (a real total mismatch, a missing
     GST number, a missing date).
  2. It lists what to IGNORE (rounded prices, tip lines, thank-you notes,
     abbreviations) - so those stop showing up as false positives.
  3. It defines SEVERITY with concrete meaning (high/medium/low), so the output
     is consistent instead of a guess.

Explicit categorical criteria beat vague hopes like "be conservative" every time.

HOW TO RUN (from the project root, in cmd):

    python review_explicit.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from billbox._shared import ask_claude, load_receipt

# Explicit criteria: exactly what to report, exactly what to ignore, and clear
# severity levels. This is the heart of Task 4.1.
EXPLICIT_SYSTEM = """You are reviewing a shop receipt for BillBox.

Report a finding ONLY if it matches one of these specific problems:

  - TOTAL_MISMATCH (high): the printed total does not equal subtotal plus taxes,
    off by more than 1 rupee.
  - MISSING_GST (medium): there is no GST / GSTIN number anywhere on the receipt.
  - MISSING_DATE (medium): there is no date on the receipt.
  - MISSING_TOTAL (high): there is no final total amount.

Do NOT report any of the following - these are acceptable and are not problems:
  - round or whole-number prices
  - a tip line, service charge, or "thank you" message
  - abbreviations or short item names
  - the payment method
  - anything not in the list above

For each finding, give: the CODE, the severity in brackets, and a one-line
reason. If there are no findings, say exactly: "No issues found."
"""


def main():
    receipt = load_receipt("grocery_receipt.txt")

    print("\n" + "=" * 64)
    print("  EXPLICIT CRITERIA  (the right way)")
    print("=" * 64)
    print("\nReviewing grocery_receipt.txt with explicit criteria...\n")

    reply = ask_claude(EXPLICIT_SYSTEM, receipt)
    print(reply)

    print("\n" + "-" * 64)
    print("""  Now Claude only reports things that match the exact criteria. The
  harmless items the vague version flagged are gone, because we told
  Claude to ignore them. Fewer false positives = a tool people trust.

  Try it on the other receipts too - change the filename in main() to
  restaurant_bill.txt or utility_bill.txt and run again.""")


if __name__ == "__main__":
    main()
