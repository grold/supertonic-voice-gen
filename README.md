# Supertonic Voice Generator (Gemini CLI Extension)

This extension provides a specialized skill for generating studio-grade voice audio using the Supertonic SDK, with integrated Chromecast support for local playback.

## Features
- **Studio Quality**: 44.1kHz 16-bit WAV output.
- **Expression Tags**: Interactive support for `<laugh>`, `<breath>`, `<sigh>`, etc.
- **Chromecast Default**: Automatically plays on your "Bedroom speaker" (configurable).
- **Local Fallback**: Supports `mpv`, `vlc`, and `ffplay` for local testing.
- **Volume Control**: Easy `--volume` flag for both local and remote playback.

## Prerequisites

This extension requires **uv** and **FFmpeg** to be installed on your system.

### 1. Install uv
[uv](https://github.com/astral-sh/uv) is used to manage the Python environment and dependencies automatically.

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install FFmpeg
[FFmpeg](https://ffmpeg.org/) is required for converting the high-quality WAV output to MP3 for Chromecast playback.

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS (Homebrew)
brew install ffmpeg
```

### 3. Automatic Python Setup
You **do not** need to manually install Python libraries like `supertonic` or `pychromecast`. 
The extension uses `uv run` with inline script metadata to:
- Automatically create a temporary virtual environment.
- Install all necessary Python dependencies on the first run.
- Download the required ONNX model weights (~100MB) from Hugging Face.

## Installation

```bash
gemini extensions install https://github.com/grold/supertonic-voice-gen
```

## Skill Usage

Once installed, simply ask Gemini:
`voice "Hello world! <laugh>"`

See `skills/supertonic-voice-gen/SKILL.md` for full command flags and examples.
