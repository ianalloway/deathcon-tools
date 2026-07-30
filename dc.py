#!/usr/bin/env python3
"""
DC - Deathcon CLI Launcher
All your tools in one command
"""
import subprocess
import sys
from pathlib import Path

TOOLS = {
    # Productivity
    "note": ("Quick note", "~/.openclaw/workspace/note.py"),
    "meeting": ("Meeting notes", "~/.openclaw/workspace/meeting.py"),
    "learn": ("Learning tracker", "~/.openclaw/workspace/learn.py"),
    "standup": ("Daily standup", "~/.openclaw/workspace/standup.py"),
    "task": ("Taskmaster", "~/.openclaw/workspace/taskmaster.py"),
    
    # Intelligence
    "pio": ("Morning briefing", "~/.openclaw/workspace/pio.py"),
    "social": ("Tweet generator", "~/.openclaw/workspace/social_poster.py"),
    "respond": ("Auto-responder", "~/.openclaw/workspace/auto_respond.py"),
    "dashboard": ("Mission Control", "~/.openclaw/workspace/dashboard.py"),
    
    # Tools
    "health": ("System health", "~/.openclaw/workspace/health.py"),
    "snippet": ("Code snippets", "~/.openclaw/workspace/snippets.py"),
    "time": ("Time tracker", "~/.openclaw/workspace/time.py"),
    "alert": ("Alert system", "~/.openclaw/workspace/alert.py"),
    "bookmark": ("Bookmarks", "~/.openclaw/workspace/bookmark.py"),
    "webhook": ("Webhooks", "~/.openclaw/workspace/webhook.py"),
    "api": ("API Server", "~/.openclaw/workspace/api_server.py"),
    
    # Generators
    "readme": ("README generator", "~/.openclaw/workspace/readme.py"),
}

def main():
    tool = sys.argv[1] if len(sys.argv) > 1 else ""
    
    if tool == "list":
        print("\nAvailable tools:")
        for name, (desc, path) in TOOLS.items():
            print(f"  dc {name:12} - {desc}")
        return
    
    if tool not in TOOLS:
        print(f"Unknown tool: {tool}")
        print("Run: dc list")
        return
    
    desc, path = TOOLS[tool]
    path = Path(path).expanduser()
    
    # Run with remaining args
    subprocess.run(["python3", path] + sys.argv[2:], capture_output=False)

if __name__ == "__main__":
    main()
