"""
error_generic.py   (the ANTI-PATTERN)
==================================================================
Part 3 demo - Task 5.3, the WRONG way: generic, contextless errors

ScholarDesk pulls in sources to answer a question - fetching a document, searching
a source set. Those operations sometimes fail. The lazy way to report a failure is
a single generic message: "Source error." This script shows why that wrecks the
assistant's ability to recover.

WHY THIS IS THE ANTI-PATTERN
----------------------------
A generic error hides everything the assistant needs to decide what to do next:

  - Was it a temporary timeout it should just retry?
  - Was the source id invalid, so retrying is pointless?
  - Did the search succeed but simply find nothing relevant?

All three collapse into "Source error." So the assistant either gives up when it
could have retried, retries forever when it shouldn't, or tells the user "something
went wrong" when actually the search just found no match.

This script simulates a source tool that returns generic errors, and shows the
assistant guessing badly.

HOW TO RUN (from the project root, in cmd):

    python error_generic.py
"""

import os
import sys


def fetch_source_generic(scenario):
    """A source tool that reports every failure the same lazy way."""
    return {"error": "Source error"}


SCENARIOS = ["timeout", "bad_source_id", "no_match"]


def assistant_decision(result):
    """What can the assistant do with a generic error? Almost nothing useful."""
    if "error" in result:
        return ("The assistant only sees 'Source error'. It cannot tell a timeout "
                "from a bad source id from an empty search, so it just tells the user "
                "'something went wrong' - and can't recover.")
    return "ok"


def main():
    print("\n" + "=" * 64)
    print("  GENERIC ERRORS  (contextless - the anti-pattern)")
    print("=" * 64)

    for sc in SCENARIOS:
        result = fetch_source_generic(sc)
        print(f"\nWhat really happened: {sc}")
        print(f"Tool returned:        {result}")
        print(f"Assistant can do:     {assistant_decision(result)}")

    print("\n" + "-" * 64)
    print("""  Three totally different situations - a temporary timeout, an invalid
  source id, and a perfectly good search that found nothing relevant -
  all come back as the SAME 'Source error'. The assistant is blind, so
  it can't retry the timeout, skip the bad id, or calmly report 'no
  relevant source found'.

  The fix is structured error context. See error_structured.py.""")


if __name__ == "__main__":
    main()
