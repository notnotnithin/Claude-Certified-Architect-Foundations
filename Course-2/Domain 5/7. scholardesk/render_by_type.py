"""
render_by_type.py
==================================================================
Part 6 demo - Task 5.6: render each content type in the right format

The last piece of provenance-aware synthesis is presentation. When you combine
information of different KINDS, forcing it all into one uniform format hurts
readability. Numeric data wants a table; a narrative finding wants prose; a set of
steps wants a numbered list.

This script shows the SAME kind of research output rendered three ways, to make the
point that the right format depends on the content type. It does NOT call the API -
it's about presentation choices.

HOW TO RUN (from the project root, in cmd):

    python render_by_type.py
"""

import os
import sys

# 1) Numeric / comparative data -> a TABLE reads best.
COST_TABLE = [
    ("Electric two-wheeler", "Rs 0.25 / km"),
    ("Petrol two-wheeler", "Rs 2.50 / km"),
]

# 2) A narrative finding -> PROSE reads best.
ADOPTION_PROSE = ("EV sales in India crossed 2 million units in 2025-26, with "
                  "two-wheelers making up the largest share, helped by lower running "
                  "costs and FAME subsidies.")

# 3) A how-to -> a NUMBERED LIST reads best.
CHARGING_STEPS = [
    "Use a fast charger to reach about 80% in under an hour.",
    "For a full charge, a standard charger takes several hours.",
    "For two-wheelers, charge overnight at home on a regular socket.",
]


def render_table(rows):
    line = "  " + "-" * 40
    out = [line, f"  {'Vehicle':24}{'Running cost':>14}", line]
    for name, cost in rows:
        out.append(f"  {name:24}{cost:>14}")
    out.append(line)
    return "\n".join(out)


def main():
    print("\n" + "=" * 64)
    print("  RENDER BY CONTENT TYPE")
    print("=" * 64)

    print("\n[1] Numeric / comparative data  ->  TABLE:")
    print(render_table(COST_TABLE))

    print("\n[2] A narrative finding  ->  PROSE:")
    print("  " + ADOPTION_PROSE)

    print("\n[3] A how-to  ->  NUMBERED LIST:")
    for i, step in enumerate(CHARGING_STEPS, 1):
        print(f"  {i}. {step}")

    print("\n" + "-" * 64)
    print("""  Same research, three content types, three formats. A cost comparison
  belongs in a table; an adoption finding reads best as prose; charging
  advice is a numbered list. Forcing all of it into one uniform block -
  all prose, or all bullets - would make it harder to read.

  Matching format to content type is the final piece of presenting
  synthesised information well.""")


if __name__ == "__main__":
    main()
