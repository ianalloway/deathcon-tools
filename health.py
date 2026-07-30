#!/usr/bin/env python3
"""
System Health Checker - Simplified
"""
import subprocess
import os

def check(name, cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return "OK" if result.returncode == 0 else "FAIL"

def main():
    print(" Deathconbot Health")
    print("=" * 30)
    
    # Check gateway
    result = subprocess.run(["pgrep", "-f", "openclaw.*gateway"], capture_output=True)
    print(f"Gateway: {'UP' if result.returncode == 0 else 'DOWN'}")
    
    # Check heartbeat
    result = subprocess.run(["pgrep", "-f", "heartbeat"], capture_output=True)
    print(f"Heartbeat: {'UP' if result.returncode == 0 else 'DOWN'}")
    
    # Check key dirs
    dirs = [
        ("Workspace", "~/.openclaw/workspace"),
        ("Projects", "~/projects"),
        ("Notion key", "~/.config/notion/api_key"),
    ]
    
    for name, path in dirs:
        path = os.path.expanduser(path)
        status = "OK" if os.path.exists(path) else "MISSING"
        print(f"{name}: {status}")
    
    # Check disk
    result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
    print(f"\nDisk: {result.stdout.split()[9]}")


if __name__ == "__main__":
    main()
