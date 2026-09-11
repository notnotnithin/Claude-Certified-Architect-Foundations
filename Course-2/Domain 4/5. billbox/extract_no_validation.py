"""
extract_no_validation.py   (the ANTI-PATTERN)
==================================================================
Part 4 demo - Task 4.4, the WRONG way: trust the output blindly

Part 3's schema guarantees the SHAPE of the data. It is tempting to think the job
is done - the JSON is valid, so ship it. This script does exactly that: it
extracts a receipt and trusts whatever comes back, with no checking.

WHY THIS IS THE ANTI-PATTERN
----------------------------
We run it on broken_total.txt - a receipt whose line items sum to 885, but whose
printed total says 985 (a 100 rupee error, maybe a typo on the receipt itself).

The schema is happy: 985 is a valid number in a valid shape. So the bad total
sails straight through into our data. Nobody noticed the numbers don't add up.
That is a SEMANTIC error, and a schema cannot catch it.

HOW TO RUN (from the project root, in cmd):

    python extract_no_validation.py
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from billbox._shared import extract_with_tool, load_receipt

ROOT = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(ROOT, "schemas", "receipt_schema_v2.json"), encoding="utf-8") as f:
    SCHEMA = json.load(f)

TOOL = {
    "name": "save_receipt",
    "description": "Save the structured data extracted from a receipt.",
    "input_schema": SCHEMA,
}

SYSTEM = """You extract data from a shop receipt and save it with save_receipt.
- date must be YYYY-MM-DD.
- line_items: every item and its price.
- stated_total: the total printed on the receipt (null if there is none).
- calculated_total: the sum of the line item prices.
- conflict_detected: true if stated_total is present and differs from your sum."""


def main():
    print("\n" + "=" * 64)
    print("  NO VALIDATION  (trust the output - the anti-pattern)")
    print("=" * 64)

    receipt = load_receipt("broken_total.txt")
    data, stop = extract_with_tool(
        SYSTEM, receipt, TOOL, {"type": "tool", "name": "save_receipt"}
    )

    print("\nExtracted (and blindly trusted):")
    print(f"  merchant        : {data.get('merchant')}")
    print(f"  stated_total    : {data.get('stated_total')}")
    print(f"  calculated_total: {data.get('calculated_total')}")
    print(f"  conflict_detected: {data.get('conflict_detected')}")

    print("\n" + "-" * 64)
    print("""  The shape is perfect, so we shipped it. But look: the line items
  do not add up to the stated total. That 100-rupee error just entered
  our data unnoticed.

  A JSON schema cannot catch this - it only checks shape, not whether
  the numbers are RIGHT. We need semantic validation. See
  extract_with_validation.py.""")


if __name__ == "__main__":
    main()
