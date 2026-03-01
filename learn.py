#!/usr/bin/env python3
"""
Learning Tracker - Track courses, certifications, skills
"""
import json
import sys
from pathlib import Path
from datetime import datetime

DATA_FILE = Path.home() / ".learning.json"

def load():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {"courses": [], "skills": [], "certifications": []}

def save(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))

def add_course(name, platform="", progress=0):
    data = load()
    data["courses"].append({
        "name": name,
        "platform": platform,
        "progress": progress,
        "started": datetime.now().isoformat(),
        "status": "in_progress"
    })
    save(data)
    return f"Added course: {name}"

def add_skill(name, level="beginner"):
    data = load()
    data["skills"].append({
        "name": name,
        "level": level,
        "added": datetime.now().isoformat()
    })
    save(data)
    return f"Added skill: {name}"

def add_cert(name, provider="", date=""):
    data = load()
    data["certifications"].append({
        "name": name,
        "provider": provider,
        "date": date,
        "earned": datetime.now().isoformat() if not date else date
    })
    save(data)
    return f"Added cert: {name}"

def list_all():
    data = load()
    
    lines = ["\n📚 Learning Tracker\n"]
    
    if data["courses"]:
        lines.append("COURSES:")
        for c in data["courses"]:
            p = c.get("progress", 0)
            lines.append(f"  - {c['name']} ({c['platform']}) - {p}%")
    
    if data["skills"]:
        lines.append("\nSKILLS:")
        for s in data["skills"]:
            lines.append(f"  - {s['name']} ({s['level']})")
    
    if data["certifications"]:
        lines.append("\nCERTIFICATIONS:")
        for c in data["certifications"]:
            lines.append(f"  - {c['name']} ({c['provider']})")
    
    return "\n".join(lines)

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    
    if cmd == "course":
        name = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Untitled"
        print(add_course(name))
    
    elif cmd == "skill":
        name = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Untitled"
        print(add_skill(name))
    
    elif cmd == "cert":
        name = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Untitled"
        print(add_cert(name))
    
    elif cmd == "list":
        print(list_all())
    
    else:
        print("Usage:")
        print("  learn course <name>")
        print("  learn skill <name>")
        print("  learn cert <name>")
        print("  learn list")


if __name__ == "__main__":
    main()
