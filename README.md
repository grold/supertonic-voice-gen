# Supertonic Voice Generator (Gemini CLI Extension)

This extension provides a specialized skill for generating studio-grade voice audio using the Supertonic SDK, with integrated Chromecast support for local playback.

## Features
- **Studio Quality**: 44.1kHz 16-bit WAV output.
- **Expression Tags**: Interactive support for `<laugh>`, `<breath>`, `<sigh>`, etc.
- **Chromecast Default**: Automatically plays on your "Bedroom speaker" (configurable).
- **Local Fallback**: Supports `mpv`, `vlc`, and `ffplay` for local testing.
- **Volume Control**: Easy `--volume` flag for both local and remote playback.

## Installation

```bash
gemini extensions install https://github.com/grold/supertonic-voice-gen
```

## Requirements
- [uv](https://github.com/astral-sh/uv)
- [FFmpeg](https://ffmpeg.org/) (for Chromecast/MP3 support)

## Skill Usage

Once installed, simply ask Gemini:
`voice "Hello world! <laugh>"`

See `skills/supertonic-voice-gen/SKILL.md` for full command flags and examples.
