"""
check_batch.py
==================================================================
Part 5 demo - Task 4.5: check a batch and process its results

After submitting a batch with submit_batch.py, you come back later and run this
to see whether it has finished and to read the results.

WHAT THIS SCRIPT DOES
---------------------
1. Retrieves the batch status.
2. If it has "ended", reads each result and matches it back to its receipt using
   the custom_id.
3. Separates SUCCEEDED from FAILED results - because the right way to handle a
   partial failure is to resubmit ONLY the failed ones, by custom_id.

DEMO MODE (so you don't wait 24 hours on camera):
A real batch can take hours. So this script also accepts the word "sample" instead
of a batch id, and reads a pre-saved results file (sample_batch_results.jsonl).
That lets you demonstrate the "read and sort the results" step immediately.

HOW TO RUN (from the project root, in cmd):

    python check_batch.py sample                 (use the pre-saved results)
    python check_batch.py msgbatch_XXXXXXXX       (use your real batch id)
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.abspath(__file__))
SAMPLE_FILE = os.path.join(ROOT, "sample_batch_results.jsonl")


def process_results(results):
    """
    Sort results into succeeded and failed, keyed by custom_id.

    'results' is a list of dicts, each with a 'custom_id' and a 'result' whose
    'type' is 'succeeded' or 'errored'/'expired'. This is the shape the real API
    returns (and the shape of our sample file).
    """
    succeeded = []
    failed = []
    for r in results:
        cid = r.get("custom_id")
        rtype = r.get("result", {}).get("type")
        if rtype == "succeeded":
            succeeded.append(cid)
        else:
            failed.append(cid)

    print("\n" + "=" * 60)
    print("  BATCH RESULTS")
    print("=" * 60)
    print(f"  Total    : {len(results)}")
    print(f"  Succeeded: {len(succeeded)}")
    print(f"  Failed   : {len(failed)}")

    if failed:
        print("\n  These custom_ids FAILED and should be resubmitted:")
        for cid in failed:
            print(f"    - {cid}")
        print("\n  The right fix is to resubmit ONLY these - not the whole batch.")
        print("  You match them by custom_id, correct the input if needed")
        print("  (e.g. chunk a receipt that was too long), and send a new batch.")
    else:
        print("\n  All receipts processed successfully.")

    # Show one succeeded result so students see the data came back.
    for r in results:
        if r.get("result", {}).get("type") == "succeeded":
            body = r["result"]["message"]["content"][0]["text"]
            print(f"\n  Example result for {r['custom_id']}:")
            print(f"    {body}")
            break


def run_sample():
    """Read the pre-saved results file so the demo works without waiting."""
    print("DEMO MODE: reading pre-saved results (sample_batch_results.jsonl).")
    print("This is what check_batch.py would show once a real batch has ended.")
    results = []
    with open(SAMPLE_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    process_results(results)


def run_real(batch_id):
    """Retrieve a real batch, poll status, and process results when ended."""
    from billbox._shared import get_client
    client = get_client()

    batch = client.messages.batches.retrieve(batch_id)
    print(f"Batch {batch_id}")
    print(f"  Status: {batch.processing_status}")

    if batch.processing_status != "ended":
        # request_counts shows how many are still processing.
        counts = batch.request_counts
        print(f"  Still working: {counts.processing} processing, "
              f"{counts.succeeded} done, {counts.errored} errored.")
        print("\n  Not finished yet. Come back later and run this again.")
        print("  (A batch can take up to 24 hours; usually much less.)")
        return

    # Ended - stream the results and sort them.
    results = []
    for result in client.messages.batches.results(batch_id):
        # The SDK yields typed objects; convert to the simple dict shape our
        # process_results() expects.
        results.append({
            "custom_id": result.custom_id,
            "result": {"type": result.result.type,
                       "message": _message_dict(result)},
        })
    process_results(results)


def _message_dict(result):
    """Pull the text out of a succeeded result, or return empty for failures."""
    try:
        if result.result.type == "succeeded":
            text = result.result.message.content[0].text
            return {"content": [{"text": text}]}
    except Exception:
        pass
    return {"content": [{"text": ""}]}


def main(argv):
    if not argv:
        print(__doc__)
        print("ERROR: pass 'sample' or a real batch id.")
        return

    target = argv[0]
    if target == "sample":
        run_sample()
    else:
        run_real(target)


if __name__ == "__main__":
    main(sys.argv[1:])
