"""
research_lossy.py   (the ANTI-PATTERN)
==================================================================
Part 1 demo - Task 5.1, the WRONG way: let findings get summarised away

A real research session runs long - you gather facts from several sources over
many turns. To save space, a common (bad) habit is to SUMMARISE the session so far
into a short blurb and carry only that forward. This script imitates that: it keeps
a vague running summary instead of the exact findings.

WHY THIS IS THE ANTI-PATTERN
----------------------------
Progressive summarisation quietly destroys the precise facts research depends on.
"EV two-wheeler running cost is Rs 0.25/km vs Rs 2.50/km for petrol, per the Cost
Brief dated 2026-01-20" becomes "EVs are cheaper to run." The exact numbers, the
source, and the date - the things you actually need to cite - are gone. Later, when
you ask "what were the exact per-km figures, and which source?", the assistant
can't answer, because it summarised them away.

HOW TO RUN (from the project root, in cmd):

    python research_lossy.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scholardesk._shared import ask_claude

SYSTEM = """You are ScholarDesk, a research assistant. You are given a SHORT SUMMARY
of the research session so far, then a follow-up question. Answer using only what you
have."""

# Imagine a long session already happened, reading several EV sources. Instead of the
# real figures, all we kept forward is this vague summary - exactly what progressive
# summarisation produces.
LOSSY_SUMMARY = """Summary so far: We looked into electric vehicles in India. EVs are
selling well and are cheaper to run than petrol vehicles. Charging is mostly in big
cities."""

# The follow-up needs the precise facts that were summarised away.
FOLLOWUP = "What were the exact running-cost figures per km for EV vs petrol, and which source and date did that come from?"


def main():
    print("\n" + "=" * 64)
    print("  LOSSY SUMMARY  (findings summarised away - the anti-pattern)")
    print("=" * 64)

    print("\nWhat we carried forward:")
    print("  " + LOSSY_SUMMARY.replace("\n", " "))
    print(f"\nQuestion: {FOLLOWUP}")

    messages = [
        {"role": "user",
         "content": f"{LOSSY_SUMMARY}\n\nFollow-up question: {FOLLOWUP}"}
    ]
    print("\nScholarDesk:", ask_claude(SYSTEM, messages))

    print("\n" + "-" * 64)
    print("""  The assistant can't give the figures or the source, because the
  summary threw away the exact numbers, the document name, and the
  date. It has to admit it lost them - avoidable, and bad for a tool
  whose whole job is citing facts.

  The fix: never summarise away hard findings. Keep them verbatim in a
  "findings" block. See research_findings.py.""")


if __name__ == "__main__":
    main()
