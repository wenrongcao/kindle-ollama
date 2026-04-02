#!/usr/bin/env python3
"""
Simple Ollama chat web server for Kindle browser.
Access at: http://192.168.0.119:8080
"""

import ollama
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

HOST = "0.0.0.0"
PORT = 8080
DEFAULT_MODEL = "qwen3.5:2b"

# Global conversation history (single-user; fine for Kindle use)
messages = []


def get_models():
    try:
        return [m.model for m in ollama.list().models]
    except Exception:
        return [DEFAULT_MODEL]


def chat_ollama(model, history):
    try:
        response = ollama.chat(model=model, messages=history)
        return response.message.content
    except Exception as e:
        return f"[Error: {e}]"


def html_escape(text):
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
    )


def render_page(model, models_list, status=""):
    model_options = "\n".join(
        f'<option value="{html_escape(m)}"{"  selected" if m == model else ""}>{html_escape(m)}</option>'
        for m in models_list
    )

    chat_html = ""
    for msg in messages:
        role = msg["role"]
        content = html_escape(msg["content"])
        # Preserve newlines
        content = content.replace("\n", "<br>")
        if role == "user":
            chat_html += f'<div class="msg user"><b>You:</b><br>{content}</div>\n'
        else:
            chat_html += f'<div class="msg assistant"><b>AI:</b><br>{content}</div>\n'

    status_html = f'<p class="status">{html_escape(status)}</p>' if status else ""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Ollama Chat</title>
<style>
body {{ font-family: Georgia, serif; margin: 0; padding: 12px; background: #f5f0e8; color: #111; font-size: 26px; }}
h1 {{ font-size: 34px; margin: 6px 0 12px 0; }}
.chat {{ border: 2px solid #aaa; background: #fff; padding: 12px; min-height: 300px; margin-bottom: 14px; }}
.msg {{ margin-bottom: 16px; padding: 10px; }}
.user {{ background: #dde8ff; }}
.assistant {{ background: #e8f5e8; }}
textarea {{ width: 100%; box-sizing: border-box; font-size: 26px; padding: 10px; }}
select {{ font-size: 24px; padding: 6px; width: 100%; margin-bottom: 10px; }}
input[type=submit] {{ font-size: 26px; padding: 10px 20px; margin: 6px 8px 6px 0; }}
.status {{ color: #888; font-size: 22px; }}
label {{ font-size: 24px; }}
</style>
</head>
<body>
<h1>Ollama Chat</h1>
{status_html}
<div class="chat" id="chat">
{chat_html if chat_html else '<p style="color:#aaa">No messages yet.</p>'}
</div>
<form method="POST" action="/chat">
<label>Model:
<select name="model">{model_options}</select>
</label><br><br>
<textarea name="message" rows="4" placeholder="Type your message here..."></textarea><br>
<input type="submit" value="Send">
<input type="submit" name="action" value="Clear Chat">
</form>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # Simple logging
        print(f"[{self.address_string()}] {fmt % args}")

    def send_html(self, html, code=200):
        encoded = html.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def redirect(self, location="/"):
        self.send_response(303)
        self.send_header("Location", location)
        self.end_headers()

    def do_GET(self):
        if urlparse(self.path).path == "/":
            models = get_models()
            model = models[0] if models else DEFAULT_MODEL
            self.send_html(render_page(model, models))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        global messages
        path = urlparse(self.path).path
        if path != "/chat":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        params = parse_qs(body)

        model = params.get("model", [DEFAULT_MODEL])[0]
        action = params.get("action", [""])[0]
        user_msg = params.get("message", [""])[0].strip()

        models = get_models()

        if action == "Clear Chat":
            messages = []
            self.send_html(render_page(model, models, status="Chat cleared."))
            return

        if not user_msg:
            self.send_html(render_page(model, models, status="Please enter a message."))
            return

        messages.append({"role": "user", "content": user_msg})
        reply = chat_ollama(model, messages)
        messages.append({"role": "assistant", "content": reply})

        self.send_html(render_page(model, models))


if __name__ == "__main__":
    print(f"Starting Ollama chat server on http://{HOST}:{PORT}")
    print(f"Kindle: point browser to http://192.168.0.119:{PORT}")
    print("Press Ctrl+C to stop.")
    server = HTTPServer((HOST, PORT), Handler)
    server.serve_forever()
