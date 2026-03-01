#!/usr/bin/env python3
"""
Quick Note - Fast note capture
Usage: note <text>
"""
import sys
from pathlib import Path
from datetime import datetime

NOTES = Path.home() / ".quick_notes.md"

def add(text):
    time = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"- [{time}] {text}\n"
    
    # Prepend to file
    if NOTES.exists():
        old = NOTES.read_text()
        NOTES.write_text(entry + old)
    else:
        NOTES.write_text(entry)
    
    return "Saved."

def list_notes():
    if not NOTES.exists():
        return "No notes yet."
    return NOTES.read_text()[:1000]

def main():
    if len(sys.argv) < 2:
        print(list_notes())
    else:
        text = " ".join(sys.argv[1:])
        print(add(text))

if __name__ == "__main__":
    main()
