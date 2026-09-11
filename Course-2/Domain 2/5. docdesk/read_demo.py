"""
read_demo.py  —  the READ tool
==============================================================
READ opens ONE file and shows its full contents. You use it
after Grep or Glob has pointed you to the right file.

Run it:   python read_demo.py
==============================================================
"""

import os

REPO = os.path.join(os.path.dirname(__file__), "sample_repo")


def show(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def read(rel_path):
    """Open ONE file and print it with line numbers."""
    full = os.path.join(REPO, rel_path)
    with open(full, encoding="utf-8") as f:
        text = f.read()
    for line_no, line in enumerate(text.splitlines(), 1):
        print(f"   {line_no:>2}:  {line}")


def main():
    show("TOOL: Read  —  open ONE file and see all of it")

    print("\nWHAT THIS TOOL DOES:")
    print("  Read opens a single file and shows its full contents.")
    print("  You use it once Grep/Glob has told you which file you need.")

    print("\nWHAT I'M ASKING IT:")
    print("  \"Open and show me the file docdesk/store.py\"")

    print("\nRESULT:")
    read(os.path.join("docdesk", "store.py"))

    print("\nWHEN TO USE READ:")
    print("  Use Read when you've found the right file and want to")
    print("  understand it fully. Grep/Glob find the file; Read opens it.")
    print()


if __name__ == "__main__":
    main()
