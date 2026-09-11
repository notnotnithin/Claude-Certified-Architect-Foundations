"""Document store: load and search documents."""

def list_documents(docs_dir):
    import os
    return [f for f in os.listdir(docs_dir) if f.endswith(".md")]

def read_document(docs_dir, name):
    import os
    path = os.path.join(docs_dir, name)
    with open(path, encoding="utf-8") as f:
        return f.read()

def search_documents(docs_dir, query):
    hits = []
    for name in list_documents(docs_dir):
        text = read_document(docs_dir, name)
        if query.lower() in text.lower():
            hits.append(name)
    return hits
