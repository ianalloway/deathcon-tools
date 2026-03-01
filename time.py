#!/usr/bin/env python3
"""
Time Tracker - Track time on projects
"""
import json
import sys
from pathlib import Path
from datetime import datetime

TIMES_FILE = Path.home() / ".timetrack.json"

def load():
    if TIMES_FILE.exists():
        return json.loads(TIMES_FILE.read_text())
    return {}

def save(data):
    TIMES_FILE.write_text(json.dumps(data, indent=2))

def start(project):
    data = load()
    data["current"] = {"project": project, "start": datetime.now().isoformat()}
    save(data)
    return f"Started tracking: {project}"

def stop():
    data = load()
    if "current" not in data:
        return "Nothing tracking."
    
    current = data["current"]
    start_time = datetime.fromisoformat(current["start"])
    duration = (datetime.now() - start_time).total_seconds() / 60
    
    if "sessions" not in data:
        data["sessions"] = []
    data["sessions"].append({
        "project": current["project"],
        "start": current["start"],
        "end": datetime.now().isoformat(),
        "minutes": round(duration, 1)
    })
    del data["current"]
    save(data)
    return f"Stopped {current['project']}. Tracked {round(duration, 1)} minutes."

def status():
    data = load()
    if "current" not in data:
        return "Not tracking anything."
    
    current = data["current"]
    start_time = datetime.fromisoformat(current["start"])
    elapsed = (datetime.now() - start_time).total_seconds() / 60
    return f"Tracking: {current['project']} ({round(elapsed, 1)} min)"

def report():
    data = load()
    sessions = data.get("sessions", [])
    
    if not sessions:
        return "No tracked time."
    
    by_project = {}
    for s in sessions:
        p = s["project"]
        by_project[p] = by_project.get(p, 0) + s["minutes"]
    
    lines = ["\nTime Report:"]
    total = 0
    for p, mins in sorted(by_project.items(), key=lambda x: -x[1]):
        lines.append(f"  {p}: {round(mins, 1)} min")
        total += mins
    lines.append(f"  Total: {round(total, 1)} min")
    return "\n".join(lines)

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    
    if cmd == "start":
        project = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "default"
        print(start(project))
    
    elif cmd == "stop":
        print(stop())
    
    elif cmd == "status":
        print(status())
    
    elif cmd == "report":
        print(report())
    
    else:
        print("Usage: time start <project>")
        print("       time stop")
        print("       time status")
        print("       time report")

if __name__ == "__main__":
    main()
