"""
answer_with_confidence.py   (the RIGHT way)
==================================================================
Part 5 demo - Task 5.5, the RIGHT way: confidence + human routing

Same questions. But now the assistant reports how CONFIDENT it is in each answer -
based on how well the sources support it - and we use a threshold to ROUTE the shaky
ones to a human reviewer instead of sending them straight to the user.

WHY THIS WORKS
--------------
Not every answer deserves equal trust. By having the model output a confidence level
alongside each answer, we can:

  - send HIGH-confidence answers straight to the user, and
  - ROUTE low-confidence (or "not covered") answers to a human for review.

Human reviewers are limited, so we spend their attention only where it's needed - on
the answers the assistant itself flagged as uncertain. That's calibrated routing.

We get the confidence as STRUCTURED output using tool use (the reliable method from
Domain 4), so it's always a clean value we can compare against a threshold.

HOW TO RUN (from the project root, in cmd):

    python answer_with_confidence.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scholardesk._shared import get_client, MODEL, source_path, list_sources


def load_all_sources():
    out = []
    for name in list_sources():
        with open(source_path(name), encoding="utf-8") as f:
            out.append(f.read())
    return "\n\n".join(out)


QUESTIONS = [
    "What is the running cost per km of an electric two-wheeler?",
    "How many public charging points does Pune have?",
    "What is the 5-year resale value of an electric scooter?",
]

# A tool that forces the model to return an answer AND a confidence level.
ANSWER_TOOL = {
    "name": "answer_user",
    "description": "Answer the user and report how confident you are, based on the sources.",
    "input_schema": {
        "type": "object",
        "properties": {
            "answer": {"type": "string", "description": "The answer to the user."},
            "confidence": {
                "type": "string",
                "enum": ["high", "medium", "low"],
                "description": "high = clearly supported by a source; low = not covered or unsure.",
            },
            "reason": {"type": "string", "description": "One line on why that confidence."},
        },
        "required": ["answer", "confidence", "reason"],
    },
}

SYSTEM = """You are ScholarDesk, a research assistant. Answer using the sources, and
honestly rate your confidence:
- high: a source clearly and directly answers the question.
- medium: partly covered, or requires some interpretation.
- low: the sources do not cover this, or you are unsure.
Use the answer_user tool."""


def route(confidence):
    return "-> sent to user" if confidence == "high" else "-> ROUTED TO HUMAN REVIEW"


def main():
    client = get_client()
    system = SYSTEM + "\n\nSOURCES:\n" + load_all_sources()

    print("\n" + "=" * 64)
    print("  WITH CONFIDENCE  (route shaky answers to a human - the right way)")
    print("=" * 64)

    for q in QUESTIONS:
        response = client.messages.create(
            model=MODEL, max_tokens=400, system=system,
            tools=[ANSWER_TOOL], tool_choice={"type": "tool", "name": "answer_user"},
            messages=[{"role": "user", "content": q}],
        )
        data = next((b.input for b in response.content if b.type == "tool_use"), {})

        print(f"\nQ: {q}")
        print(f"A: {data.get('answer')}")
        print(f"   confidence: {data.get('confidence')}  ({data.get('reason')})")
        print(f"   {route(data.get('confidence'))}")

    print("\n" + "-" * 64)
    print("""  Now the resale-value answer - which the sources don't cover - comes
  back LOW confidence and is routed to a human, instead of going out
  looking authoritative. The two clearly-covered questions come back
  HIGH and go straight to the user.

  Human review time is spent only where the assistant flagged doubt.""")


if __name__ == "__main__":
    main()
