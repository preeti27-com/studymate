"""
StudyMate - Vercel Serverless Function Handler
Handles web API requests at /api/chat
"""

import json
import os
import sys
from http.server import BaseHTTPRequestHandler

# Ensure project root is in sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import chatbot


class handler(BaseHTTPRequestHandler):
    """Vercel serverless request handler."""

    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        """Handles pre-flight CORS requests."""
        self._set_headers(200)

    def do_GET(self):
        """Health check endpoint."""
        self._set_headers(200)
        payload = {
            "status": "online",
            "bot": "StudyMate",
            "message": "StudyMate Chatbot API is active on Vercel."
        }
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_POST(self):
        """Processes incoming user chat messages."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length)
            data = json.loads(post_body.decode("utf-8")) if post_body else {}
        except Exception:
            data = {}

        raw_input = str(data.get("message", "")).strip()
        user_name = data.get("user_name", None)

        user_input = raw_input.lower()
        bot_response, updated_name = chatbot.get_response(user_input, raw_input, user_name)

        # Strip "StudyMate: " prefix if present for clean web UI presentation
        display_text = bot_response
        if display_text.startswith("StudyMate: "):
            display_text = display_text[len("StudyMate: "):]

        response_payload = {
            "response": display_text,
            "raw_response": bot_response,
            "user_name": updated_name
        }

        self._set_headers(200)
        self.wfile.write(json.dumps(response_payload).encode("utf-8"))
