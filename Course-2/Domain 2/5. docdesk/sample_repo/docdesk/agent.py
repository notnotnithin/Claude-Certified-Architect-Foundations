"""The DocDesk agent entry point."""
from docdesk.tools import tool_search, tool_load

def run(docs_dir, question):
    names = tool_search(docs_dir, question)
    if not names:
        return "No matching documents."
    return tool_load(docs_dir, names[0])
