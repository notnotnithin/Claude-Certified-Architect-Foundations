"""
test_stops.py
-------------
Small, plain tests for the stop-building and date-validation logic.

You can run these with:
    python -m pytest tests/test_stops.py
(after installing pytest), OR just read them to see what "valid" means.

We keep some test files here in tests/ and ONE test file next to the code it
tests (destinations/test_date_beside_module.py). That mix is on purpose: in
Part 1 we show how a single '.claude/rules/' file with a glob pattern can cover
test files wherever they live, which a folder-bound CLAUDE.md cannot do easily.
"""

from destinations.stops import make_stop, validate_date


def test_make_stop_builds_a_clean_dictionary():
    stop = make_stop("Jaipur", "2026-10-02", 3)
    assert stop == {"place": "Jaipur", "date": "2026-10-02", "nights": 3}


def test_make_stop_trims_whitespace_from_place():
    stop = make_stop("  Goa  ", "2026-11-05", 2)
    assert stop["place"] == "Goa"


def test_make_stop_rejects_empty_place():
    try:
        make_stop("", "2026-10-02", 3)
        assert False, "expected a ValueError for empty place"
    except ValueError:
        pass


def test_validate_date_accepts_a_real_date():
    assert validate_date("2026-10-02") is True


def test_validate_date_rejects_a_bad_format():
    try:
        validate_date("02-10-2026")  # wrong order
        assert False, "expected a ValueError for bad date format"
    except ValueError:
        pass
