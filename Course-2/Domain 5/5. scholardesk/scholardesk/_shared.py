"""
_shared.py
----------
A tiny helper the ScholarDesk scripts use, so each script stays focused on the
ONE idea it teaches rather than on API plumbing.

Every script that calls Claude must load the .env itself (see load_dotenv below),
because if we relied on another module to do it, this file could run first and
find no API key.
"""

import os
import sys

from dotenv import load_dotenv
import anthropic

load_dotenv()

MODEL = "claude-sonnet-4-6"


def get_client():
    """Build the Anthropic client, or explain clearly if the key is missing."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\nNo API key found.")
        print("Copy .env.example to .env and paste your key:")
        print("    copy .env.example .env")
        print("Then open .env and set ANTHROPIC_API_KEY=sk-ant-...\n")
        sys.exit(1)
    return anthropic.Anthropic()


def ask_claude(system_prompt, messages, max_tokens=800):
    """
    Send a request to Claude and return the plain text of the reply.

    `messages` is the full conversation list, so the SAME helper works for a
    single question and for a long multi-turn research session - which matters in
    Domain 5, where managing a long session is a core theme.
    """
    client = get_client()
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=messages,
    )
    return "".join(b.text for b in response.content if b.type == "text").strip()


def source_path(filename):
    """Return the path to a file in the sources/ folder at the project root."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, "sources", filename)


def list_sources():
    """Return the names of all source documents, sorted."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    folder = os.path.join(root, "sources")
    if not os.path.isdir(folder):
        return []
    return sorted(n for n in os.listdir(folder) if n.endswith(".txt"))
