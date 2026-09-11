"""
review_self.py   (the ANTI-PATTERN)
==================================================================
Part 6 demo - Task 4.6, the weaker way: a model reviews its OWN work

BillBox extracts a receipt, then we ask the SAME conversation to review that
extraction for mistakes. It sounds efficient - why start a new conversation? But
it's the weaker approach, and this script shows why.

WHY THIS IS THE ANTI-PATTERN
----------------------------
When the same instance that produced the extraction reviews it, it still carries
all the REASONING it used to produce it. It already "decided" the total was 985,
so when asked to check, it tends to defend or lightly polish that decision rather
than truly question it. It's the same reason a writer misses their own typos: they
read what they MEANT to write.

So self-review catches fewer real problems. A fresh pair of eyes catches more -
that's review_independent.py.

HOW TO RUN (from the project root, in cmd):

    python review_self.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from billbox._shared import get_client, MODEL, load_receipt


def main():
    client = get_client()
    receipt = load_receipt("broken_total.txt")  # the tricky one: items sum 885, says 985

    print("\n" + "=" * 64)
    print("  SELF-REVIEW  (same conversation - the anti-pattern)")
    print("=" * 64)

    # Turn 1: extract. Turn 2: ask the SAME conversation to review its own work.
    # Both turns share ONE message history, so the reviewer carries the extractor's
    # reasoning with it.
    messages = [
        {"role": "user", "content":
            f"Extract the merchant, the line items with prices, and the total "
            f"from this receipt:\n\n{receipt}"}
    ]

    first = client.messages.create(
        model=MODEL, max_tokens=500, messages=messages
    )
    extraction = "".join(b.text for b in first.content if b.type == "text").strip()
    print("\n[Turn 1] The extraction:")
    print(extraction)

    # Add the model's own answer, then ask IT to review IT.
    messages.append({"role": "assistant", "content": extraction})
    messages.append({"role": "user", "content":
        "Now review your own extraction above. Is anything wrong or inconsistent? "
        "Do the line items actually add up to the total?"})

    second = client.messages.create(
        model=MODEL, max_tokens=500, messages=messages
    )
    review = "".join(b.text for b in second.content if b.type == "text").strip()
    print("\n[Turn 2] Its review of its OWN work:")
    print(review)

    print("\n" + "-" * 64)
    print("""  The reviewer here is the SAME instance that did the extraction, so
  it carries its own reasoning. It may notice the mismatch - or it may
  gloss over it, because it is checking work it already "believes" in.

  Run it a few times: self-review is inconsistent at catching its own
  mistakes. Compare with review_independent.py.""")


if __name__ == "__main__":
    main()
