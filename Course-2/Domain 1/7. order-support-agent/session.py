"""
session.py
-----------
THE HEART OF DEMO 7: making a conversation PERSISTENT so you can stop now and
continue later — and choosing the RIGHT way to continue.

The Claude Agent SDK / CLI gives you:
  - --resume <session-name>  : continue a specific earlier conversation.
  - fork_session             : branch a saved conversation into an independent
                               copy, so you can explore a different path without
                               touching the original.

We model those ideas in plain Python by saving each session's message history
to a small JSON file under ./sessions/. That makes the concepts concrete:

  save_session(name, messages)      -> write history to sessions/<name>.json
  resume_session(name)              -> read that history back (the --resume idea)
  fork_session(name, new_name)      -> copy a session to a new name (independent)
  start_fresh_with_summary(summary) -> begin a NEW history seeded only with a
                                       short summary (no stale tool results)

WHEN TO USE WHICH (Task 1.7)
----------------------------
  - RESUME when the earlier context is mostly still valid.
  - START FRESH WITH A SUMMARY when the old tool results are STALE (the world
    changed). A clean summary is more reliable than replaying outdated results.
  - FORK when you want to try a different direction from a shared baseline
    without losing or altering the original session.
"""

import os
import json

SESSIONS_DIR = "sessions"


def _path(name: str) -> str:
    os.makedirs(SESSIONS_DIR, exist_ok=True)
    return os.path.join(SESSIONS_DIR, f"{name}.json")


def session_exists(name: str) -> bool:
    return os.path.exists(_path(name))


def save_session(name: str, messages: list) -> None:
    """Persist a session's message history to disk (so it survives restarts)."""
    with open(_path(name), "w", encoding="utf-8") as f:
        json.dump({"name": name, "messages": messages}, f, indent=2)
    print(f"[session] saved '{name}' ({len(messages)} messages) "
          f"-> {_path(name)}")


def resume_session(name: str) -> list:
    """
    Load a saved session's history back (models `--resume <name>`).
    Returns the messages list, or an empty list if the session is new.
    """
    if not session_exists(name):
        print(f"[session] no saved session '{name}' — starting a new one.")
        return []
    with open(_path(name), "r", encoding="utf-8") as f:
        data = json.load(f)
    messages = data.get("messages", [])
    print(f"[session] resumed '{name}' ({len(messages)} messages restored).")
    return messages


def fork_session(name: str, new_name: str) -> list:
    """
    Copy an existing session into a NEW, independent session (models
    `fork_session`). Changes to the fork do NOT affect the original.
    Returns the forked messages (also saved under new_name).
    """
    messages = resume_session(name)
    save_session(new_name, messages)
    print(f"[session] forked '{name}' -> '{new_name}' (independent branch).")
    return messages


def start_fresh_with_summary(summary: str) -> list:
    """
    Begin a NEW history seeded with ONLY a short summary — not the old, possibly
    stale, tool results. This is the reliable choice when the world has changed.
    """
    print("[session] starting FRESH with an injected summary (no stale results).")
    return [{
        "role": "user",
        "content": (
            "Here is a summary of the earlier conversation to continue from "
            f"(treat it as the current truth):\n{summary}"
        ),
    }]


def inform_of_change(messages: list, change_note: str) -> list:
    """
    Add a note to a RESUMED session telling the agent what changed since last
    time, so it re-checks the affected facts instead of trusting stale results.
    """
    messages.append({
        "role": "user",
        "content": f"NOTE — something changed since we last spoke: {change_note} "
                   "Please take this into account.",
    })
    print(f"[session] informed the resumed session of a change: {change_note}")
    return messages
