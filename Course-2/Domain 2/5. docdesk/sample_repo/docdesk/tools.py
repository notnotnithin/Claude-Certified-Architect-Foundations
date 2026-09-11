"""Tool wrappers around the store."""
from docdesk.store import search_documents, read_document

def tool_search(docs_dir, query):
    return search_documents(docs_dir, query)

def tool_load(docs_dir, name):
    return read_document(docs_dir, name)
