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

### Tags supported
`<laugh>`, `<breath>`, `<sigh>`, `<cough>`, `<throat_clearing>`

### Implementation
This skill calls `uv run scripts/generate_voice.py`.
