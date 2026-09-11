"""
extract_structured.py   (the RIGHT way)
==================================================================
Part 3 demo - Task 4.3: guaranteed structured output with tool_use

This is the core of Domain 4. Instead of asking for JSON as text and hoping it
parses, we give Claude a TOOL whose input is a strict JSON schema. When Claude
"calls" the tool, the data it fills in is GUARANTEED to match that schema. No
preambles, no code fences, no syntax errors - just clean structured data.

WHAT THIS SHOWS
---------------
1. Defining an extraction tool from our schema (schemas/receipt_schema.json).
2. Getting back schema-shaped data with zero JSON-parsing risk.
3. All THREE tool_choice modes and what each means:
     - "auto"  : Claude decides whether to use the tool (it might just chat).
     - "any"   : Claude MUST use some tool, but can pick which.
     - forced  : Claude MUST use the specific tool we name.
   For reliable extraction we use "any" or forced - never leave it to chance.

HOW TO RUN (from the project root, in cmd):

    python extract_structured.py
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from billbox._shared import extract_with_tool, load_receipt

# Load our JSON schema from disk and wrap it as a tool definition. The tool's
# "input_schema" IS the schema - that is what Claude's output must match.
ROOT = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(ROOT, "schemas", "receipt_schema.json"), encoding="utf-8") as f:
    RECEIPT_SCHEMA = json.load(f)

EXTRACT_TOOL = {
    "name": "save_receipt",
    "description": "Save the structured data extracted from a receipt.",
    "input_schema": RECEIPT_SCHEMA,
}

# The prompt still carries format-normalisation rules. Strict schemas guarantee
# the SHAPE; the prompt guides the CONTENT (e.g. how to normalise dates).
SYSTEM = """You extract data from a shop receipt and save it with the save_receipt tool.

Normalisation rules:
- date must be YYYY-MM-DD.
- total must be a plain number.
- gst_number: use the real GST/GSTIN if present, otherwise null. Never invent one.
- category: grocery, restaurant, utility, or other. If 'other', put a short
  description in category_detail; otherwise category_detail is null."""


def show(name, data, stop_reason):
    print(f"\n--- {name} ---")
    if data is None:
        print(f"(no tool was used; stop_reason={stop_reason})")
        return
    # data is already clean Python - no json.loads, no cleanup needed.
    print(f"  merchant : {data.get('merchant')}")
    print(f"  date     : {data.get('date')}")
    print(f"  total    : {data.get('total')}")
    print(f"  gst      : {data.get('gst_number')}")
    print(f"  category : {data.get('category')}", end="")
    if data.get("category_detail"):
        print(f"  ({data.get('category_detail')})")
    else:
        print()


def main():
    print("\n" + "=" * 64)
    print("  STRUCTURED OUTPUT via tool_use  (guaranteed schema-compliant)")
    print("=" * 64)

    # --- Part A: forced tool_choice (the most reliable for extraction) ---
    print("\n[A] tool_choice = forced (must call save_receipt)")
    print("    Best for extraction: the tool ALWAYS runs, output always fits.")
    forced = {"type": "tool", "name": "save_receipt"}
    for name in ["grocery_receipt.txt", "restaurant_bill.txt", "handwritten_style.txt"]:
        data, stop = extract_with_tool(SYSTEM, load_receipt(name), EXTRACT_TOOL, forced)
        show(name, data, stop)

    # --- Part B: tool_choice "any" (must use a tool, can pick which) ---
    print("\n" + "-" * 64)
    print("[B] tool_choice = any (must use SOME tool)")
    print("    With one tool, 'any' also guarantees structured output.")
    any_choice = {"type": "any"}
    data, stop = extract_with_tool(SYSTEM, load_receipt("utility_bill.txt"), EXTRACT_TOOL, any_choice)
    show("utility_bill.txt", data, stop)

    # --- Part C: tool_choice "auto" (Claude may choose NOT to use the tool) ---
    print("\n" + "-" * 64)
    print("[C] tool_choice = auto (Claude decides)")
    print("    Claude MAY just reply in text instead of using the tool -")
    print("    which is exactly why 'auto' is risky for guaranteed extraction.")
    auto_choice = {"type": "auto"}
    data, stop = extract_with_tool(SYSTEM, load_receipt("grocery_receipt.txt"), EXTRACT_TOOL, auto_choice)
    show("grocery_receipt.txt (auto)", data, stop)

    print("\n" + "-" * 64)
    print("""  With forced or 'any', every receipt came back as clean structured
  data - no JSON parsing, no broken output possible. That is the
  reliability tool_use buys you.

  One honest caveat: a strict schema removes SYNTAX errors, but not
  SEMANTIC ones. The shape is always valid; whether 'total' is the
  RIGHT number is a separate problem - that's what Part 4 tackles.""")


if __name__ == "__main__":
    main()
