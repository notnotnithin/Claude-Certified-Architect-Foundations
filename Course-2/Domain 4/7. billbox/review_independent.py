"""
review_independent.py   (the RIGHT way)
==================================================================
Part 6 demo - Task 4.6: an INDEPENDENT instance reviews the work

Same receipt. But this time the reviewer is a BRAND-NEW conversation that never
saw how the extraction was produced. It gets only the receipt and the extraction,
with no reasoning attached - a genuine fresh pair of eyes.

WHY THIS WORKS
--------------
Because the independent reviewer has no attachment to the extraction's reasoning,
it has nothing to defend. It simply checks: do these numbers add up? Is anything
inconsistent? It reliably catches the 885-vs-985 mismatch that self-review might
gloss over.

This is the core of Task 4.6: to catch subtle errors, use a SEPARATE instance
without the generator's context - not the same one that produced the work.

HOW TO RUN (from the project root, in cmd):

    python review_independent.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from billbox._shared import get_client, MODEL, load_receipt


def main():
    client = get_client()
    receipt = load_receipt("broken_total.txt")

    print("\n" + "=" * 64)
    print("  INDEPENDENT REVIEW  (a fresh instance - the right way)")
    print("=" * 64)

    # Step 1: an extraction is produced (in its own conversation).
    extract_msgs = [
        {"role": "user", "content":
            f"Extract the merchant, the line items with prices, and the total "
            f"from this receipt:\n\n{receipt}"}
    ]
    first = client.messages.create(model=MODEL, max_tokens=500, messages=extract_msgs)
    extraction = "".join(b.text for b in first.content if b.type == "text").strip()
    print("\n[Extraction produced by instance A]:")
    print(extraction)

    # Step 2: a COMPLETELY SEPARATE call reviews it. Note this is a fresh
    # messages list - none of instance A's reasoning is carried over. The reviewer
    # sees only the receipt and the extraction to check.
    review_msgs = [
        {"role": "user", "content":
            f"You are an independent reviewer. Here is a receipt and an extraction "
            f"someone else produced from it. Check it carefully: do the line items "
            f"add up to the total? Is anything inconsistent? Report specifically.\n\n"
            f"RECEIPT:\n{receipt}\n\nEXTRACTION TO REVIEW:\n{extraction}\n\n"
            f"Also give your confidence (high/medium/low) that the extraction is correct."}
    ]
    second = client.messages.create(model=MODEL, max_tokens=500, messages=review_msgs)
    review = "".join(b.text for b in second.content if b.type == "text").strip()
    print("\n[Review by an INDEPENDENT instance B]:")
    print(review)

    print("\n" + "-" * 64)
    print("""  Instance B never saw how the extraction was made, so it has no
  reasoning to defend. It just checks the numbers - and reliably spots
  the 885-vs-985 mismatch.

  Notice we also asked for a CONFIDENCE level. A low-confidence review
  is a signal to route this receipt to a human. That's calibrated
  routing: let the model tell you which results need a closer look.""")


if __name__ == "__main__":
    main()
