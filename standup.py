#!/usr/bin/env python3
"""
Daily Standup Generator - Creates standup from activity
"""
import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path

PROJECTS = Path.home() / "projects"
TASKMASTER = Path.home() / ".taskmaster" / "tasks.json"

def get_yesterday_commits():
    """Get git commits from yesterday"""
    commits = []
    
    for proj in PROJECTS.iterdir():
        if not proj.is_dir() or not (proj / ".git").exists():
            continue
        
        try:
            result = subprocess.run(
                ["git", "log", "--since=midnight", "--until=now", "--oneline"],
                cwd=proj, capture_output=True, text=True, timeout=5
            )
            if result.stdout.strip():
                commits.append((proj.name, result.stdout.strip().split("\n")))
        except:
            pass
    
    return commits

def get_tasks():
    """Get pending tasks from taskmaster"""
    if not TASKMASTER.exists():
        return []
    
    data = json.loads(TASKMASTER.read_text())
    return [t for t in data if not t.get("completed")]

def get_blockers():
    """Check for known blockers"""
    # Would integrate with Notion or a blockers file
    return []

def generate():
    date = datetime.now().strftime("%Y-%m-%d")
    
    lines = [
        f"## Daily Standup - {date}",
        "",
        "### Yesterday",
    ]
    
    # Get commits
    commits = get_yesterday_commits()
    if commits:
        for proj, comms in commits[:3]:
            for c in comms[:2]:
                lines.append(f"- {proj}: {c}")
    else:
        lines.append("- No commits yesterday")
    
    lines.extend(["", "### Today"])
    
    # Get tasks
    tasks = get_tasks()
    if tasks:
        for t in tasks[:5]:
            priority = t.get("priority", "medium")[0].upper()
            lines.append(f"- [{priority}] {t['description']}")
    else:
        lines.append("- No active tasks")
    
    lines.extend(["", "### Blockers"])
    
    blockers = get_blockers()
    if blockers:
        for b in blockers:
            lines.append(f"- {b}")
    else:
        lines.append("- None")
    
    return "\n".join(lines)

def main():
    print(generate())


if __name__ == "__main__":
    main()
