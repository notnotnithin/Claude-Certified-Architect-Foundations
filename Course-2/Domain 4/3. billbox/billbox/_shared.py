"""
_shared.py
----------
A tiny helper both demo scripts use, so the scripts themselves stay focused on
the ONE thing that matters in this part: the review criteria in the prompt.

Every script that calls Claude must load the .env itself (see load_dotenv below),
because if we relied on another module to do it, this file could run first and
find no API key.
"""

import os
import sys

from dotenv import load_dotenv
import anthropic

# Load the API key from .env in THIS file, so any script importing us is covered.
load_dotenv()

MODEL = "claude-sonnet-4-6"


def get_client():
    """
    Build the Anthropic client, or explain clearly if the key is missing.

    A friendly message here saves a beginner from a confusing crash.
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\nNo API key found.")
        print("Copy .env.example to .env and paste your key:")
        print("    copy .env.example .env")
        print("Then open .env and set ANTHROPIC_API_KEY=sk-ant-...\n")
        sys.exit(1)
    return anthropic.Anthropic()


def ask_claude(system_prompt, user_text, max_tokens=800):
    """
    Send one request to Claude and return the plain text of the reply.

    Kept deliberately tiny - the LESSON is the prompt we pass in, not this call.
    """
    client = get_client()
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_text}],
    )
    parts = [b.text for b in response.content if b.type == "text"]
    return "".join(parts).strip()


def load_receipt(name):
    """Load one receipt's text from the receipts/ folder at the project root."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(root, "receipts", name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
