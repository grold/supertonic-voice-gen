# `supertonic-voice-gen` Implementation Plan (Updated for Chromecast)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Gemini CLI skill for interactive voice generation using the Supertonic SDK, with default playback on "Bedroom speaker" via Chromecast.

**Architecture:** A Python driver script (`scripts/generate_voice.py`) handles synthesis, starts a temporary HTTP server, and triggers Chromecast playback. Local playback fallback included.

**Tech Stack:** Python, Supertonic SDK, `pychromecast`, `uv`.

---

### Task 1-3: Driver & Synthesis (Completed)
Tasks 1-3 are already implemented and provide the core synthesis and local playback fallback.

---

### Task 5: Chromecast Integration

**Files:**
- Modify: `scripts/generate_voice.py`
- Test: `tests/test_voice_gen_extended.py`

- [ ] **Step 1: Implement Local IP Detection**
```python
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80)) # Doesn't actually connect
        return s.getsockname()[0]
    except Exception:
        return socket.gethostbyname(socket.gethostname())
    finally:
        s.close()
```

- [ ] **Step 2: Implement Threaded HTTP Server**
```python
import http.server
import socketserver
import threading

def start_temporary_server(file_path, port=8000):
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd
```

- [ ] **Step 3: Implement Chromecast Playback Logic**
```python
import pychromecast

def play_on_chromecast(file_path, friendly_name, local_ip, port):
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[friendly_name])
    if not chromecasts:
        return False
    
    cast = chromecasts[0]
    cast.wait()
    mc = cast.media_controller
    url = f"http://{local_ip}:{port}/{file_path}"
    mc.play_media(url, 'audio/wav')
    mc.block_until_active()
    return True
```

- [ ] **Step 4: Update `main()` with Chromecast-first logic**
```python
# In main():
# 1. Synthesize
# 2. Check if casting is requested (and not --no-cast)
# 3. If cast:
#    - Detect IP
#    - Start server
#    - play_on_chromecast
# 4. Fallback to local playback if cast fails or --no-cast
```

- [ ] **Step 5: Verify via mock/manual test**
Run: `uv run scripts/generate_voice.py "Testing Chromecast" --cast "Bedroom speaker"`

- [ ] **Step 6: Commit**
```bash
git add scripts/generate_voice.py
git commit -m "feat: add Chromecast support via pychromecast"
```

---

### Task 4: Gemini CLI Skill (Updated)

**Files:**
- Modify: `skills/supertonic-voice-gen/SKILL.md`

- [ ] **Step 1: Update SKILL.md documentation**
```markdown
# Supertonic Voice Generator

Generate studio-grade 44.1kHz voice audio with interactive expression tags. 
**Plays on "Bedroom speaker" by default.**

## Usage

`voice "<text>" [flags]`

### Examples
- `voice "Hello world"` (Plays on Bedroom speaker)
- `voice "Test" --no-cast` (Plays locally)
- `voice "Test" --cast "Living Room"` (Plays on specific device)
```

- [ ] **Step 2: Re-install and Reload**
Run: `gemini skills install ./skills/supertonic-voice-gen --scope workspace`
Run: `/skills reload`

- [ ] **Step 3: Commit**
```bash
git add skills/supertonic-voice-gen/SKILL.md
git commit -m "docs: update skill for Chromecast defaults"
```
