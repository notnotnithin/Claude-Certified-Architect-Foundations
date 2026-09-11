"""
trip_store.py
-------------
Loads and saves the trip to a JSON file on disk.

This is the ONLY part of TripPlanner that touches the file system. Keeping all
file reading/writing in one small module (instead of spreading it across the
whole app) is a deliberate design choice: later, when Asha asks Claude Code to
change how trips are stored, Claude only has to look in one place.
"""

import json
import os

# The trip is saved next to this project as a simple JSON file.
TRIP_FILE = "my_trip.json"


def load_trip():
    """
    Read the saved trip from disk and return it as a list of stops.

    If no trip file exists yet (the very first run), we return an empty list
    instead of crashing. That way a brand-new user starts with an empty trip.
    """
    if not os.path.exists(TRIP_FILE):
        return []

    # encoding="utf-8" matters: place names like "Jaipur" or "Còn Đảo" can
    # contain non-ASCII characters, and the default Windows encoding may choke
    # on them. Being explicit here avoids a UnicodeDecodeError.
    with open(TRIP_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_trip(stops):
    """
    Write the full list of stops back to disk as JSON.

    We always write the WHOLE list, not just the new stop. This keeps the code
    simple: the file on disk is always an exact copy of the stops we hold in
    memory.
    """
    with open(TRIP_FILE, "w", encoding="utf-8") as f:
        # indent=2 makes the JSON file human-readable if you open it in VS Code.
        # ensure_ascii=False keeps "Jaipur"-style names readable instead of
        # turning them into escape codes.
        json.dump(stops, f, indent=2, ensure_ascii=False)
