import argparse
import sys
from supertonic import TTS
import os

def main():
    parser = argparse.ArgumentParser(description="Supertonic Voice Generator")
    parser.add_argument("text", help="Text to synthesize")
    parser.add_argument("--voice", default="M1", help="Voice preset")
    parser.add_argument("--speed", type=float, default=1.0, help="Speed multiplier")
    parser.add_argument("--steps", type=int, default=8, help="Inference steps")
    parser.add_argument("--lang", default="en", help="Language code")
    parser.add_argument("--output", default="voice_test.wav", help="Output filename")
    parser.add_argument("--no-play", action="store_true", help="Disable playback")
    parser.add_argument("--player", help="Explicit player choice")

    args = parser.parse_args()
    
    tts = TTS(auto_download=True)
    style = tts.get_voice_style(voice_name=args.voice)
    
    wav, duration = tts.synthesize(
        text=args.text,
        lang=args.lang,
        voice_style=style,
        total_steps=args.steps,
        speed=args.speed
    )
    
    tts.save_audio(wav, args.output)
    print(f"Saved to {args.output} (Duration: {duration:.2f}s)")

if __name__ == "__main__":
    main()
