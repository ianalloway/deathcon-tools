#!/usr/bin/env python3
"""
Webhook Handler - Receives webhooks and triggers actions
"""
import json
import sys
from pathlib import Path
from datetime import datetime

HOOKS_FILE = Path.home() / ".webhooks.json"

def load_hooks():
    if HOOKS_FILE.exists():
        return json.loads(HOOKS_FILE.read_text())
    return {}

def save_hooks(hooks):
    HOOKS_FILE.write_text(json.dumps(hooks, indent=2))

def add_hook(name, url, event):
    hooks = load_hooks()
    hooks[name] = {"url": url, "event": event, "created": datetime.now().isoformat()}
    save_hooks(hooks)
    return f"Added hook: {name}"

def list_hooks():
    hooks = load_hooks()
    if not hooks:
        return "No hooks configured."
    lines = ["Webhooks:"]
    for name, data in hooks.items():
        lines.append(f"  - {name}: {data['event']} -> {data['url']}")
    return "\n".join(lines)

def trigger_hook(name, payload):
    # Would actually fire the webhook here
    print(f"Triggering {name} with payload: {payload}")
    return f"Triggered: {name}"

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    
    if cmd == "add":
        name = sys.argv[2] if len(sys.argv) > 2 else "hook"
        url = sys.argv[3] if len(sys.argv) > 3 else ""
        event = sys.argv[4] if len(sys.argv) > 4 else "push"
        print(add_hook(name, url, event))
    
    elif cmd == "list":
        print(list_hooks())
    
    elif cmd == "trigger":
        name = sys.argv[2] if len(sys.argv) > 2 else ""
        payload = sys.argv[3] if len(sys.argv) > 3 else "{}"
        print(trigger_hook(name, payload))
    
    else:
        print("Usage: webhook add <name> <url> <event>")
        print("       webhook list")
        print("       webhook trigger <name>")

if __name__ == "__main__":
    main()
