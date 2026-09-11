"""
escalate_criteria.py   (the RIGHT way)
==================================================================
Part 2 demo - Task 5.2, the RIGHT way: explicit escalation criteria

Same three questions. But now the bot escalates on EXPLICIT triggers, not on how
hard the question feels - and we give it few-shot examples so the boundary is
crystal clear.

THE RIGHT TRIGGERS (from the exam, mapped to research)
------------------------------------------------------
Escalate to a human expert when:
  1. the user explicitly asks for a human (honor it immediately),
  2. the SOURCES DON'T COVER the question (a coverage gap - the research version of
     a "policy gap"; not just "hard" questions),
  3. the bot genuinely can't make progress (e.g. sources conflict unresolvably).

Otherwise, ANSWER it from the sources. A forcefully-phrased question that IS covered
still gets a direct answer - the user's tone is NOT a reason to escalate.

HOW TO RUN (from the project root, in cmd):

    python escalate_criteria.py
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


# Explicit criteria + few-shot examples showing the boundary.
CRITERIA_SYSTEM = """You are ScholarDesk, a research assistant. Decide whether to
answer from the sources yourself or escalate to a human expert.

ESCALATE only if one of these is true:
  (a) the user explicitly asks for a human expert - honor this immediately;
  (b) the SOURCES DO NOT COVER the question (a coverage gap);
  (c) you genuinely cannot make progress (e.g. sources conflict and you can't
      resolve which is right).

Otherwise ANSWER it from the sources. If a question is fully covered but phrased
forcefully or urgently, still just answer it - tone is NOT a reason to escalate.

Examples:
User: "URGENT!! how many EVs were sold in India?"
Reply: ANSWER: (covered by the adoption report - tone doesn't matter)

User: "Which insurer is cheapest for an EV in Pune?"
Reply: ESCALATE: (no source covers insurance - a coverage gap)

Start your reply with "ANSWER:" or "ESCALATE:" and a short reason."""

QUESTIONS = [
    "I need this NOW: what is the exact running cost per km of an electric two-wheeler?",
    "What is the 5-year resale value of an electric scooter in Pune?",
    "Can you have a human research expert look into this for me?",
]


def main():
    sources = load_all_sources()
    system = CRITERIA_SYSTEM + "\n\nSOURCES:\n" + sources

    print("\n" + "=" * 64)
    print("  EXPLICIT CRITERIA  (the right triggers - the right way)")
    print("=" * 64)

    for q in QUESTIONS:
        print(f"\nUser: {q}")
        reply = ask_claude(system, [{"role": "user", "content": q}])
        print(f"ScholarDesk: {reply}")

    print("\n" + "-" * 64)
    print("""  Now the decisions line up with reality:
    - urgent-but-covered cost question -> ANSWER (tone doesn't matter)
    - resale value (no source covers it) -> ESCALATE (coverage gap)
    - "have a human look into this"      -> ESCALATE (explicit request)

  Difficulty and tone stopped driving the decision; the actual triggers
  do: explicit request, missing coverage, or being genuinely stuck.""")


if __name__ == "__main__":
    main()
