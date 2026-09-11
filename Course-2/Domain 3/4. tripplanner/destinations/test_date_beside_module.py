"""
test_date_beside_module.py
--------------------------
This test lives NEXT TO the code it tests (inside destinations/), not in the
tests/ folder. That is common in real projects.

Why it's here: in Part 1 (Task 3.3) we use a '.claude/rules/' file whose glob
pattern is  paths: ["**/test_*.py"].  That single pattern catches THIS file and
the ones in tests/ alike — no matter which folder they sit in. A directory-level
CLAUDE.md could not do that as cleanly. This file is the concrete proof.
"""

from destinations.stops import validate_date


def test_validate_date_rejects_february_30():
    try:
        validate_date("2026-02-30")  # not a real calendar day
        assert False, "expected a ValueError for an impossible date"
    except ValueError:
        pass
