r"""
ci_review.py
==================================================================
Part 4 demo — turning Claude's JSON into PR comments (Task 3.6)

WHAT THIS IS
------------
In a real CI/CD pipeline, nobody reads Claude's output. A MACHINE does. The
pipeline needs to take Claude's findings and post them as comments on the pull
request, then decide whether to pass or fail the build.

This script is that machine step. It takes the JSON that
`claude -p --output-format json --json-schema` produced, reads the findings, and:

  1. prints each finding the way a PR comment would look,
  2. counts them by severity,
  3. exits with code 0 (pass) or 1 (fail) so the pipeline can block a merge.

That last point is the whole reason we asked for JSON in the first place. You
cannot reliably write "if there are high-severity bugs, fail the build" against a
paragraph of English prose. You can against structured data.

HOW TO RUN (in cmd, from the project folder):

    python ci\ci_review.py ci\sample-review.json

Or on the real output you generated in Block 1:

    python ci\ci_review.py ci\review-output.json

No API key needed - this script only READS a JSON file.
"""

import json
import sys


def load_review(path):
    """
    Read the review JSON produced by Claude Code.

    `claude -p --output-format json --json-schema ...` wraps the schema-shaped
    answer inside a "structured_output" field, alongside metadata like
    session_id and total_cost_usd. We accept either the full wrapper OR a plain
    findings object, so this works with real output and with our sample file.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Real CLI output: the answer lives under "structured_output".
    if isinstance(data, dict) and "structured_output" in data:
        return data["structured_output"], data

    # Already the bare object (our sample file).
    return data, None


def severity_marker(severity):
    """A simple text marker so severity is scannable in the terminal."""
    return {
        "high": "[HIGH]  ",
        "medium": "[MEDIUM]",
        "low": "[LOW]   ",
    }.get(severity, "[?]     ")


def main(argv):
    if not argv:
        print(__doc__)
        print("ERROR: pass the review JSON file, e.g.")
        print("    python ci\\ci_review.py ci\\sample-review.json")
        return 2

    path = argv[0]

    try:
        review, wrapper = load_review(path)
    except FileNotFoundError:
        print(f"Could not find: {path}")
        return 2
    except json.JSONDecodeError as e:
        print(f"That file is not valid JSON: {e}")
        return 2

    findings = review.get("findings", [])
    verdict = review.get("verdict", "unknown")

    print()
    print("=" * 64)
    print("  WHAT THE CI PIPELINE WOULD POST ON THE PULL REQUEST")
    print("=" * 64)

    if not findings:
        print("\n  No issues found. Nothing to comment.\n")
    else:
        for f in findings:
            print()
            print(f"  {severity_marker(f.get('severity'))} {f.get('file')}:{f.get('line')}")
            print(f"     {f.get('issue')}")
            print(f"     Suggestion: {f.get('suggestion')}")

    # Count by severity - this is what the pass/fail decision is built on.
    counts = {"high": 0, "medium": 0, "low": 0}
    for f in findings:
        sev = f.get("severity")
        if sev in counts:
            counts[sev] += 1

    print()
    print("-" * 64)
    print(f"  Findings: {counts['high']} high, {counts['medium']} medium, {counts['low']} low")
    print(f"  Claude's verdict: {verdict}")

    # If the real CLI wrapper was present, show the metadata CI teams care about.
    if wrapper:
        cost = wrapper.get("total_cost_usd")
        if cost is not None:
            print(f"  This run cost: ${cost}")

    # THE GATE. A machine decision, made from structured data.
    # Our rule: any high-severity finding blocks the merge.
    print("-" * 64)
    if counts["high"] > 0:
        print("  RESULT: FAIL - high-severity issues must be fixed before merge.")
        print("  (exit code 1 - the pipeline stops here)")
        print()
        return 1

    print("  RESULT: PASS - no high-severity issues.")
    print("  (exit code 0 - the pipeline continues)")
    print()
    return 0


if __name__ == "__main__":
    # The exit code is how CI knows whether to continue. This is not decoration.
    sys.exit(main(sys.argv[1:]))
