"""
extract_few_shot.py   (the RIGHT way)
==================================================================
Part 2 demo - Task 4.2, the RIGHT way: few-shot examples

Same four receipts, same model. The only change: we SHOW Claude a few worked
examples of exactly the output we want, before asking it to do a new one. That is
"few-shot" prompting, and it is the most effective way to get consistent,
well-formatted output.

WHY THIS WORKS
--------------
The prompt below includes THREE examples (2-4 is the sweet spot). They are chosen
to cover the tricky cases on purpose:

  - a normal receipt        -> shows the baseline shape
  - a date written as words -> shows how to normalise it to YYYY-MM-DD
  - an informal amount "/-"  -> shows how to turn it into a plain number
  - a receipt with NO GST    -> shows returning null instead of inventing one

By SHOWING the shape (not just describing it), every answer comes back the same
way - even for the messy handwritten-style receipt the model has never seen in
this exact form. That is generalisation: the examples teach judgement, not just a
fixed template.

HOW TO RUN (from the project root, in cmd):

    python extract_few_shot.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from billbox._shared import ask_claude, load_receipt

RECEIPTS = [
    "grocery_receipt.txt",
    "restaurant_bill.txt",
    "utility_bill.txt",
    "handwritten_style.txt",
]

# The SAME instruction as zero-shot, but now followed by worked examples that
# show exactly the shape we want - including the tricky cases (word-dates,
# informal amounts, missing GST -> null).
FEW_SHOT_SYSTEM = """You extract data from a receipt.

Pull out the merchant name, the date, and the total amount. Return ONLY a JSON
object with exactly these keys: "merchant", "date", "total", "gst_number".
- "date"  must be YYYY-MM-DD
- "total" must be a plain number (no "Rs." or "/-")
- "gst_number" is the GST/GSTIN if present, otherwise null (do not invent one)

Examples of exactly what to return:

Receipt: "SuperSave Mart, Mumbai. Date: 15/09/2026. GSTIN: 27AAAAA0000A1Z5. Total: Rs. 850.00"
Output: {"merchant": "SuperSave Mart", "date": "2026-09-15", "total": 850.00, "gst_number": "27AAAAA0000A1Z5"}

Receipt: "Cafe Blue ~ bill dt 3-mar-26 ~ coffee 120/- cake 200/- ~ total 320 rupees ~ no gst"
Output: {"merchant": "Cafe Blue", "date": "2026-03-03", "total": 320, "gst_number": null}

Receipt: "CITY POWER BILL. Consumer: R Sharma. Billing date 01 Aug 2026. Amount Payable Rs 1450."
Output: {"merchant": "City Power", "date": "2026-08-01", "total": 1450, "gst_number": null}"""


def main():
    print("\n" + "=" * 64)
    print("  FEW-SHOT EXTRACTION  (with examples - the right way)")
    print("=" * 64)

    for name in RECEIPTS:
        receipt = load_receipt(name)
        print(f"\n--- {name} ---")
        reply = ask_claude(FEW_SHOT_SYSTEM, receipt)
        print(reply)

    print("\n" + "-" * 64)
    print("""  Now every answer comes back in the SAME shape: date as YYYY-MM-DD,
  total as a plain number, missing GST as null instead of invented.
  Even the messy handwritten-style receipt is handled correctly,
  because the examples taught the pattern, not just a fixed template.

  That is few-shot prompting: SHOW the output you want, and Claude
  matches it consistently across formats it has never seen.""")


if __name__ == "__main__":
    main()
