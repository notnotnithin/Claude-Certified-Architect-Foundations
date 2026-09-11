"""
stops.py
--------
Builds and validates a single trip "stop".

A stop is just a small dictionary, for example:
    {"place": "Jaipur", "date": "2026-10-02", "nights": 3}

Keeping the "what does a valid stop look like?" rules in one module means that
later, when we add path-specific rules or ask Claude Code to review the code,
all the validation logic lives in a predictable place.
"""

from datetime import datetime


def make_stop(place, date, nights):
    """
    Build a validated stop dictionary from three plain values.

    Raises ValueError with a clear message if anything is wrong, so the CLI can
    show the user a friendly error instead of a confusing crash.
    """
    place = (place or "").strip()
    if not place:
        raise ValueError("Place cannot be empty.")

    # validate_date does the heavy lifting and raises if the date is bad.
    validate_date(date)

    try:
        nights = int(nights)
    except (TypeError, ValueError):
        raise ValueError(f"Nights must be a whole number, got: {nights!r}")

    if nights < 1:
        raise ValueError("Nights must be at least 1.")

    return {"place": place, "date": date, "nights": nights}


def validate_date(date):
    """
    Check that 'date' is a real calendar date in YYYY-MM-DD form.

    We use a strict format so the whole app stores dates the same way. This
    single check is exactly the kind of small, well-scoped change we point to in
    Part 3 when we talk about 'direct execution' vs 'plan mode'.
    """
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except (TypeError, ValueError):
        raise ValueError(
            f"Date must look like YYYY-MM-DD (example: 2026-10-02), got: {date!r}"
        )
    return True
