#!/usr/bin/env python3
"""
Meeting Notes Generator - Creates structured meeting notes
"""
import sys
from datetime import datetime
from pathlib import Path

NOTES_DIR = Path.home() / "meetings"
NOTES_DIR.mkdir(exist_ok=True)

TEMPLATE = """# Meeting Notes - {date}

## Attendees
-

## Agenda
1. 

## Discussion

### Topic 1
- 

### Topic 2
- 

## Action Items
- [ ] 

## Next Steps
- 

## Links/References
-
"""

def create_note(title, date=None):
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    
    filename = NOTES_DIR / f"{date}_{title.replace(' ', '-')}.md"
    content = TEMPLATE.format(date=date, title=title)
    
    filename.write_text(content)
    return filename

def list_notes():
    files = sorted(NOTES_DIR.glob("*.md"), reverse=True)
    if not files:
        return "No meetings yet."
    
    lines = ["Meetings:"]
    for f in files[:10]:
        lines.append(f"  - {f.stem}")
    return "\n".join(lines)

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    
    if cmd == "new":
        title = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Untitled"
        file = create_note(title)
        print(f"Created: {file}")
    
    elif cmd == "list":
        print(list_notes())
    
    else:
        print("Usage: meeting new <title> | meeting list")


if __name__ == "__main__":
    main()
