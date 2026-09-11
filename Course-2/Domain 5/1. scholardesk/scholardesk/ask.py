"""
ask.py
------
ScholarDesk - Part 0 version.

ScholarDesk is a research assistant. You ask it a question, and it answers using
source documents. Over Domain 5 we make it RELIABLE: good at long research
sessions, honest about uncertainty, and careful to say which source each fact
came from.

In Part 0 it's deliberately simple: it answers from ONE source document at a time.
Combining MANY sources - and tracking which fact came from which - is the big theme
that arrives fully in Part 6. Starting with one source keeps the foundation clear.

HOW TO RUN (from the project root, in cmd):

    python scholardesk/ask.py list
    python scholardesk/ask.py ev_cost_brief.txt "How much does an electric scooter cost in Pune?"
"""

import sys
import os

# Allow running as "python scholardesk/ask.py" from the project root.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scholardesk._shared import ask_claude, source_path, list_sources

SYSTEM = """You are ScholarDesk, a careful research assistant. Answer the user's
question using ONLY the source document provided. If the source doesn't contain the
answer, say so plainly rather than guessing. Keep the answer short and factual."""


def cmd_list():
    """Show the source documents ScholarDesk can read."""
    names = list_sources()
    if not names:
        print("No sources found in the 'sources' folder.")
        return
    print("Sources available:")
    for name in names:
        print(f"   - {name}")
    print(f"\nTotal: {len(names)} sources")


def cmd_ask(source_name, question):
    """Answer a question from ONE source document."""
    try:
        with open(source_path(source_name), encoding="utf-8") as f:
            source_text = f.read()
    except FileNotFoundError:
        print(f"No source named {source_name!r}. Try:  python scholardesk/ask.py list")
        return

    system = SYSTEM + "\n\nSOURCE DOCUMENT:\n" + source_text
    print(f"\nQuestion: {question}")
    print(f"(from {source_name})")
    print("\nScholarDesk:", ask_claude(system, [{"role": "user", "content": question}]))


def print_help():
    print("ScholarDesk - a research assistant (Part 0)")
    print()
    print("Commands:")
    print("   python scholardesk/ask.py list")
    print('   python scholardesk/ask.py <source_file> "<your question>"')
    print()
    print("Example:")
    print('   python scholardesk/ask.py ev_cost_brief.txt "What is the running cost per km?"')


def main(argv):
    if not argv:
        print_help()
        return
    if argv[0] == "list":
        cmd_list()
    elif len(argv) >= 2:
        cmd_ask(argv[0], argv[1])
    else:
        print("Please give a source file AND a question, or use 'list'.")
        print_help()


if __name__ == "__main__":
    main(sys.argv[1:])
