"""
extract_zero_shot.py   (the ANTI-PATTERN)
==================================================================
Part 2 demo - Task 4.2, the WRONG way: no examples (zero-shot)

BillBox needs to pull the SAME fields out of EVERY receipt - merchant, date,
total - no matter how the receipt is laid out. This script tries to do that with
instructions only, and no examples. Watch what happens across our different
receipt formats.

WHY THIS IS THE ANTI-PATTERN
----------------------------
The prompt describes what we want in words, but never SHOWS an example. So Claude
has to guess the exact output shape for each receipt. Across formats you tend to
get:

  - different date formats (02/10/2026 here, 10-oct-26 there, "5 Oct 2026" there)
  - the total sometimes a number, sometimes a string with "Rs." or "/-"
  - the merchant sometimes trimmed, sometimes with the address attached
  - occasional extra commentary around the answer

Same fields, inconsistent shapes. Downstream code can't rely on that.

HOW TO RUN (from the project root, in cmd):

    python extract_zero_shot.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from billbox._shared import ask_claude, load_receipt

# All four receipts, in four different formats.
RECEIPTS = [
    "grocery_receipt.txt",
    "restaurant_bill.txt",
    "utility_bill.txt",
    "handwritten_style.txt",
]

# Instructions only - NO examples. This is what "zero-shot" means.
ZERO_SHOT_SYSTEM = """You extract data from a receipt.

Pull out the merchant name, the date, and the total amount. Return the result as
JSON."""


def main():
    print("\n" + "=" * 64)
    print("  ZERO-SHOT EXTRACTION  (no examples - the anti-pattern)")
    print("=" * 64)

    for name in RECEIPTS:
        receipt = load_receipt(name)
        print(f"\n--- {name} ---")
        reply = ask_claude(ZERO_SHOT_SYSTEM, receipt)
        print(reply)

    print("\n" + "-" * 64)
    print("""  Look across the four answers. The date format probably changes
  from receipt to receipt. The total may be a number in one and a
  string like "Rs. 374" in another. The merchant may include the
  address sometimes. Same fields, DIFFERENT shapes.

  Downstream code that expects one consistent shape will break on
  this. Compare with extract_few_shot.py.""")


if __name__ == "__main__":
    main()
