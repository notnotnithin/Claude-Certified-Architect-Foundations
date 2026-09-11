"""
reader.py
---------
Loads a receipt's text from a file on disk.

This is the only part of BillBox that touches the file system. In Part 0 there is
no AI yet - we simply read the raw text so you can see what BillBox will later
turn into clean, structured data.
"""

import os


def load_receipt(path):
    """
    Read a receipt file and return its text.

    We use encoding="utf-8" because receipts contain the Rupee sign and other
    non-ASCII characters, and the default Windows encoding can choke on them.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"No receipt found at: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def list_receipts(folder):
    """
    Return the names of all .txt receipts in a folder, sorted.

    Later parts loop over these to extract many receipts at once.
    """
    if not os.path.isdir(folder):
        return []
    names = [n for n in os.listdir(folder) if n.endswith(".txt")]
    return sorted(names)
