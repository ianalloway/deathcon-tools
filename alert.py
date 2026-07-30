#!/usr/bin/env python3
"""
Alert System - Custom alerts and notifications
"""
import json
import sys
from pathlib import Path
from datetime import datetime

ALERTS_FILE = Path.home() / ".alerts.json"

def load_alerts():
    if ALERTS_FILE.exists():
        return json.loads(ALERTS_FILE.read_text())
    return []

def save_alerts(alerts):
    ALERTS_FILE.write_text(json.dumps(alerts, indent=2))

def add_alert(message, level="info", tag=None):
    alerts = load_alerts()
    alerts.append({
        "message": message,
        "level": level,  # info, warning, error, critical
        "tag": tag,
        "created": datetime.now().isoformat(),
        "read": False
    })
    save_alerts(alerts)
    return f"Alert added: {message[:50]}"

def list_alerts(unread_only=False):
    alerts = load_alerts()
    if not alerts:
        return "No alerts."
    
    if unread_only:
        alerts = [a for a in alerts if not a.get("read")]
    
    lines = [f"\nAlerts ({len(alerts)}):"]
    for a in alerts[-10:]:
        icon = {"info": "ℹ️", "warning": "⚠️", "error": "❌", "critical": "🚨"}.get(a.get("level", "info"), "📬")
        lines.append(f"{icon} {a['message'][:60]}")
    return "\n".join(lines)

def mark_read(index):
    alerts = load_alerts()
    if 0 <= index < len(alerts):
        alerts[index]["read"] = True
        save_alerts(alerts)
        return f"Marked alert {index} as read"
    return "Invalid index"

def clear():
    save_alerts([])
    return "All alerts cleared"

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    
    if cmd == "add":
        message = " ".join(sys.argv[2:-1]) if len(sys.argv) > 2 else ""
        level = sys.argv[-1] if len(sys.argv) > 2 else "info"
        if level not in ["info", "warning", "error", "critical"]:
            level = "info"
            message = " ".join(sys.argv[2:])
        print(add_alert(message, level))
    
    elif cmd == "list":
        print(list_alerts())
    
    elif cmd == "unread":
        print(list_alerts(unread_only=True))
    
    elif cmd == "read":
        idx = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        print(mark_read(idx))
    
    elif cmd == "clear":
        print(clear())
    
    else:
        print("Usage: alert add <message> [level]")
        print("       alert list")
        print("       alert unread")
        print("       alert read <index>")
        print("       alert clear")

if __name__ == "__main__":
    main()
