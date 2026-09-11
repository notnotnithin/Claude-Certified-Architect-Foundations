"""
write_demo.py  —  the WRITE tool
==============================================================
WRITE creates a whole file (or replaces one completely) with
new content. Here we WRITE a real throwaway file called
scratch.txt so you can SEE a file appear.

It only ever touches scratch.txt — the sample_repo is never
changed. Safe to run again and again.

Run it:   python write_demo.py
==============================================================
"""

import os

HERE = os.path.dirname(__file__)
SCRATCH = os.path.join(HERE, "scratch.txt")


def show(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main():
    show("TOOL: Write  —  create (or replace) a whole file")

    print("\nWHAT THIS TOOL DOES:")
    print("  Write puts new content into a file. If the file doesn't")
    print("  exist, it's created. If it does exist, it's replaced.")

    new_content = (
        "Shopping list\n"
        "- milk\n"
        "- bread\n"
        "- eggs\n"
    )

    print("\nWHAT I'M ASKING IT:")
    print("  \"Create a file scratch.txt with a shopping list inside\"")

    # WRITE the whole file.
    with open(SCRATCH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("\nRESULT:")
    print(f"  Wrote the file: {os.path.basename(SCRATCH)}")
    print("  Its contents are now:")
    print("  " + "-" * 30)
    for line in new_content.splitlines():
        print("  | " + line)
    print("  " + "-" * 30)

    print("\nWHEN TO USE WRITE:")
    print("  Use Write to CREATE a new file, or to REPLACE a file's whole")
    print("  content. (To change just a small PART of a file, use Edit.)")
    print()
    print("Tip: open scratch.txt in your folder — you'll see the real file.")
    print()


if __name__ == "__main__":
    main()
