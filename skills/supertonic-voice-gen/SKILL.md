---
name: supertonic-voice-gen
description: Use when you need to generate high-quality voice audio for testing expression tags or vocal styles.
---

# Supertonic Voice Generator

Generate studio-grade 44.1kHz voice audio with interactive expression tags.
**Plays on "Bedroom speaker" by default via Chromecast.**

## Usage

`voice "<text>" [flags]`

### Examples
- `voice "Hello world"` (Plays on Bedroom speaker)
- `voice "That's hilarious! <laugh>" --voice F1 --speed 1.2`
- `voice "I am... <breath> very tired." --no-cast` (Plays locally)
- `voice "Test" --cast "Living Room speaker"` (Plays on specific device)
- `voice "Turn it up! <laugh>" --volume 80`

### Tags supported
`<laugh>`, `<breath>`, `<sigh>`, `<cough>`, `<throat_clearing>` (Note: some tags may vary by model)

### Requirements
- **uv**: This skill uses `uv run` to manage its Python environment.
- **FFmpeg**: Required for MP3 conversion (for Chromecast playback).
- **Dependencies**: The skill requires `supertonic`, `pychromecast`, and `pydub` (handled via `pyproject.toml` in the extension root).

### Implementation
This skill calls the bundled `scripts/generate_voice.py` using `uv run`.
The agent should look for the absolute path to this script in the skill directory.
