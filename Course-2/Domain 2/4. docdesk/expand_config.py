"""
expand_config.py
-----------------
RUNNABLE DEMO (Part B): show ENVIRONMENT-VARIABLE EXPANSION in .mcp.json.

The whole point of writing ${GITHUB_TOKEN} instead of a real token is that the
secret is injected from your environment ONLY at load time — so the .mcp.json
file itself stays safe to commit.

This script reads .mcp.json, finds every ${VAR} placeholder, and prints the
config with the values filled in from your environment. Run it with and without
the env vars set to SEE the difference.

    # nothing set yet -> placeholders stay unresolved (shown clearly)
    python expand_config.py

    # set values, then run again -> they get filled in
    #   Windows (PowerShell):
    #     $env:DOCDESK_DOCS_DIR="./documents"; $env:GITHUB_TOKEN="ghp_demo123"
    #   macOS / Linux / WSL:
    #     export DOCDESK_DOCS_DIR=./documents GITHUB_TOKEN=ghp_demo123
    python expand_config.py
"""

import os
import re
import json
from dotenv import load_dotenv

# Load a .env file (if present) into the environment BEFORE we expand.
# This is why you can put DOCDESK_DOCS_DIR / GITHUB_TOKEN in .env and just run
# `python expand_config.py` — no `set` commands needed.
load_dotenv()

PLACEHOLDER = re.compile(r"\$\{([^}]+)\}")   # matches ${SOMETHING}


def expand(value: str):
    """Replace every ${VAR} in a string with its environment value.
    Returns (expanded_string, list_of_missing_vars)."""
    missing = []

    def repl(match):
        var = match.group(1)
        val = os.environ.get(var)
        if val is None:
            missing.append(var)
            return match.group(0)          # leave ${VAR} as-is if not set
        return val

    return PLACEHOLDER.sub(repl, value), missing


def walk(obj, missing):
    """Recursively expand ${VAR} in all string values of the config.
    Comment keys (starting with '//') are skipped so example placeholders
    written inside comments don't count as real variables."""
    if isinstance(obj, dict):
        return {k: (v if k.startswith("//") else walk(v, missing))
                for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk(v, missing) for v in obj]
    if isinstance(obj, str):
        expanded, miss = expand(obj)
        missing.extend(miss)
        return expanded
    return obj


def main():
    with open(".mcp.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    print("=" * 66)
    print("BEFORE expansion (.mcp.json as committed — safe, no secrets):")
    print("=" * 66)
    # show just the env blocks so the placeholders are obvious
    for name, server in config.get("mcpServers", {}).items():
        if name.startswith("//"):
            continue
        print(f"  {name}.env = {server.get('env', {})}")

    missing = []
    resolved = walk(config, missing)

    print("\n" + "=" * 66)
    print("AFTER expansion (what Claude Code actually uses at connect time):")
    print("=" * 66)
    for name, server in resolved.get("mcpServers", {}).items():
        if name.startswith("//"):
            continue
        print(f"  {name}.env = {server.get('env', {})}")

    if missing:
        unique = sorted(set(missing))
        print("\n[!] These variables are NOT set in your environment yet:")
        for v in unique:
            print(f"      - {v}")
        print("    Their ${...} placeholders stayed unresolved above.")
        print("    Set them (see the header of this file) and re-run to see")
        print("    the real values filled in.")
    else:
        print("\n[ok] All ${...} placeholders were resolved from your environment.")
    print("\nKey idea: the SECRET never lives in .mcp.json — only ${VAR} does.")


if __name__ == "__main__":
    main()
