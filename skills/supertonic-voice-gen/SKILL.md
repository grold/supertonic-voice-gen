---
name: supertonic-voice-gen
description: Use when you need to generate high-quality voice audio for testing expression tags or vocal styles.
---

# Supertonic Voice Generator

Generate studio-grade 44.1kHz voice audio with interactive expression tags.

## Usage

`voice "<text>" [flags]`

### Examples
- `voice "Hello world"`
- `voice "That's hilarious! <laugh>" --voice F1 --speed 1.2`
- `voice "I am... <breath> very tired." --steps 12`

### Tags supported
`<laugh>`, `<breath>`, `<sigh>`, `<cough>`, `<throat_clearing>`

### Implementation
This skill calls `uv run scripts/generate_voice.py`.
