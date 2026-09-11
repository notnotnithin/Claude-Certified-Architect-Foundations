"""
multi_pass_review.py
==================================================================
Part 6 demo - Task 4.6: split a big review into focused passes

When you have MANY receipts to review, doing them all in one giant prompt dilutes
the model's attention - it reviews some carefully and skims others, and can even
contradict itself. The fix is to split the work into focused passes.

TWO KINDS OF PASS
-----------------
1. LOCAL passes: review each receipt on its own, one at a time. Full attention on
   one receipt means consistent, careful checks.

2. An INTEGRATION pass: look ACROSS all receipts together for things that only
   make sense in aggregate - duplicate bills, an impossible date order, the same
   merchant charging wildly different amounts.

A local pass can't see cross-receipt issues; an integration pass can't give each
receipt deep individual attention. You need both.

HOW TO RUN (from the project root, in cmd):

    python multi_pass_review.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from billbox._shared import get_client, MODEL, load_receipt

# A few receipts to review together.
RECEIPTS = ["grocery_receipt.txt", "restaurant_bill.txt", "broken_total.txt"]


def local_pass(client, name):
    """Review ONE receipt on its own, with full attention."""
    receipt = load_receipt(name)
    msgs = [{"role": "user", "content":
        f"Review this single receipt for internal problems only (do the numbers "
        f"add up? is the date valid? is the total present?). Be brief - one or two "
        f"lines.\n\n{receipt}"}]
    resp = client.messages.create(model=MODEL, max_tokens=300, messages=msgs)
    return "".join(b.text for b in resp.content if b.type == "text").strip()


def integration_pass(client, summaries):
    """Look ACROSS all receipts for issues visible only in aggregate."""
    combined = "\n".join(f"- {name}: {summary}" for name, summary in summaries)
    msgs = [{"role": "user", "content":
        f"Here are per-receipt review notes for several receipts:\n\n{combined}\n\n"
        f"Now look ACROSS all of them together. Are there any cross-receipt issues - "
        f"duplicates, the same merchant with very different totals, dates out of "
        f"order? Be brief."}]
    resp = client.messages.create(model=MODEL, max_tokens=300, messages=msgs)
    return "".join(b.text for b in resp.content if b.type == "text").strip()


def main():
    client = get_client()

    print("\n" + "=" * 64)
    print("  MULTI-PASS REVIEW")
    print("=" * 64)

    # --- Local passes: one receipt at a time ---
    print("\n[1] LOCAL passes - each receipt reviewed on its own:\n")
    summaries = []
    for name in RECEIPTS:
        note = local_pass(client, name)
        summaries.append((name, note))
        print(f"  {name}:")
        print(f"    {note}\n")

    # --- Integration pass: across all receipts ---
    print("[2] INTEGRATION pass - looking across all receipts together:\n")
    across = integration_pass(client, summaries)
    print(f"  {across}")

    print("\n" + "-" * 64)
    print("""  Each receipt got full attention in its own LOCAL pass - so no
  receipt was skimmed. Then one INTEGRATION pass caught anything that
  only appears across receipts.

  Splitting the work this way beats one giant prompt, which would
  dilute attention and give inconsistent, sometimes contradictory
  reviews.""")


if __name__ == "__main__":
    main()
