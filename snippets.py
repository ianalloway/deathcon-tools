#!/usr/bin/env python3
"""
Code Snippet Manager - Store and search code snippets
"""
import json
import sys
from pathlib import Path
from datetime import datetime

SNIPPETS_FILE = Path.home() / ".snippets.json"

def load_snippets():
    if SNIPPETS_FILE.exists():
        return json.loads(SNIPPETS_FILE.read_text())
    return {}

def save_snippets(snippets):
    SNIPPETS_FILE.write_text(json.dumps(snippets, indent=2))

def add(name, code, tags=None, language="python"):
    snippets = load_snippets()
    snippets[name] = {
        "code": code,
        "tags": tags or [],
        "language": language,
        "created": datetime.now().isoformat(),
    }
    save_snippets(snippets)
    return f"Added: {name}"

def search(query):
    snippets = load_snippets()
    results = []
    query = query.lower()
    
    for name, data in snippets.items():
        if query in name.lower():
            results.append((name, data, "name"))
        elif any(query in tag.lower() for tag in data.get("tags", [])):
            results.append((name, data, "tag"))
        elif query in data.get("code", "").lower():
            results.append((name, data, "code"))
    
    return results

def list_all():
    snippets = load_snippets()
    if not snippets:
        return "No snippets."
    
    lines = ["\n📦 Snippets:"]
    for name, data in snippets.items():
        lang = data.get("language", "?")
        tags = ", ".join(data.get("tags", [])) or "-"
        lines.append(f"  {name} [{lang}] - {tags}")
    return "\n".join(lines)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    
    if cmd == "add":
        name = sys.argv[2] if len(sys.argv) > 2 else "untitled"
        code = sys.argv[3] if len(sys.argv) > 3 else ""
        tags = sys.argv[4:] if len(sys.argv) > 4 else []
        print(add(name, code, tags))
    
    elif cmd == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        results = search(query)
        if not results:
            print("No matches.")
        else:
            for name, data, match_type in results:
                print(f"\n{name} [{match_type}]")
                print(data["code"][:200])
    
    elif cmd == "list":
        print(list_all())
    
    else:
        print("Usage: snippets.py add <name> <code> [tags...]")
        print("       snippets.py search <query>")
        print("       snippets.py list")


if __name__ == "__main__":
    main()
