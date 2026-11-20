"""Local metrics shared by the terminal and web dashboards."""

import shutil
import subprocess


def service_status():
    def running(pattern):
        return subprocess.run(["pgrep", "-f", pattern], capture_output=True).returncode == 0

    return {"gateway": running("openclaw.*gateway"), "heartbeat": running("heartbeat")}


def disk_used():
    usage = shutil.disk_usage("/")
    return f"{100 * usage.used / usage.total:.0f}%"
