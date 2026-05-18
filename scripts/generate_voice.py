import argparse
import sys

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
    print(f"Synthesizing: {args.text}")

if __name__ == "__main__":
    main()
