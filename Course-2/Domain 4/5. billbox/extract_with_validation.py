"""
extract_with_validation.py   (the RIGHT way)
==================================================================
Part 4 demo - Task 4.4: validate, then retry with specific feedback

Now we check the extraction with our Pydantic model, and if it fails, we send
the failure BACK to Claude with the exact error, and let it try again. This is
the retry-with-error-feedback loop.

Two receipts show the two outcomes the exam cares about:

  1. broken_total.txt  - line items sum to 885 but the receipt says 985.
     Retry CAN help: told the exact discrepancy, Claude re-reads and corrects
     (usually by flagging the conflict and fixing calculated_total).

  2. missing_total.txt - the receipt has NO total at all (torn off).
     Retry CANNOT help: the information simply is not in the document. No amount
     of re-asking can invent it. A good loop RECOGNISES this and gives up instead
     of looping forever.

Knowing the difference - format/semantic errors (retry helps) vs missing
information (retry is useless) - is the heart of Task 4.4.

HOW TO RUN (from the project root, in cmd):

    python extract_with_validation.py
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pydantic import ValidationError

from billbox._shared import extract_with_tool, load_receipt
from billbox.receipt_model import Receipt

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

MAX_RETRIES = 2


def extract_and_validate(receipt_name):
    """
    Extract a receipt, validate it, and retry with feedback if validation fails.

    Returns (validated_receipt_or_None, story) where 'story' is the list of what
    happened, so we can print the loop clearly.
    """
    receipt_text = load_receipt(receipt_name)
    story = []

    # The user message starts as just the receipt. On each retry we ADD the
    # previous failure and the specific error, so Claude can correct itself.
    user_message = f"Receipt:\n{receipt_text}"

    for attempt in range(1, MAX_RETRIES + 2):  # first try + retries
        data, _ = extract_with_tool(
            SYSTEM, user_message, TOOL, {"type": "tool", "name": "save_receipt"}
        )

        try:
            receipt = Receipt(**data)
            story.append(f"Attempt {attempt}: VALID.")
            return receipt, story
        except ValidationError as e:
            error_text = "; ".join(err["msg"] for err in e.errors())
            story.append(f"Attempt {attempt}: rejected - {error_text}")

            # THE KEY DECISION: is this the kind of error a retry can fix?
            # If the total is simply MISSING from the receipt, retrying is
            # pointless - the information is not there to find.
            if "missing" in error_text.lower():
                story.append(
                    "   -> The total is ABSENT from the receipt. Retrying cannot "
                    "invent it. Giving up (this needs a human)."
                )
                return None, story

            # Otherwise it is a format/semantic error - retry WITH the specific
            # error appended, so Claude knows exactly what to fix.
            if attempt <= MAX_RETRIES:
                story.append("   -> A fixable discrepancy. Retrying with the exact error...")
                user_message = (
                    f"Receipt:\n{receipt_text}\n\n"
                    f"Your previous extraction was rejected for this reason:\n"
                    f"  {error_text}\n\n"
                    f"Re-read the receipt carefully and extract it correctly. "
                    f"If the printed total genuinely disagrees with the line items, "
                    f"set conflict_detected to true and make calculated_total the "
                    f"true sum of the items."
                )

    story.append("Gave up after retries.")
    return None, story


def run(receipt_name):
    print("\n" + "=" * 64)
    print(f"  VALIDATING: {receipt_name}")
    print("=" * 64)
    receipt, story = extract_and_validate(receipt_name)
    for line in story:
        print("  " + line)
    if receipt:
        print(f"\n  FINAL: {receipt.merchant}, items sum to "
              f"{sum(i.price for i in receipt.line_items):.2f}, "
              f"conflict={receipt.conflict_detected}")
    else:
        print("\n  FINAL: no valid extraction - routed to a human.")


def main():
    # Case 1: a fixable discrepancy - retry helps.
    run("broken_total.txt")
    # Case 2: information genuinely missing - retry cannot help.
    run("missing_total.txt")

    print("\n" + "-" * 64)
    print("""  The lesson of Task 4.4:
    - broken_total: a discrepancy retry CAN fix - so we feed back the
      exact error and let Claude correct itself.
    - missing_total: the info is ABSENT - retry is useless, so we stop
      and route to a human instead of looping forever.

  Feeding back the SPECIFIC error (not just "try again") is what makes
  the retry work. And knowing when NOT to retry is just as important.""")


if __name__ == "__main__":
    main()
