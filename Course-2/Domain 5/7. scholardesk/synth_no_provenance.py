"""
synth_no_provenance.py   (the ANTI-PATTERN)
==================================================================
Part 6 demo - Task 5.6, the WRONG way: synthesis that loses its sources

ScholarDesk's whole job is answering from SEVERAL sources at once. The lazy way is
to blend them into one smooth answer and move on. This script does that: it merges
all the sources and answers, with no tracking of which fact came from which document.

WHY THIS IS THE ANTI-PATTERN
----------------------------
Two problems appear the moment you synthesise without provenance:

  1. SOURCE ATTRIBUTION IS LOST. The answer states facts with no idea which source
     backs each one. If the user asks "says who?", you can't say where it came from -
     a fatal flaw for a research tool.

  2. CONFLICTS GET RESOLVED ARBITRARILY. Two of our sources DISAGREE on Pune's
     charging-point count - the newer adoption report says ~480, the older charging
     note says ~350. A blended answer just picks one (often whichever it read last)
     and states it as fact, hiding that there was ever a conflict.

HOW TO RUN (from the project root, in cmd):

    python synth_no_provenance.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scholardesk._shared import ask_claude, source_path, list_sources


def load_all_sources():
    out = []
    for name in list_sources():
        with open(source_path(name), encoding="utf-8") as f:
            out.append(f.read())
    return "\n\n".join(out)


SYSTEM = """You are ScholarDesk, a research assistant. Answer the user's question
using the sources below. Give one smooth, combined answer."""

QUESTION = "How many public charging points does Pune have, and how is EV adoption going?"


def main():
    system = SYSTEM + "\n\nSOURCES:\n" + load_all_sources()

    print("\n" + "=" * 64)
    print("  NO PROVENANCE  (blended answer - the anti-pattern)")
    print("=" * 64)
    print(f"\nUser: {QUESTION}")
    print("\nScholarDesk:", ask_claude(system, [{"role": "user", "content": QUESTION}]))

    print("\n" + "-" * 64)
    print("""  Notice two things:
    - The answer cites NO sources - you can't tell which document any
      given fact came from.
    - The two sources DISAGREE on the charging count (480 vs 350), but
      the blended answer likely states ONE number as if it were settled,
      hiding the conflict entirely.

  The fix keeps each fact tied to its source and flags the conflict
  using the sources' dates. See synth_with_provenance.py.""")


if __name__ == "__main__":
    main()
