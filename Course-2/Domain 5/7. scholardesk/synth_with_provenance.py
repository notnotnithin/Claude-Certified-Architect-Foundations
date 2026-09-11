"""
synth_with_provenance.py   (the RIGHT way)
==================================================================
Part 6 demo - Task 5.6: synthesis that keeps its sources

Same sources, same question. But now ScholarDesk returns a STRUCTURED answer where
every claim is tied to the source it came from - and where a conflict between sources
is flagged with BOTH values, their sources, AND their dates, instead of being
silently resolved.

WHAT THIS SHOWS
---------------
1. CLAIM-SOURCE MAPPINGS: each fact is paired with its source document, so
   attribution survives the synthesis instead of dissolving into a blend.

2. CONFLICT ANNOTATION: two sources disagree on Pune's charging-point count. Rather
   than pick one, ScholarDesk reports BOTH values with their sources.

3. TEMPORAL METADATA: each source has a publication date. The newer adoption report
   (2026-03-10, "~480") supersedes the older charging note (2026-02-05, "~350"). The
   dates turn a scary-looking "contradiction" into what it really is: an UPDATE.
   Without the dates you'd think the sources disagree; with them, you can see which
   value is current.

We get this as structured output using tool use (Domain 4's reliable method).

HOW TO RUN (from the project root, in cmd):

    python synth_with_provenance.py
"""

import os
import sys
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scholardesk._shared import get_client, MODEL, source_path, list_sources


def load_labelled_sources():
    """
    Load each source, pulling its publication date out of the header so the model
    can attribute claims AND reason about which source is newer.
    """
    blocks = []
    for name in list_sources():
        with open(source_path(name), encoding="utf-8") as f:
            text = f.read()
        # The date sits in the header as "(published YYYY-MM-DD)".
        m = re.search(r"published (\d{4}-\d{2}-\d{2})", text)
        date = m.group(1) if m else "unknown"
        blocks.append(f"[SOURCE: {name} | published: {date}]\n{text}")
    return "\n\n".join(blocks)


# A tool that forces provenance-preserving structure.
SYNTH_TOOL = {
    "name": "answer_with_sources",
    "description": "Answer the user while preserving which source each claim came from.",
    "input_schema": {
        "type": "object",
        "properties": {
            "claims": {
                "type": "array",
                "description": "Each fact in the answer, tied to its source document.",
                "items": {
                    "type": "object",
                    "properties": {
                        "statement": {"type": "string"},
                        "source": {"type": "string", "description": "The source filename."},
                    },
                    "required": ["statement", "source"],
                },
            },
            "conflicts": {
                "type": "array",
                "description": "Any place the sources disagree. Empty if none.",
                "items": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string"},
                        "values": {
                            "type": "array",
                            "description": "Each conflicting value with its source and date.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "value": {"type": "string"},
                                    "source": {"type": "string"},
                                    "source_date": {"type": "string"},
                                },
                                "required": ["value", "source", "source_date"],
                            },
                        },
                        "resolution": {
                            "type": "string",
                            "description": "Which value is current and why (use the dates).",
                        },
                    },
                    "required": ["topic", "values", "resolution"],
                },
            },
        },
        "required": ["claims", "conflicts"],
    },
}

SYSTEM = """You are ScholarDesk, a research assistant. Answer using the labelled
sources. Preserve provenance: tie every claim to the source it came from. If two
sources give different values for the same thing, do NOT pick one silently - record
it as a conflict listing both values with their sources and publication dates, and in
'resolution' say which is current (the more recent publication date wins) and why.
Use the answer_with_sources tool."""

QUESTION = "How many public charging points does Pune have, and how is EV adoption going?"


def main():
    client = get_client()
    system = SYSTEM + "\n\nSOURCES:\n" + load_labelled_sources()

    print("\n" + "=" * 64)
    print("  WITH PROVENANCE  (claims tied to sources - the right way)")
    print("=" * 64)
    print(f"\nUser: {QUESTION}\n")

    response = client.messages.create(
        model=MODEL, max_tokens=1000, system=system,
        tools=[SYNTH_TOOL], tool_choice={"type": "tool", "name": "answer_with_sources"},
        messages=[{"role": "user", "content": QUESTION}],
    )
    data = next((b.input for b in response.content if b.type == "tool_use"), {})

    print("CLAIMS (each tied to its source):")
    for c in data.get("claims", []):
        print(f"  - {c.get('statement')}")
        print(f"      source: {c.get('source')}")

    conflicts = data.get("conflicts", [])
    if conflicts:
        print("\nCONFLICTS (flagged, not hidden):")
        for con in conflicts:
            print(f"  Topic: {con.get('topic')}")
            for v in con.get("values", []):
                print(f"    - {v.get('value')}  [{v.get('source')}, {v.get('source_date')}]")
            print(f"    Resolution: {con.get('resolution')}")
    else:
        print("\nCONFLICTS: none reported.")

    print("\n" + "-" * 64)
    print("""  Every claim now carries its source. And the charging-count conflict
  (480 vs 350) is reported with BOTH values, their sources, and their
  dates - then resolved by recency: the newer report (2026-03-10) wins,
  so ~480 is current.

  The dates are what turn a "contradiction" into an "update". Without
  them the two values look like a disagreement; with them, you can see
  one simply replaced the other.""")


if __name__ == "__main__":
    main()
