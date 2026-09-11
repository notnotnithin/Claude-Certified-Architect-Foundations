"""
local_recovery.py
==================================================================
Part 3 demo - Task 5.3: recover locally, and annotate coverage gaps

When a source fetch hits a TRANSIENT failure (a timeout, a brief service blip), the
right move is to try to fix it RIGHT THERE - retry a couple of times - before
escalating the problem up. And when one source genuinely can't be reached, we don't
silently drop it or abandon the whole task: we finish with the sources we have, and
ANNOTATE which parts are well-supported versus which have a gap.

WHY THIS MATTERS
----------------
Three anti-patterns to avoid:
  - Terminating the whole research task on the first hiccup (a quick retry would fix
    it).
  - Propagating a bare error with no context (whoever receives it is blind).
  - Silently pretending a missing source was empty (hiding a real gap).

This script simulates a flaky source that fails twice then succeeds, then shows a
synthesis that clearly marks a coverage gap where one source stayed unavailable.

HOW TO RUN (from the project root, in cmd):

    python local_recovery.py
"""

import os
import sys

# A flaky source: fails the first two times (transient), then works.
_attempts = {"count": 0}


def flaky_fetch(source_name):
    """Simulate a source that is briefly unavailable, then recovers."""
    _attempts["count"] += 1
    if _attempts["count"] < 3:
        return {
            "ok": False,
            "error_type": "transient",
            "retryable": True,
            "attempted": f"fetch {source_name}",
            "message": "Source temporarily unavailable.",
        }
    return {"ok": True, "results": "…adoption figures…"}


def fetch_with_local_recovery(source_name, max_retries=3):
    """Try the fetch; retry locally on transient failure before giving up."""
    story = []
    for attempt in range(1, max_retries + 1):
        result = flaky_fetch(source_name)
        if result.get("ok"):
            story.append(f"Attempt {attempt}: success.")
            return result, story
        if result.get("retryable"):
            story.append(f"Attempt {attempt}: transient failure - retrying locally "
                         f"(user sees nothing).")
            continue
        story.append(f"Attempt {attempt}: non-retryable - stop and report.")
        return result, story
    story.append("Local recovery exhausted - propagate a structured error.")
    return {"ok": False, "error_type": "transient", "retryable": True,
            "attempted": f"fetch {source_name}",
            "message": "Still unavailable after retries."}, story


def synthesis_with_coverage(available, missing):
    """
    Build a short synthesis that is HONEST about coverage: which topics are
    well-supported by a source, and which have a gap because a source was missing.
    """
    print("\nSynthesis (with coverage annotations):")
    for topic, src in available:
        print(f"  [well-supported] {topic}  (source: {src})")
    for topic, src in missing:
        print(f"  [GAP] {topic}  - could not be covered ({src} unavailable)")


def main():
    print("\n" + "=" * 64)
    print("  LOCAL RECOVERY + COVERAGE ANNOTATIONS")
    print("=" * 64)

    print("\n[1] A flaky source (fails twice, then works). Retry loop handles it:\n")
    _attempts["count"] = 0
    result, story = fetch_with_local_recovery("ev_adoption_report.txt")
    for line in story:
        print("  " + line)
    if result.get("ok"):
        print("\n  Recovered locally - the user never saw a hiccup.")

    print("\n[2] Suppose a DIFFERENT source stayed down after all retries.")
    print("    We don't abandon the task or hide the gap - we annotate it:")
    synthesis_with_coverage(
        available=[("EV adoption figures", "ev_adoption_report.txt"),
                   ("running costs", "ev_cost_brief.txt")],
        missing=[("charging infrastructure", "ev_charging_note.txt")],
    )

    print("\n" + "-" * 64)
    print("""  Transient failures were handled locally with retries - the task was
  never abandoned over a temporary blip. And where a source genuinely
  couldn't be reached, the synthesis MARKS the gap instead of hiding it,
  so the reader knows exactly what is and isn't well-supported.""")


if __name__ == "__main__":
    main()
