"""
error_structured.py   (the RIGHT way)
==================================================================
Part 3 demo - Task 5.3, the RIGHT way: structured error context

Same failures, but now each one comes back as STRUCTURED information the assistant
can act on: what kind of failure, whether it's worth retrying, what was attempted,
and any partial results.

WHY THIS WORKS
--------------
With structure, the assistant makes the RIGHT recovery move for each case:

  - a transient timeout        -> retry locally (don't bother the user)
  - an invalid source id       -> don't retry; report the bad reference
  - a valid empty search       -> not an error at all; report "no relevant source
                                  found" - which is a real, useful answer

Two ideas from the exam live here:
  1. Structured error context (type, retryable, attempted query, partial results).
  2. The crucial difference between an ACCESS FAILURE (couldn't run the search) and
     a VALID EMPTY RESULT (search ran fine, found nothing). Collapsing these is a
     classic bug.

HOW TO RUN (from the project root, in cmd):

    python error_structured.py
"""

import os
import sys


def fetch_source_structured(scenario):
    """A source tool that reports each failure with useful structure."""
    if scenario == "timeout":
        return {
            "ok": False,
            "error_type": "transient",       # temporary - safe to retry
            "retryable": True,
            "attempted": "fetch ev_adoption_report.txt",
            "message": "Source service timed out after 5s.",
        }
    if scenario == "bad_source_id":
        return {
            "ok": False,
            "error_type": "validation",      # bad reference - retrying won't help
            "retryable": False,
            "attempted": "fetch ev_taxes_2027.txt",
            "message": "No source named 'ev_taxes_2027.txt' exists.",
        }
    if scenario == "no_match":
        # IMPORTANT: this is NOT an error. The search ran fine and found nothing.
        return {
            "ok": True,                       # the access succeeded...
            "results": [],                    # ...it just found no relevant source
            "attempted": "search sources for 'EV resale value'",
        }
    return {"ok": True, "results": ["..."]}


def assistant_recovery(result):
    """Pick the right recovery move from the structured result."""
    # First: did the access succeed? An empty result with ok=True is a valid answer.
    if result.get("ok"):
        if result.get("results") == []:
            return ("VALID EMPTY RESULT: the search worked and found nothing relevant. "
                    "Report 'no source covers this' plainly - that is a real answer, "
                    "not a failure (and a good moment to escalate, per Part 2).")
        return "Success with data."

    # Otherwise it's a real failure - use the structure to decide.
    if result.get("error_type") == "transient" and result.get("retryable"):
        return ("TRANSIENT: retry locally once or twice before bothering anyone. "
                f"(was attempting: {result['attempted']})")
    if result.get("error_type") == "validation":
        return ("VALIDATION: retrying won't help - the source reference is wrong. "
                f"Report the bad reference. ({result['message']})")
    return "Unknown failure - propagate with what we know."


SCENARIOS = ["timeout", "bad_source_id", "no_match"]


def main():
    print("\n" + "=" * 64)
    print("  STRUCTURED ERRORS  (context the assistant can act on - the right way)")
    print("=" * 64)

    for sc in SCENARIOS:
        result = fetch_source_structured(sc)
        print(f"\nWhat really happened: {sc}")
        print(f"Tool returned:        {result}")
        print(f"Assistant recovery:   {assistant_recovery(result)}")

    print("\n" + "-" * 64)
    print("""  Now each case gets the RIGHT response: retry the timeout, reject the
  bad source id, and report 'no relevant source' calmly (because that
  empty result is a success, not a failure).

  Two anti-patterns this also avoids: silently hiding an error (which
  loses information), and killing the whole research task on one failure
  (when a local retry would have fixed it).""")


if __name__ == "__main__":
    main()
