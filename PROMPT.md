# Replication Prompt

Use the following prompt to recreate this project with Claude Code or any AI coding assistant.

---

> I need you to create a simple web server using Python to run Ollama AI chat so I can access it using a Kindle's very basic web browser via home WiFi.
>
> **Server machine:** Linux (e.g. NVIDIA Jetson AGX Orin or any Ubuntu machine)
> **Local IP:** `<your-machine-ip>` (e.g. `192.168.0.119`)
> **Client:** Kindle e-reader using its built-in experimental browser
>
> **Requirements:**
> - Single file `server.py` in the project folder
> - Use the `ollama` Python package (install via `pip install ollama`) to communicate with the local Ollama instance
> - Use Python's built-in `http.server` — no Flask or other web frameworks
> - The UI must work with no JavaScript — plain HTML form with POST submission and full page reload on each message
> - Conversation history stored in-memory server-side (single user assumed)
> - A dropdown to select from all locally available Ollama models
> - A "Clear Chat" button to reset the conversation
> - A "Send" button to submit messages
> - Also include `requirements.txt`, `.gitignore`, and `README.md` with a demo image
>
> **Kindle browser quirks to handle:**
> - Kindle browser reports its full physical pixel resolution (~1072px wide) as the CSS viewport with no DPI scaling — so everything looks tiny on the 6-inch e-ink screen
> - Use large fonts: base `26px`, headings `34px`, buttons and inputs `26px`
> - Avoid JavaScript, `box-shadow`, and complex CSS — the browser is old WebKit (circa 2009)
> - Use `<meta name="viewport" content="width=device-width, initial-scale=1">`
>
> **Run it with:**
> ```bash
> pip install -r requirements.txt
> python3 server.py
> ```
> Then open `http://<your-machine-ip>:8080` in the Kindle browser.
