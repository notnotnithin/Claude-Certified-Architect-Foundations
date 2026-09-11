"""
retrieval.py
------------
ScholarDesk's source-retrieval helpers - the functions it uses to find and load
sources before answering.

These return STRUCTURED results (with an ok flag and error context) exactly as
Part 3 taught. This module exists partly so ScholarDesk has a realistic codebase to
EXPLORE in Part 4 - a few modules that call each other, the way a real project looks.
"""

import os


def _sources_dir():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, "sources")


def list_source_names():
    """Return all available source filenames, sorted."""
    folder = _sources_dir()
    if not os.path.isdir(folder):
        return []
    return sorted(n for n in os.listdir(folder) if n.endswith(".txt"))


def load_source(name):
    """
    Load one source by name.

    Returns a structured result: ok=True with the text, or ok=False with an
    error_type the assistant can act on (see Part 3).
    """
    path = os.path.join(_sources_dir(), name)
    if not os.path.exists(path):
        return {"ok": False, "error_type": "validation", "retryable": False,
                "attempted": f"load_source({name})",
                "message": f"No source named {name!r} exists."}
    with open(path, "r", encoding="utf-8") as f:
        return {"ok": True, "results": f.read()}


def search_sources(keyword):
    """
    Search every source for a keyword and return the ones that mention it.

    An empty list here is a VALID EMPTY RESULT - the search ran fine and found no
    match (not an error), exactly the distinction Part 3 made.
    """
    hits = []
    for name in list_source_names():
        loaded = load_source(name)
        if loaded.get("ok") and keyword.lower() in loaded["results"].lower():
            hits.append(name)
    return {"ok": True, "results": hits, "attempted": f"search_sources({keyword!r})"}
