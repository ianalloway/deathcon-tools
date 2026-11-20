#!/usr/bin/env python3
"""
API Server - Serves dashboard + provides JSON endpoints
"""
import json
import os
import urllib.request
from datetime import datetime
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit

from host_status import service_status

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

def dashboard_data():
    repos, stars = get_github()
    pending, approved = get_jobs()
    return {
        "github": {"repos": repos, "stars": stars},
        "jobs": {"pending": pending, "approved": approved},
        "tasks": get_tasks(),
        "projects": get_projects(),
        "skills": get_skills()[:5],
        "notes": get_notes()[:5],
        "system": service_status(),
        "timestamp": datetime.now().isoformat(),
    }


class Handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.serve_dashboard(head_only=True)

    def do_GET(self):
        self.serve_dashboard(head_only=False)

    def serve_dashboard(self, head_only):
        hosts = self.headers.get_all("Host", [])
        port = self.server.server_port
        allowed_hosts = {"localhost", "127.0.0.1", f"localhost:{port}", f"127.0.0.1:{port}"}
        if len(hosts) != 1 or hosts[0].lower() not in allowed_hosts:
            self.send_error(403)
            return
        path = urlsplit(self.path).path
        if path == "/api":
            content = json.dumps(dashboard_data(), indent=2).encode()
            content_type = "application/json"
        elif path in {"/", "/dashboard", "/dashboard.html"}:
            try:
                content = (WORKSPACE / "dashboard.html").read_bytes()
            except FileNotFoundError:
                self.send_error(404, "Generate the dashboard with dashboard.py")
                return
            content_type = "text/html; charset=utf-8"
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(content)

    def log_message(self, format, *args):
        pass  # Suppress logging

def main(port=8080):
    server = HTTPServer(("127.0.0.1", port), Handler)
    print(f"Mission Control API: http://localhost:{port}")
    print(f"Dashboard: http://localhost:{port}/dashboard.html")
    print(f"API: http://localhost:{port}/api")
    server.serve_forever()

if __name__ == "__main__":
    main()
