import io
from email.message import Message
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import api_server
import dashboard
import host_status


class DashboardTests(unittest.TestCase):
    def handle(self, path, head_only=False, host="localhost:8080"):
        handler = MagicMock()
        handler.server.server_port = 8080
        handler.headers = Message()
        handler.headers["Host"] = host
        handler.path = path
        handler.wfile = io.BytesIO()
        api_server.Handler.serve_dashboard(handler, head_only)
        return handler

    def test_api_returns_one_json_document(self):
        with patch.object(api_server, "dashboard_data", return_value={"tasks": []}):
            handler = self.handle("/api")
        self.assertEqual(json.loads(handler.wfile.getvalue()), {"tasks": []})
        handler.send_response.assert_called_once_with(200)

    def test_dashboard_aliases_and_head(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "dashboard.html").write_bytes(b"dashboard")
            with patch.object(api_server, "WORKSPACE", root):
                for path in ("/", "/dashboard", "/dashboard.html"):
                    self.assertEqual(self.handle(path).wfile.getvalue(), b"dashboard")
                handler = self.handle("/dashboard", head_only=True)
                self.assertEqual(handler.wfile.getvalue(), b"")
                handler.send_header.assert_any_call("Content-Length", "9")
                self.handle("/unknown").send_error.assert_called_once_with(404)

    def test_html_displays_note_as_text(self):
        with patch.multiple(dashboard, get_github=lambda: (1, 2), get_jobs=lambda: (0, 1),
                            get_tasks=lambda: [], get_projects=lambda: [], get_skills=lambda: [],
                            get_notes=lambda: ["Meals & recipes"], get_system=lambda: ("UP", "UP", "30%")):
            self.assertIn("Meals &amp; recipes", dashboard.generate())

    def test_disk_display_uses_numeric_filesystem_values(self):
        with patch.object(host_status.shutil, "disk_usage") as usage:
            usage.return_value.used, usage.return_value.total = 25, 100
            self.assertEqual(host_status.disk_used(), "25%")
            usage.return_value.used = 0
            self.assertEqual(host_status.disk_used(), "0%")

    def test_server_accepts_only_its_local_names(self):
        self.handle("/api", host="example.org").send_error.assert_called_once_with(403)
        with patch.object(api_server, "dashboard_data", return_value={}):
            self.handle("/api", host="127.0.0.1:8080").send_response.assert_called_once_with(200)
