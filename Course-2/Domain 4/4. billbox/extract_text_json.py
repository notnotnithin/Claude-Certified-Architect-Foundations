"""
extract_text_json.py   (the ANTI-PATTERN)
==================================================================
Part 3 demo - Task 4.3, the WRONG way: asking for JSON as plain text

In Part 2, few-shot got the output shape USUALLY right. But "usually" is not good
enough for a pipeline. This script shows the weakness of the text approach: we
ask Claude to "return JSON" as ordinary text, then try to parse it ourselves.

WHY THIS IS THE ANTI-PATTERN
----------------------------
When Claude replies as free text, the reply can include things that break
`json.loads`:

  - a friendly preamble ("Sure! Here's the JSON:")
  - ```json code fences around the object
  - a trailing comment after the closing brace
  - very occasionally, a genuine JSON syntax slip

Any of those makes the parse fail. You end up writing fragile cleanup code that
strips fences and hunts for braces - and it still breaks eventually. Part 3's
tool_use approach removes this whole class of problem.

HOW TO RUN (from the project root, in cmd):

    python extract_text_json.py
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from billbox._shared import ask_claude, load_receipt

RECEIPTS = ["grocery_receipt.txt", "restaurant_bill.txt", "handwritten_style.txt"]

TEXT_JSON_SYSTEM = """You extract data from a receipt.

Return the merchant, date (YYYY-MM-DD), and total (a number) as a JSON object."""


def main():
    print("\n" + "=" * 64)
    print("  TEXT JSON  (parse it ourselves - the anti-pattern)")
    print("=" * 64)

    for name in RECEIPTS:
        receipt = load_receipt(name)
        print(f"\n--- {name} ---")
        reply = ask_claude(TEXT_JSON_SYSTEM, receipt)
        print("Raw reply:")
        print(reply)

        # Now try to use it as real data - this is where it can break.
        try:
            data = json.loads(reply)
            print(f"Parsed OK -> merchant = {data.get('merchant')!r}")
        except json.JSONDecodeError as e:
            print(f"PARSE FAILED: {e}")
            print("(A preamble, code fence, or stray text broke json.loads.)")

    print("\n" + "-" * 64)
    print("""  Even when the content is right, the WRAPPING can break the parse:
  a "Here's the JSON:" preamble, ```json fences, or a trailing note.
  You can write cleanup code to cope, but it stays fragile.

  Part 3's fix (extract_structured.py) makes broken JSON impossible.""")


if __name__ == "__main__":
    main()
