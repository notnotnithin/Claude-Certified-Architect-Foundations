"""
escalate_vague.py   (the ANTI-PATTERN)
==================================================================
Part 2 demo - Task 5.2, the WRONG way: escalate on the wrong signals

ScholarDesk has to decide: answer from the sources itself, or hand the question to
a human expert? The tempting (bad) approach is to escalate based on how HARD the
question feels or how demanding the user sounds. This script tells the bot exactly
that.

WHY THIS IS THE ANTI-PATTERN
----------------------------
"Difficulty" and tone are UNRELIABLE signals for whether a question actually needs
a human. The result is miscalibrated:

  - A well-covered question that merely SOUNDS demanding gets escalated needlessly.
  - A question the sources simply DON'T COVER gets a confident, made-up answer,
    because the bot didn't judge it "hard" - when that is exactly the case a human
    should handle.

We run three questions to show it escalate the wrong ones.

HOW TO RUN (from the project root, in cmd):

    python escalate_vague.py
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


# Vague guidance: escalate based on difficulty/tone. No real criteria.
VAGUE_SYSTEM = """You are ScholarDesk, a research assistant. Decide whether to answer
the question yourself from the sources, or escalate to a human expert.

Escalate if the question seems hard or the user sounds demanding. Otherwise, answer
it yourself. Start your reply with either "ANSWER:" or "ESCALATE:"."""

QUESTIONS = [
    # Fully covered by the sources, just phrased forcefully - should NOT escalate.
    "I need this NOW: what is the exact running cost per km of an electric two-wheeler?",
    # NOT covered by any source (resale value) - SHOULD go to a human expert.
    "What is the 5-year resale value of an electric scooter in Pune?",
    # Explicitly asks for a human expert - should be honored immediately.
    "Can you have a human research expert look into this for me?",
]


def main():
    sources = load_all_sources()
    system = VAGUE_SYSTEM + "\n\nSOURCES:\n" + sources

    print("\n" + "=" * 64)
    print("  VAGUE ESCALATION  (difficulty + tone - the anti-pattern)")
    print("=" * 64)

    for q in QUESTIONS:
        print(f"\nUser: {q}")
        reply = ask_claude(system, [{"role": "user", "content": q}])
        print(f"ScholarDesk: {reply}")

    print("\n" + "-" * 64)
    print("""  Watch the mismatches. The forcefully-phrased but fully-covered cost
  question may get ESCALATED (over tone) when the bot could just answer
  it. The resale-value question - which NO source covers - may get
  ANSWERED with a made-up number, even though a missing-coverage case
  is exactly when a human should step in.

  Difficulty and tone are the wrong signals. See escalate_criteria.py.""")


if __name__ == "__main__":
    main()
