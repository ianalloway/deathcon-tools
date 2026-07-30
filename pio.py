#!/usr/bin/env python3
"""
Personal Intelligence Officer (PIO)
Daily morning briefing - pulls from all your data sources
"""
import json
import os
from datetime import datetime
from pathlib import Path

# Config
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
GITHUB_USER = "ianalloway"

# Paths
PROJECTS_DIR = Path.home() / "projects"
APPLY_QUEUE = Path.home() / ".openclaw" / "apply-queue"


def get_github_activity():
    import urllib.request
    url = f"https://api.github.com/users/{GITHUB_USER}/events?per_page=10"
    req = urllib.request.Request(url)
    if GITHUB_TOKEN:
        req.add_header("Authorization", f"token {GITHUB_TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            events = json.loads(resp.read())
    except:
        return {"pushes": 0, "creates": 0}
    
    push_events = [e for e in events if e.get("type") == "PushEvent"]
    return {"pushes": len(push_events)}


def get_repo_stats():
    import urllib.request
    url = f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100"
    req = urllib.request.Request(url)
    if GITHUB_TOKEN:
        req.add_header("Authorization", f"token {GITHUB_TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            repos = json.loads(resp.read())
    except:
        return {"total": 0, "stars": 0}
    
    total_stars = sum(r.get("stargazers_count", 0) for r in repos)
    return {"total": len(repos), "stars": total_stars}


def get_job_status():
    if not APPLY_QUEUE.exists():
        return {"pending": 0, "approved": 0}
    files = list(APPLY_QUEUE.glob("*.json"))
    pending = approved = 0
    for f in files:
        content = f.read_text()
        if "pending" in content: pending += 1
        if "approved" in content: approved += 1
    return {"pending": pending, "approved": approved}


def get_project_status():
    projects = [
        "sports-betting-ml", "ai-advantage", "Money-maker-bot",
        "job-match-scanner", "cold-outreach", "repo-health",
        "deathcon-dashboard", "taskmaster", "blog-idea-engine",
    ]
    status = {}
    for proj in projects:
        path = PROJECTS_DIR / proj
        status[proj] = "active" if path.exists() else "missing"
    return status


def generate_briefing(github, repos, jobs, projects):
    date = datetime.now().strftime("%Y-%m-%d")
    
    lines = [
        f"## Morning Briefing - {date}",
        "",
        "### Activity",
        f"- GitHub: {github.get('pushes', 0)} recent pushes, {repos.get('stars', 0)} stars across {repos.get('total', 0)} repos",
        f"- Jobs: {jobs.get('pending', 0)} pending applications, {jobs.get('approved', 0)} approved",
        "",
        "### Projects",
    ]
    
    for proj, status in projects.items():
        if status == "active":
            lines.append(f"- {proj}: active")
    
    lines.extend([
        "",
        "### Today's Focus",
        "- Review job queue for new matches",
        "- Keep shipping",
    ])
    
    return "\n".join(lines)


def main():
    print(" Gathering intelligence...")
    
    github = get_github_activity()
    repos = get_repo_stats()
    jobs = get_job_status()
    projects = get_project_status()
    
    briefing = generate_briefing(github, repos, jobs, projects)
    
    print("\n" + briefing)
    
    output = Path.home() / ".openclaw" / "pio" / "briefing.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(briefing)
    print(f"\n[Saved to {output}]")


if __name__ == "__main__":
    main()
