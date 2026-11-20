#!/usr/bin/env python3
"""
System Health Checker - Simplified
"""
import os

from host_status import disk_used, service_status

def main():
    print(" Deathconbot Health")
    print("=" * 30)
    
    services = service_status()
    print(f"Gateway: {'UP' if services['gateway'] else 'DOWN'}")
    print(f"Heartbeat: {'UP' if services['heartbeat'] else 'DOWN'}")

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
    
    print(f"\nDisk: {disk_used()}")


if __name__ == "__main__":
    main()
