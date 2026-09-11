"""
edit_demo.py  —  the EDIT tool (and its fallback)
==============================================================
EDIT changes a SMALL PART of a file by finding a piece of text
and replacing it. The catch: the text you point to must be
UNIQUE. If it appears more than once, Edit can't tell which one
you mean — then you fall back to READ + WRITE.

This works on a real throwaway file (scratch_edit.txt). It never
touches the sample_repo. Safe to run again and again.

Run it:   python edit_demo.py
==============================================================
"""

import os

HERE = os.path.dirname(__file__)
SCRATCH = os.path.join(HERE, "scratch_edit.txt")


def show(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def read_file():
    with open(SCRATCH, encoding="utf-8") as f:
        return f.read()


def print_file(label):
    print(f"\n{label}")
    print("  " + "-" * 34)
    for line in read_file().splitlines():
        print("  | " + line)
    print("  " + "-" * 34)


def edit(old_text, new_text):
    """
    Try to change `old_text` into `new_text`.
    RULE: only works if `old_text` appears EXACTLY ONCE.
    Returns True if it edited, False if the text wasn't unique.
    """
    content = read_file()
    count = content.count(old_text)
    if count == 1:
        content = content.replace(old_text, new_text)
        with open(SCRATCH, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False   # not unique (or not found) -> Edit can't safely do it


def main():
    # Start from a known scratch file each run (so it's repeatable).
    starting = (
        "name: DocDesk\n"
        "status: active\n"
        "owner: team-a\n"
        "status: active\n"      # NOTE: 'status: active' appears TWICE on purpose
    )
    with open(SCRATCH, "w", encoding="utf-8") as f:
        f.write(starting)

    show("TOOL: Edit  —  change a small part of a file")

    print("\nWHAT THIS TOOL DOES:")
    print("  Edit finds a piece of text in a file and replaces it —")
    print("  but ONLY if that text is UNIQUE (appears exactly once).")

    print_file("STARTING FILE (scratch_edit.txt):")

    # ---- CASE 1: unique text -> Edit works ----
    show("CASE 1: the text is UNIQUE  ->  Edit works")
    print("\nWHAT I'M ASKING IT:")
    print("  \"Change 'owner: team-a' to 'owner: team-b'\"")
    print("  ('owner: team-a' appears exactly once, so Edit is safe.)")

    ok = edit("owner: team-a", "owner: team-b")
    print("\nRESULT:")
    print("  Edit succeeded ✔" if ok else "  Edit could not run")
    print_file("FILE AFTER EDIT:")

    # ---- CASE 2: non-unique text -> Edit fails -> fall back to Read+Write ----
    show("CASE 2: the text is NOT unique  ->  use Read + Write")
    print("\nWHAT I'M ASKING IT:")
    print("  \"Change 'status: active' to 'status: paused'\"")
    print("  BUT 'status: active' appears TWICE — Edit can't tell which one!")

    ok = edit("status: active", "status: paused")
    print("\nRESULT of trying Edit:")
    if not ok:
        print("  Edit REFUSED ✗  — the text isn't unique.")
        print("\n  FALLBACK: Read the whole file, change it, Write it back.")
        # READ everything, change everything, WRITE it back.
        content = read_file()
        content = content.replace("status: active", "status: paused")
        with open(SCRATCH, "w", encoding="utf-8") as f:
            f.write(content)
        print("  Done using Read + Write ✔")
    print_file("FILE AFTER FALLBACK:")

    print("\nWHEN TO USE EDIT vs READ+WRITE:")
    print("  Edit       -> small change, and the target text is UNIQUE.")
    print("  Read+Write -> the target text is NOT unique (or you're")
    print("                changing lots of the file). Read it all,")
    print("                change it, write it back.")
    print()
    print("Tip: open scratch_edit.txt to see the final file.")
    print()


if __name__ == "__main__":
    main()
