"""
research_findings.py   (the RIGHT way)
==================================================================
Part 1 demo - Task 5.1, the RIGHT way: a persistent "findings" block

Same long research session. But instead of summarising the facts away, we pull the
hard findings - figures, dates, source names - into a "KEY FINDINGS" block that we
include in EVERY prompt, word for word. The narrative can be summarised; the facts
never are.

WHY THIS WORKS
--------------
The precise, citable details (numbers, dates, source names) live in a fixed block
that is always present and never condensed. So no matter how long the session runs,
the assistant can always answer "what were the exact figures, and from where?"
exactly. We also place that block at the TOP of the prompt - because models attend
most reliably to the beginning and end of a long input, and least to the middle
("lost in the middle").

HOW TO RUN (from the project root, in cmd):

    python research_findings.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scholardesk._shared import ask_claude

SYSTEM = """You are ScholarDesk, a research assistant. A KEY FINDINGS block holds the
verified, exact facts gathered so far, each with its source and date. Always trust
and use the KEY FINDINGS for anything involving figures, dates, or which source a
fact came from."""

# The hard findings, kept verbatim - never summarised. This block rides along in
# every prompt, placed FIRST so it's in the most reliably-read position.
KEY_FINDINGS = """KEY FINDINGS (verified, do not alter):
- EV two-wheeler running cost: Rs 0.25/km; petrol: Rs 2.50/km
  [source: EV Ownership Cost Brief, 2026-01-20]
- Typical EV two-wheeler on-road price in Pune: Rs 1.10 lakh
  [source: EV Ownership Cost Brief, 2026-01-20]
- India EV sales 2025-26: crossed 2 million units
  [source: India EV Adoption Report, 2026-03-10]
- Pune public charging points: ~350 as of early 2026
  [source: Public Charging Note, 2026-02-05]"""

# The narrative CAN be summarised - that part is fine to compress.
NARRATIVE_SUMMARY = "Narrative: we reviewed adoption, cost, and charging for EVs in India, focused on Pune."

FOLLOWUP = "What were the exact running-cost figures per km for EV vs petrol, and which source and date did that come from?"


def main():
    print("\n" + "=" * 64)
    print("  KEY FINDINGS BLOCK  (facts kept verbatim - the right way)")
    print("=" * 64)

    print("\nWhat we carry forward (facts kept exact, only narrative summarised):")
    print(KEY_FINDINGS)
    print(f"\nQuestion: {FOLLOWUP}")

    # The prompt puts KEY FINDINGS first (best-read position), then the summarised
    # narrative, then the follow-up question.
    user_content = (
        f"{KEY_FINDINGS}\n\n"
        f"{NARRATIVE_SUMMARY}\n\n"
        f"Follow-up question: {FOLLOWUP}"
    )
    print("\nScholarDesk:", ask_claude(SYSTEM, [{"role": "user", "content": user_content}]))

    print("\n" + "-" * 64)
    print("""  Now the assistant answers exactly - the figures (Rs 0.25/km vs
  Rs 2.50/km), the source (Cost Brief), and the date (2026-01-20) -
  because those were kept verbatim in the KEY FINDINGS block instead of
  being summarised into mush.

  Two ideas together: (1) keep hard facts in a persistent block, and
  (2) put that block FIRST, where the model reads most reliably.""")


if __name__ == "__main__":
    main()
