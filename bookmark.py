#!/usr/bin/env python3
"""
Bookmark Manager - Save and search bookmarks
"""
import json
import sys
from pathlib import Path
from datetime import datetime

BOOKMARKS_FILE = Path.home() / ".bookmarks.json"

def load():
    if BOOKMARKS_FILE.exists():
        return json.loads(BOOKMARKS_FILE.read_text())
    return {}

def save(bookmarks):
    BOOKMARKS_FILE.write_text(json.dumps(bookmarks, indent=2))

def add(url, title="", tags=None):
    bookmarks = load()
    bookmarks[url] = {
        "title": title or url,
        "tags": tags or [],
        "added": datetime.now().isoformat()
    }
    save(bookmarks)
    return f"Added: {title or url}"

def list_bookmarks(tag=None):
    bookmarks = load()
    if tag:
        bookmarks = {u: b for u, b in bookmarks.items() if tag in b.get("tags", [])}
    
    if not bookmarks:
        return "No bookmarks."
    
    lines = [f"\nBookmarks ({len(bookmarks)}):"]
    for url, data in bookmarks.items():
        title = data.get("title", url)
        tags = ", ".join(data.get("tags", [])) or "-"
        lines.append(f"  - {title} [{tags}]")
    return "\n".join(lines)

def search(query):
    bookmarks = load()
    query = query.lower()
    results = []
    
    for url, data in bookmarks.items():
        if query in url.lower() or query in data.get("title", "").lower():
            results.append((data.get("title", url), url))
    
    if not results:
        return "No matches."
    
    return "\n".join(f"{t}: {u}" for t, u in results)

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    
    if cmd == "add":
        url = sys.argv[2] if len(sys.argv) > 2 else ""
        title = sys.argv[3] if len(sys.argv) > 3 else ""
        tags = sys.argv[4:] if len(sys.argv) > 4 else []
        if url:
            print(add(url, title, tags))
        else:
            print("Usage: bookmark add <url> [title] [tags...]")
    
    elif cmd == "list":
        tag = sys.argv[2] if len(sys.argv) > 2 else None
        print(list_bookmarks(tag))
    
    elif cmd == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        print(search(query))
    
    else:
        print("Usage: bookmark add <url> [title] [tags...]")
        print("       bookmark list [tag]")
        print("       bookmark search <query>")

if __name__ == "__main__":
    main()
