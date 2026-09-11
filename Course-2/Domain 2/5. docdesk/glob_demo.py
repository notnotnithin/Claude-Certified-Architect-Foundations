"""
glob_demo.py  —  the GLOB tool
==============================================================
GLOB finds FILES BY THEIR NAME (or file type), no matter where
they sit in the folders. It does NOT look inside the files.

Run it:   python glob_demo.py
==============================================================
"""

import os
import glob

# The little codebase we explore.
REPO = os.path.join(os.path.dirname(__file__), "sample_repo")


def show(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main():
    show("TOOL: Glob  —  find files by their NAME")

    print("\nWHAT THIS TOOL DOES:")
    print("  Glob finds files whose NAME matches a pattern.")
    print("  It looks at file names only — never inside the files.")

    # ---- Example 1: find all the test files by name ----
    print("\nWHAT I'M ASKING IT:")
    print("  \"Find all the test files\"  (pattern: tests/test_*.py)")

    matches = glob.glob(os.path.join(REPO, "tests", "test_*.py"))
    print("\nRESULT:")
    for path in sorted(matches):
        print("  ", os.path.relpath(path, REPO))

    # ---- Example 2: find every Python file, anywhere ----
    print("\nWHAT I'M ASKING IT:")
    print("  \"Find every Python file, in any folder\"  (pattern: **/*.py)")

    all_py = glob.glob(os.path.join(REPO, "**", "*.py"), recursive=True)
    print("\nRESULT:")
    for path in sorted(all_py):
        print("  ", os.path.relpath(path, REPO))

    print("\nWHEN TO USE GLOB:")
    print("  Use Glob when you know the file's NAME or TYPE,")
    print("  but not what's inside it. Example: 'find all test files',")
    print("  'find all .md files'.  (To search INSIDE files, use Grep.)")
    print()


if __name__ == "__main__":
    main()
