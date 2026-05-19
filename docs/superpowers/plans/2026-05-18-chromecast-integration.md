# Chromecast Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Chromecast support to the voice generation script, allowing users to play synthesized audio on a "Bedroom speaker" by default.

**Architecture:** Implement local IP detection, a threaded HTTP server to serve the audio file, and use `pychromecast` to trigger playback on the target device. Add command-line flags for cast control and fallback to local playback.

**Tech Stack:** Python, `pychromecast`, `http.server`, `socket`, `threading`.

---

### Task 1: Implement Local IP Detection

**Files:**
- Modify: `scripts/generate_voice.py`

- [ ] **Step 1: Add `get_local_ip` function**

```python
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't actually connect, just gets the interface IP
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except Exception:
        return socket.gethostbyname(socket.gethostname())
    finally:
        s.close()
```

- [ ] **Step 2: Add imports at the top of `scripts/generate_voice.py`**
Include `import socket` at the top of the file.

- [ ] **Step 3: Commit**

```bash
git add scripts/generate_voice.py
git commit -m "feat: add local IP detection helper"
```

### Task 2: Implement Threaded HTTP Server

**Files:**
- Modify: `scripts/generate_voice.py`

- [ ] **Step 1: Add `start_temporary_server` function**

```python
import http.server
import socketserver
import threading

def start_temporary_server(file_path, port=8000):
    # handler for serving just the directory of the file
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd
```

- [ ] **Step 2: Add imports at the top of `scripts/generate_voice.py`**
Include `import http.server`, `import socketserver`, `import threading`.

- [ ] **Step 3: Commit**

```bash
git add scripts/generate_voice.py
git commit -m "feat: add threaded HTTP server for serving audio"
```

### Task 3: Implement Chromecast Playback Logic

**Files:**
- Modify: `scripts/generate_voice.py`

- [ ] **Step 1: Add `play_on_chromecast` function**

```python
import pychromecast

def play_on_chromecast(file_path, friendly_name, local_ip, port):
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[friendly_name])
    if not chromecasts:
        return False
    
    cast = chromecasts[0]
    cast.wait()
    mc = cast.media_controller
    # file_path should be relative to the server root (current directory)
    url = f"http://{local_ip}:{port}/{file_path}"
    mc.play_media(url, 'audio/wav')
    mc.block_until_active()
    return True
```

- [ ] **Step 2: Add `import pychromecast` at the top**

- [ ] **Step 3: Commit**

```bash
git add scripts/generate_voice.py
git commit -m "feat: add Chromecast playback logic"
```

### Task 4: Update `main()` with Chromecast-first logic

**Files:**
- Modify: `scripts/generate_voice.py`

- [ ] **Step 1: Add --cast and --no-cast flags to the parser**

```python
    parser.add_argument("--cast", default="Bedroom speaker", help="Chromecast device name")
    parser.add_argument("--no-cast", action="store_true", help="Disable Chromecast playback")
```

- [ ] **Step 2: Update playback logic in `main()`**

```python
        if not args.no_play:
            played_remotely = False
            if not args.no_cast:
                try:
                    import random
                    local_ip = get_local_ip()
                    port = random.randint(8000, 9000)
                    httpd = start_temporary_server(args.output, port)
                    print(f"Playing on Chromecast: {args.cast}...")
                    if play_on_chromecast(args.output, args.cast, local_ip, port):
                        played_remotely = True
                        import time
                        time.sleep(2) # Give it a moment to start
                    else:
                        print(f"Warning: Chromecast '{args.cast}' not found.")
                except Exception as cast_err:
                    print(f"Warning: Chromecast playback failed: {cast_err}")

            if not played_remotely:
                if not play_audio(args.output, args.player):
                    print("Warning: No audio player found.")
```

- [ ] **Step 3: Commit**

```bash
git add scripts/generate_voice.py
git commit -m "feat: integrate Chromecast playback into main workflow"
```

### Task 5: Verify via mock test

**Files:**
- Create: `tests/test_voice_gen_extended.py`

- [ ] **Step 1: Create test file with mocks for `pychromecast`**

```python
import unittest
from unittest.mock import patch, MagicMock
import scripts.generate_voice as gv

class TestChromecastIntegration(unittest.TestCase):
    @patch('pychromecast.get_listed_chromecasts')
    def test_play_on_chromecast_success(self, mock_get):
        mock_cast = MagicMock()
        mock_get.return_value = ([mock_cast], MagicMock())
        
        result = gv.play_on_chromecast("test.wav", "Test Speaker", "127.0.0.1", 8000)
        
        self.assertTrue(result)
        mock_cast.wait.assert_called_once()
        mock_cast.media_controller.play_media.assert_called_once_with(
            "http://127.0.0.1:8000/test.wav", "audio/wav"
        )

    @patch('pychromecast.get_listed_chromecasts')
    def test_play_on_chromecast_failure(self, mock_get):
        mock_get.return_value = ([], MagicMock())
        result = gv.play_on_chromecast("test.wav", "Non-existent", "127.0.0.1", 8000)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run the test**

Run: `uv run python tests/test_voice_gen_extended.py`

- [ ] **Step 3: Commit**

```bash
git add tests/test_voice_gen_extended.py
git commit -m "test: add unit tests for Chromecast integration"
```
