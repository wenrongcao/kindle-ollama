# Kindle Ollama Chat — Project Summary

## Overview
A lightweight Python web server that exposes a chat UI for Ollama LLMs, accessible from a Kindle's basic browser over home WiFi.

## Hardware
- **Server:** NVIDIA Jetson AGX Orin, Ubuntu, IP `192.168.0.119`
- **Client:** Kindle (basic browser, e-ink screen, ~1072px wide viewport, no DPI scaling)

## Access
- Run: `python3 server.py`
- URL: `http://192.168.0.119:8080`

## Files
| File | Purpose |
|---|---|
| `server.py` | Single-file HTTP server + chat UI |
| `requirements.txt` | `ollama>=0.6.0` |
| `README.md` | Project docs with demo screenshot |
| `IMG_6350.jpg` | Demo photo of Kindle running the UI |
| `.gitignore` | Ignores pycache, logs, .env |

## Key Design Decisions
- Pure Python `http.server` stdlib — no Flask needed
- `ollama` Python package for LLM calls (not raw urllib)
- No JavaScript — plain HTML form POST, page-reload chat
- Conversation history in global in-memory list (single user)
- Large fonts (26px base, 34px heading) for Kindle e-ink readability
- Kindle browser quirk: reports full physical resolution (~1072px) as viewport with no DPI scaling — so fonts must be explicitly large

## GitHub
https://github.com/wenrongcao/kindle-ollama
