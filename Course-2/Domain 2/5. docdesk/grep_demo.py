"""
grep_demo.py  —  the GREP tool
==============================================================
GREP searches INSIDE files for a word or phrase. It tells you
which file and which line the text appears on. Think of it as
"Ctrl+F across the whole project".

Run it:   python grep_demo.py
==============================================================
"""

import os
import re
import glob

REPO = os.path.join(os.path.dirname(__file__), "sample_repo")


def show(title):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def grep(pattern):
    """Search every .py file's CONTENTS for `pattern`. Print file:line: text."""
    found = []
    for path in glob.glob(os.path.join(REPO, "**", "*.py"), recursive=True):
        with open(path, encoding="utf-8") as f:
            for line_no, text in enumerate(f, 1):
                if re.search(pattern, text):
                    found.append((os.path.relpath(path, REPO), line_no, text.strip()))
    for rel, line_no, text in found:
        print(f"   {rel}:{line_no}:  {text}")
    if not found:
        print("   (no matches)")


def main():
    show("TOOL: Grep  —  find TEXT inside files")

    print("\nWHAT THIS TOOL DOES:")
    print("  Grep searches the CONTENTS of files for a word or phrase,")
    print("  and shows which file and line it is on.")

    # ---- Example 1: find where a function is used ----
    print("\nWHAT I'M ASKING IT:")
    print("  \"Find everywhere the word 'search_documents' appears\"")
    print("\nRESULT:")
    grep(r"search_documents")

    # ---- Example 2: find a specific message ----
    print("\nWHAT I'M ASKING IT:")
    print("  \"Find the line with the message: No matching documents\"")
    print("\nRESULT:")
    grep(r"No matching documents")

    print("\nWHEN TO USE GREP:")
    print("  Use Grep when you know the TEXT you're looking for but not")
    print("  which file it's in. Example: 'where is this function used?',")
    print("  'where does this error message come from?'")
    print("  (To find files by NAME instead, use Glob.)")
    print()


if __name__ == "__main__":
    main()
