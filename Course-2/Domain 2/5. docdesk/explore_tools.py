"""
explore_tools.py
-----------------
A RUNNABLE demonstrator for Task 2.5 — Claude Code's BUILT-IN TOOLS:
Grep, Glob, Read, Write, Edit.

These tools live INSIDE Claude Code, not in the Anthropic API — so we can't call
"Claude Code's Grep" from Python. But each tool is really a familiar operation:

    Grep  = search file CONTENTS for a pattern
    Glob  = find FILE PATHS matching a name pattern
    Read  = read a whole file
    Write = write a whole file
    Edit  = change a small part of a file by matching UNIQUE text

This script performs those same operations on the sample_repo/ codebase, so you
can SEE what each tool does and — most importantly — learn WHEN to choose which.
That "which tool when" judgment is exactly what Task 2.5 tests.

Run it:
    python explore_tools.py
"""

import os
import re
import glob

REPO = os.path.join(os.path.dirname(__file__), "sample_repo")


def line(title):
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


# --------------------------------------------------------------------------
# GREP  — search file CONTENTS for a pattern.
# Use when: you want to find WHERE something appears (a function's callers,
# an error message, an import). You know WHAT text, not which file.
# --------------------------------------------------------------------------
def grep(pattern, root=REPO):
    print(f"[Grep] searching file contents for: {pattern!r}")
    hits = []
    for path in glob.glob(os.path.join(root, "**", "*.py"), recursive=True):
        with open(path, encoding="utf-8") as f:
            for n, text in enumerate(f, 1):
                if re.search(pattern, text):
                    rel = os.path.relpath(path, root)
                    hits.append((rel, n, text.strip()))
    for rel, n, text in hits:
        print(f"   {rel}:{n}: {text}")
    if not hits:
        print("   (no matches)")
    return hits


# --------------------------------------------------------------------------
# GLOB  — find FILE PATHS matching a name pattern.
# Use when: you want files BY NAME/TYPE, regardless of contents or location
# (e.g. all test files, all .md files).
# --------------------------------------------------------------------------
def glob_find(pattern, root=REPO):
    print(f"[Glob] finding files matching: {pattern!r}")
    matches = [os.path.relpath(p, root)
               for p in glob.glob(os.path.join(root, pattern), recursive=True)]
    for m in sorted(matches):
        print(f"   {m}")
    if not matches:
        print("   (no files matched)")
    return matches


# --------------------------------------------------------------------------
# READ  — read a whole file.
# Use when: you've found the right file and want to understand it fully.
# --------------------------------------------------------------------------
def read(rel_path):
    print(f"[Read] {rel_path}")
    with open(os.path.join(REPO, rel_path), encoding="utf-8") as f:
        text = f.read()
    for n, ln in enumerate(text.splitlines(), 1):
        print(f"   {n:>2}: {ln}")
    return text


def main():
    line("1) GLOB — find files by NAME pattern (all test files)")
    print("When to use Glob: you want files by name/type, not by content.")
    glob_find("tests/test_*.py")
    print("\nAlso: every Python file in the repo:")
    glob_find("**/*.py")

    line("2) GREP — find WHERE something appears in file CONTENTS")
    print("Task: find everywhere 'search_documents' is used (its callers).")
    grep(r"search_documents")
    print("\nTask: locate a specific string (like an error message).")
    grep(r"No matching documents")

    line("3) READ — open the RIGHT file once Grep/Glob found it")
    print("Grep showed search_documents is DEFINED in docdesk/store.py — read it:")
    read(os.path.join("docdesk", "store.py"))

    line("4) INCREMENTAL EXPLORATION (the recommended workflow)")
    print("Don't read every file up front. Instead:")
    print("  a) GREP for an entry point...")
    grep(r"def run\(")
    print("  b) ...then READ that file and FOLLOW its imports.")
    read(os.path.join("docdesk", "agent.py"))
    print("Notice agent.py imports from docdesk.tools -> which imports from")
    print("docdesk.store. You trace the flow by following imports, guided by")
    print("Grep + Read — NOT by reading all files blindly.")

    line("5) EDIT vs READ+WRITE (the fallback rule)")
    print("EDIT changes a small part of a file by matching UNIQUE text.")
    print("If the anchor text is NOT unique, Edit can't tell which one to change")
    print("-> fall back to READ the whole file, modify, then WRITE it back.\n")
    # Show a non-unique anchor: 'import os' appears multiple times in store.py
    hits = grep(r"import os", os.path.join(REPO, "docdesk"))
    if len(hits) > 1:
        print(f"\n-> 'import os' appears {len(hits)} times in store.py.")
        print("   Edit on 'import os' would be AMBIGUOUS (which one?).")
        print("   So here you'd use READ + WRITE instead of Edit.")
    else:
        print("\n-> anchor was unique; Edit would be fine here.")

    line("Summary — which tool when")
    print("  Glob  -> find files by NAME/TYPE          (**/*.test.tsx)")
    print("  Grep  -> find WHERE text appears           (callers, errors)")
    print("  Read  -> understand a file you've located")
    print("  Edit  -> small change via UNIQUE anchor text")
    print("  Read+Write -> fallback when the anchor isn't unique")
    print("  Workflow -> Grep to find entry points, Read to follow imports")


if __name__ == "__main__":
    main()
