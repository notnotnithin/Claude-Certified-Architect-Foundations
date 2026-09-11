"""
submit_batch.py
==================================================================
Part 5 demo - Task 4.5: submit many receipts as ONE batch

BillBox has a pile of receipts to process overnight. Instead of calling the API
once per receipt (fast but full price), we send them all as a single BATCH:

  - 50% cheaper than normal calls
  - processed within 24 hours (usually much faster), with NO latency guarantee
  - each receipt tagged with a custom_id so we can match results back to it

That trade - cheaper but slower and not guaranteed-fast - is the whole decision of
Task 4.5. Batch is perfect for overnight jobs. It is WRONG for anything a user is
waiting on right now.

WHAT THIS SCRIPT DOES
---------------------
1. Reads every receipt in receipts_bulk/.
2. Builds one batch request per receipt, each with a unique custom_id.
3. Submits the batch and prints the batch id (save it - check_batch.py needs it).

IMPORTANT (honest note for the demo):
A real batch can take up to 24 hours. You submit it here, then come back later and
run check_batch.py. You will NOT see results appear instantly. That waiting is not
a bug - it is exactly the trade-off batch processing makes.

HOW TO RUN (from the project root, in cmd):

    python generate_receipts.py     (once, to create the receipts)
    python submit_batch.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from billbox._shared import get_client, MODEL

# The batch API uses these typed helpers from the SDK.
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

ROOT = os.path.dirname(os.path.abspath(__file__))
BULK = os.path.join(ROOT, "receipts_bulk")

SYSTEM = """You extract data from a shop receipt.
Return the merchant, the date (YYYY-MM-DD), and the total amount as a number."""


def build_requests():
    """Turn every receipt file into a batch Request with a unique custom_id."""
    requests = []
    for name in sorted(os.listdir(BULK)):
        if not name.endswith(".txt"):
            continue
        with open(os.path.join(BULK, name), encoding="utf-8") as f:
            receipt_text = f.read()

        requests.append(
            Request(
                # custom_id is how we match this receipt to its result later.
                # We use the filename (without .txt) so it is easy to trace.
                custom_id=name.replace(".txt", ""),
                params=MessageCreateParamsNonStreaming(
                    model=MODEL,
                    max_tokens=300,
                    system=SYSTEM,
                    messages=[{"role": "user", "content": receipt_text}],
                ),
            )
        )
    return requests


def main():
    client = get_client()

    if not os.path.isdir(BULK):
        print("No receipts_bulk/ folder. Run:  python generate_receipts.py  first.")
        return

    requests = build_requests()
    print(f"Prepared {len(requests)} receipts for one batch.")

    batch = client.messages.batches.create(requests=requests)

    print("\nBatch submitted!")
    print(f"  Batch ID : {batch.id}")
    print(f"  Status   : {batch.processing_status}")
    print("\nSAVE THAT BATCH ID. Later, check progress with:")
    print(f"    python check_batch.py {batch.id}")
    print("\nA batch can take up to 24 hours (often far less). It will NOT")
    print("finish instantly - that patience is the price of the 50% discount.")


if __name__ == "__main__":
    main()
