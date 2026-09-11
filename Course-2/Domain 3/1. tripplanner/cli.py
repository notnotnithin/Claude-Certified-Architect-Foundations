"""
cli.py
------
The main entry point for TripPlanner.

Run it from the 'tripplanner' folder like this:

    python cli.py add "Jaipur 2026-10-02 3"
    python cli.py list

TripPlanner is a tiny command-line app that remembers the stops on your trip.
It is deliberately small: the point of this course is to learn how to CONFIGURE
Claude Code around a real Python project, not to build a complicated app.

How the pieces fit together:
    parsing/free_text.py   -> turns your text into a stop
    destinations/stops.py  -> checks the stop is valid
    storage/trip_store.py  -> saves/loads the trip to a JSON file
    cli.py (this file)     -> the commands you actually type
"""

import sys

from parsing.free_text import parse_line
from storage.trip_store import load_trip, save_trip


def cmd_add(text):
    """Add one stop to the trip and save it."""
    try:
        stop = parse_line(text)
    except ValueError as e:
        # A friendly, expected error (bad input) — not a crash.
        print(f"Could not add that stop.\n   {e}")
        return

    stops = load_trip()
    stops.append(stop)
    save_trip(stops)
    print(f"Added: {stop['nights']} night(s) in {stop['place']} from {stop['date']}")


def cmd_list():
    """Show the whole trip, one stop per line, in date order."""
    stops = load_trip()

    if not stops:
        print("Your trip is empty. Add a stop, for example:")
        print('   python cli.py add "Jaipur 2026-10-02 3"')
        return

    # Sort by date so the trip reads top-to-bottom in the order you'll travel.
    stops = sorted(stops, key=lambda s: s["date"])

    print("Your trip:")
    print("-" * 40)
    for i, stop in enumerate(stops, start=1):
        print(f"{i}. {stop['place']}")
        print(f"   arrive {stop['date']}, stay {stop['nights']} night(s)")
    print("-" * 40)
    print(f"Total stops: {len(stops)}")


def main(argv):
    """
    Read the command the user typed and run the matching function.

    We keep this simple on purpose: one 'add' command and one 'list' command.
    """
    if len(argv) < 1:
        print_help()
        return

    command = argv[0]

    if command == "add":
        if len(argv) < 2:
            print('Please provide the stop text, e.g.  python cli.py add "Jaipur 2026-10-02 3"')
            return
        cmd_add(argv[1])
    elif command == "list":
        cmd_list()
    else:
        print(f"Unknown command: {command!r}")
        print_help()


def print_help():
    """Show the two commands TripPlanner understands."""
    print("TripPlanner - a tiny trip itinerary tracker")
    print()
    print("Commands:")
    print('   python cli.py add "<place> <YYYY-MM-DD> <nights>"   Add a stop')
    print("   python cli.py list                                 Show the trip")


if __name__ == "__main__":
    # sys.argv[0] is the script name; the real arguments start at [1:].
    main(sys.argv[1:])
