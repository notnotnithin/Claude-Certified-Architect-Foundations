"""
cli.py
------
The BillBox command line - Part 0 version.

BillBox will eventually read a messy receipt and pull out clean, structured data
(merchant, date, items, total). But it has to walk before it can run. In Part 0
it only does two simple things, with NO AI at all:

    python cli.py list                     show which receipts we have
    python cli.py show grocery_receipt.txt print one receipt's raw text

Seeing the raw, messy text first is the whole point: from Part 1 onward you will
watch Claude turn this mess into structured data.

How the pieces fit together:
    receipts/           the messy receipt text files
    billbox/reader.py   loads a receipt from disk
    billbox/cli.py      the commands you type (this file)
"""

import sys
import os

# Allow running as "python billbox/cli.py" from the project root by making sure
# the project root (which contains the 'billbox' package) is importable.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from billbox.reader import load_receipt, list_receipts

# The receipts folder sits next to the 'billbox' package, at the project root.
# We build the path from this file's location so it works no matter which folder
# you run the command from.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECEIPTS_FOLDER = os.path.join(PROJECT_ROOT, "receipts")


def cmd_list():
    """Show every receipt file we have to work with."""
    names = list_receipts(RECEIPTS_FOLDER)
    if not names:
        print("No receipts found in the 'receipts' folder.")
        return
    print("Receipts available:")
    for name in names:
        print(f"   - {name}")
    print(f"\nTotal: {len(names)} receipts")


def cmd_show(name):
    """Print one receipt's raw text - the messy input BillBox starts from."""
    path = os.path.join(RECEIPTS_FOLDER, name)
    try:
        text = load_receipt(path)
    except FileNotFoundError as e:
        print(e)
        return

    print("=" * 44)
    print(f"  RAW TEXT: {name}")
    print("=" * 44)
    print(text)
    print("=" * 44)
    print("This is the messy input. From Part 1, Claude turns text")
    print("like this into clean, structured data.")


def print_help():
    print("BillBox - a receipt data extractor (Part 0)")
    print()
    print("Commands:")
    print("   python billbox/cli.py list            List all receipts")
    print("   python billbox/cli.py show <file>     Show one receipt's raw text")


def main(argv):
    if not argv:
        print_help()
        return

    command = argv[0]
    if command == "list":
        cmd_list()
    elif command == "show":
        if len(argv) < 2:
            print("Please name a receipt, e.g.  python cli.py show grocery_receipt.txt")
            return
        cmd_show(argv[1])
    else:
        print(f"Unknown command: {command!r}")
        print_help()


if __name__ == "__main__":
    main(sys.argv[1:])
