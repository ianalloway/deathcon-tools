#!/usr/bin/env python3
"""
API Server - Serves dashboard + provides JSON endpoints
"""
import json
import os
import subprocess
import urllib.request
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_USER = "ianalloway"

PROJECTS = Path.home() / "projects"
APPLY_QUEUE = Path.home() / ".openclaw" / "apply-queue"
TASKS = Path.home() / ".taskmaster" / "tasks.json"
NOTES = Path.home() / ".quick_notes.md"
LEARNING = Path.home() / ".learning.json"
WORKSPACE = Path.home() / ".openclaw" / "workspace"

def get_github():
    try:
        url = f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100"
        req = urllib.request.Request(url)
        if GITHUB_TOKEN:
            req.add_header("Authorization", f"token {GITHUB_TOKEN}")
        with urllib.request.urlopen(req, timeout=10) as resp:
            repos = json.loads(resp.read())
        stars = sum(r.get("stargazers_count", 0) for r in repos)
        return len(repos), stars
    except:
        return 0, 0

def get_jobs():
    if not APPLY_QUEUE.exists():
        return 0, 0
    files = list(APPLY_QUEUE.glob("*.json"))
    pending = approved = 0
    for f in files:
        content = f.read_text()
        if "pending" in content: pending += 1
        if "approved" in content: approved += 1
    return pending, approved

def get_tasks():
    if not TASKS.exists():
        return []
    data = json.loads(TASKS.read_text())
    return [{"id": t.get("id"), "desc": t.get("description", "")[:50], "priority": t.get("priority", "medium")} 
            for t in data if not t.get("completed")]

def get_projects():
    key = ["sports-betting-ml", "ai-advantage", "Money-maker-bot", "job-match-scanner", 
           "cold-outreach", "taskmaster", "deathcon-dashboard", "blog-idea-engine"]
    return [{"name": p, "active": (PROJECTS / p).exists()} for p in key]

def get_skills():
    if not LEARNING.exists():
        return []
    return json.loads(LEARNING.read_text()).get("skills", [])

def get_notes():
    if not NOTES.exists():
        return []
    return NOTES.read_text().strip().split("\n")

def get_system():
    r = subprocess.run(["pgrep", "-f", "openclaw.*gateway"], capture_output=True)
    gw = r.returncode == 0
    r = subprocess.run(["pgrep", "-f", "heartbeat"], capture_output=True)
    hb = r.returncode == 0
    return {"gateway": gw, "heartbeat": hb}

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api":
            data = {
                "github": {"repos": get_github()[0], "stars": get_github()[1]},
                "jobs": {"pending": get_jobs()[0], "approved": get_jobs()[1]},
                "tasks": get_tasks(),
                "projects": get_projects(),
                "skills": get_skills()[:5],
                "notes": get_notes()[:5],
                "system": get_system(),
                "timestamp": datetime.now().isoformat()
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data, indent=2).encode())
        elif self.path == "/" or self.path == "/dashboard":
            self.path = "/dashboard.html"
        return SimpleHTTPRequestHandler.do_GET(self)
    
    def log_message(self, format, *args):
        pass  # Suppress logging

def main(port=8080):
    os.chdir(WORKSPACE)
    server = HTTPServer(("", port), Handler)
    print(f"Mission Control API: http://localhost:{port}")
    print(f"Dashboard: http://localhost:{port}/dashboard.html")
    print(f"API: http://localhost:{port}/api")
    server.serve_forever()

if __name__ == "__main__":
    main()
