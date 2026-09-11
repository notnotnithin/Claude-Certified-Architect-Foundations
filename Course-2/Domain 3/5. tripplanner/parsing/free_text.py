"""
free_text.py
------------
Turns a short free-text line like:

    "Jaipur 2026-10-02 3"

into a structured stop:

    {"place": "Jaipur", "date": "2026-10-02", "nights": 3}

IMPORTANT (for students):
This Part 0 version is a SIMPLE, rule-based parser. It just splits the line by
spaces and expects the exact order:  place  date  nights.

In Part 3 (the live-API demo) we replace this with a real Claude call that can
understand messy, natural input like "3 nights in Jaipur from Oct 2". For now,
this keeps the whole app runnable on your machine with NO API key needed.
"""

from destinations.stops import make_stop


def parse_line(line):
    """
    Parse a simple 'place date nights' line into a validated stop.

    This is intentionally strict and unclever. Its only job in Part 0 is to let
    the app run end-to-end. Real natural-language understanding arrives in Part 3.
    """
    parts = (line or "").split()
    if len(parts) != 3:
        raise ValueError(
            "Expected exactly: <place> <YYYY-MM-DD> <nights>\n"
            '   Example:  Jaipur 2026-10-02 3'
        )

    place, date, nights = parts
    # make_stop validates everything and raises a clear error if something is off.
    return make_stop(place, date, nights)
