#!/usr/bin/env python3
"""
MISSION CONTROL - Your Personal Command Center
"""
import json
import os
from html import escape
from pathlib import Path

from host_status import disk_used, service_status

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_USER = "ianalloway"

PROJECTS = Path.home() / "projects"
WORKSPACE = Path.home() / ".openclaw" / "workspace"
APPLY_QUEUE = Path.home() / ".openclaw" / "apply-queue"
TASKS = Path.home() / ".taskmaster" / "tasks.json"
NOTES = Path.home() / ".quick_notes.md"
LEARNING = Path.home() / ".learning.json"

HTML = """<!DOCTYPE html>
<html><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#0d1117;color:#c9d1d9;min-height:100vh}
.header{background:#161b22;padding:20px;border-bottom:1px solid #30363d;display:flex;justify-content:space-between;align-items:center}
.header h1{color:#58a6ff;font-size:24px}
.header .time{color:#8b949e}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:16px;padding:20px}
.card{background:#161b22;border:1px solid #30363d;border-radius:6px;padding:16px}
.card h2{color:#58a6ff;font-size:16px;margin-bottom:12px}
.stat{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #21262d}
.stat .label{color:#8b949e}
.stat .value{color:#58a6ff;font-weight:600}
.value.green{color:#3fb950}
.value.yellow{color:#d29922}
.list{max-height:200px;overflow-y:auto}
.list-item{padding:8px;margin:4px 0;background:#21262d;border-radius:4px;font-size:13px}
.priority-H{border-left:3px solid #f85149}
.priority-M{border-left:3px solid #d29922}
.priority-L{border-left:3px solid #3fb950}
.refresh{background:#238636;color:#fff;border:none;padding:8px 16px;border-radius:4px;cursor:pointer}
.refresh:hover{background:#2ea043}
.footer{text-align:center;padding:20px;color:#8b949e;font-size:12px}
</style></head>
<body>
<div class="header">
<h1>⚰️ Mission Control</h1>
<span class="time" id="time"></span>
</div>
<div class="grid">
<div class="card"><h2>📊 Overview</h2>
<div class="stat"><span class="label">Repos</span><span class="value" id="repos">-</span></div>
<div class="stat"><span class="label">Stars</span><span class="value" id="stars">-</span></div>
<div class="stat"><span class="label">Jobs Pending</span><span class="value" id="pending">-</span></div>
<div class="stat"><span class="label">Jobs Approved</span><span class="value green" id="approved">-</span></div>
</div>
<div class="card"><h2>📋 Tasks</h2><div class="list" id="tasks"></div></div>
<div class="card"><h2>💼 Projects</h2><div class="list" id="projects"></div></div>
<div class="card"><h2>🧠 Skills</h2><div class="list" id="skills"></div></div>
<div class="card"><h2>📝 Notes</h2><div class="list" id="notes"></div></div>
<div class="card"><h2>🔧 System</h2>
<div class="stat"><span class="label">Gateway</span><span class="value green" id="gateway">-</span></div>
<div class="stat"><span class="label">Heartbeat</span><span class="value green" id="heartbeat">-</span></div>
<div class="stat"><span class="label">Disk</span><span class="value" id="disk">-</span></div>
</div>
</div>
<div class="footer">Last updated: <span id="updated"></span></div>
<script>
function update(){document.getElementById('time').textContent=new Date().toLocaleString();document.getElementById('updated').textContent=new Date().toLocaleTimeString()}
update();setInterval(update,1000);
</script></body></html>"""

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
        if '"status": "pending"' in content or '"status": "approved"' in content:
            if "pending" in content: pending += 1
            if "approved" in content: approved += 1
    return pending, approved

def get_tasks():
    if not TASKS.exists():
        return []
    data = json.loads(TASKS.read_text())
    return [t for t in data if not t.get("completed")][:5]

def get_projects():
    key = ["sports-betting-ml", "ai-advantage", "Money-maker-bot", "job-match-scanner", 
           "cold-outreach", "taskmaster", "deathcon-dashboard", "blog-idea-engine"]
    return [{"n": p, "s": "active" if (PROJECTS / p).exists() else "missing"} for p in key]

def get_skills():
    if not LEARNING.exists():
        return []
    return json.loads(LEARNING.read_text()).get("skills", [])[:5]

def get_notes():
    if not NOTES.exists():
        return []
    return NOTES.read_text().strip().split("\n")[:5]

def get_system():
    status = service_status()
    return ("UP" if status["gateway"] else "DOWN",
            "UP" if status["heartbeat"] else "DOWN",
            disk_used())


def generate():
    repos, stars = get_github()
    pending, approved = get_jobs()
    tasks = get_tasks()
    projects = get_projects()
    skills = get_skills()
    notes = get_notes()
    gw, hb, disk = get_system()
    
    # Build HTML with data
    html = HTML
    html = html.replace('id="repos">-', f'id="repos">{repos}')
    html = html.replace('id="stars">-', f'id="stars">{stars}')
    html = html.replace('id="pending">-', f'id="pending">{pending}')
    html = html.replace('id="approved">-', f'id="approved">{approved}')
    html = html.replace('id="gateway">-', f'id="gateway">{gw}')
    html = html.replace('id="heartbeat">-', f'id="heartbeat">{hb}')
    html = html.replace('id="disk">-', f'id="disk">{disk}')
    
    # Tasks
    task_html = ""
    for t in tasks:
        p = {"high": "H", "medium": "M", "low": "L"}.get(str(t.get("priority", "")).lower(), "M")
        task_html += f'<div class="list-item priority-{p}">{escape(str(t.get("description", ""))[:45])}</div>'
    html = html.replace('<div class="list" id="tasks"></div>', f'<div class="list">{task_html}</div>')
    
    # Projects
    proj_html = ""
    for p in projects:
        icon = "🟢" if p["s"] == "active" else "🔴"
        proj_html += f'<div class="list-item">{icon} {p["n"]}</div>'
    html = html.replace('<div class="list" id="projects"></div>', f'<div class="list">{proj_html}</div>')
    
    # Skills
    skill_html = ""
    for s in skills:
        skill_html += f'<div class="list-item">{escape(str(s.get("name", "")))} ({escape(str(s.get("level", "")))})</div>'
    html = html.replace('<div class="list" id="skills"></div>', f'<div class="list">{skill_html}</div>')
    
    # Notes
    note_html = ""
    for n in notes:
        note_html += f'<div class="list-item">{escape(str(n))}</div>'
    html = html.replace('<div class="list" id="notes"></div>', f'<div class="list">{note_html}</div>')
    
    return html

import urllib.request

def main():
    output = WORKSPACE / "dashboard.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(generate(), encoding="utf-8")
    print(f"Dashboard: {output}")
    return output

if __name__ == "__main__":
    main()
