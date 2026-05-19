# Design Spec: `supertonic-voice-gen` Skill

**Date:** 2026-05-18
**Topic:** Interactive Voice Generation Testing via Supertonic (with Chromecast Support)
**Status:** Draft (Updated for Chromecast)

## 1. Overview
A specialized skill for Gemini CLI to generate studio-grade (44.1kHz) voice audio using the Supertonic ONNX-based SDK. The skill is optimized for **Interactive Testing**, allowing developers to rapidly iterate on expression tags (e.g., `<laugh>`, `<breath>`) and vocal styles. Audio is played by default on a local Google Home speaker.

## 2. Goals & Success Criteria
- **Chromecast Playback:** Default to playing audio on "Bedroom speaker" using `pychromecast`.
- **Rapid Feedback:** Backgrounded local audio playback via `mpv`/`vlc` as a fallback or if requested.
- **Explicit Control:** Stateless CLI interface with comprehensive flags for all Supertonic and Chromecast parameters.
- **Studio Quality:** Ensure output is always 44.1kHz 16-bit WAV.
- **Zero Configuration:** Auto-detect local IP for the Chromecast media URL.

## 3. Architecture

### A. Components
- **Python Driver (`scripts/generate_voice.py`):** Core logic. Uses `supertonic` for synthesis, `pychromecast` for discovery, and `http.server` for local hosting.
- **Skill Wrapper (`SKILL.md`):** Exposes the `voice` command.
- **Local HTTP Server:** A temporary, threaded server that hosts the generated `.wav` file for the Chromecast to download.

### B. Data Flow
1. **User Input:** `voice "Text <tag>"` + flags.
2. **Synthesis:** Text processed into `voice_test.wav`.
3. **Serving:** Start a temporary HTTP server on a random port.
4. **Discovery:** Find "Bedroom speaker" via mDNS.
5. **Playback:** 
    - **Chromecast:** Send local URL (e.g., `http://192.168.1.50:8080/voice_test.wav`) to the speaker.
    - **Local (Fallback):** Trigger `mpv` or `vlc` if `--no-cast` is provided or if discovery fails.
6. **Cleanup:** Shut down HTTP server once playback starts.

## 4. Command Interface

### `voice <text> [flags]`

| Flag | Default | Description |
| :--- | :--- | :--- |
| `--voice` | `M1` | Preset (M1-3, F1-3) or path to custom voice. |
| `--speed` | `1.0` | Speed multiplier (0.7 - 2.0). |
| `--steps` | `8` | Inference steps (5 - 12). |
| `--lang` | `en` | ISO language code or `na`. |
| `--cast` | `"Bedroom speaker"` | Friendly name of the Chromecast device. |
| `--no-cast` | `False` | Force local playback instead of Chromecast. |
| `--output` | `voice_test.wav` | Destination filename. |
| `--play` | `True` | Enable playback (default). |
| `--no-play` | `False` | Disable all playback. |

## 5. Technical Implementation Details
- **IP Detection:** Use `socket.gethostbyname(socket.gethostname())` or connect to an external IP to determine the correct interface for mDNS.
- **Temporary Server:** Use `http.server.SimpleHTTPRequestHandler` in a `threading.Thread(daemon=True)`.
- **Discovery Timeout:** Set a reasonable timeout (e.g., 5s) for `pychromecast` to avoid hanging.

## 6. Validation Plan
- **Connectivity:** Verify the machine's IP is reachable by the Google Home.
- **Handshake:** Verify `pychromecast` correctly identifies the "Bedroom speaker".
- **Fallback:** Verify `--no-cast` correctly triggers local players (`mpv`).

