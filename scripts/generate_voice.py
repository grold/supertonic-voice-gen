import argparse
import sys
from supertonic import TTS
import os
import subprocess
import shutil

def play_audio(file_path, player_override=None):
    players = [player_override] if player_override else ["mpv", "vlc", "ffplay"]
    for p in players:
        if p and shutil.which(p):
            # Background the process
            subprocess.Popen([p, file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
    return False

def main():
    parser = argparse.ArgumentParser(description="Supertonic Voice Generator")
    parser.add_argument("text", help="Text to synthesize")
    parser.add_argument("--voice", default="M1", help="Voice preset")
    parser.add_argument("--speed", type=float, default=1.0, help="Speed multiplier")
    parser.add_argument("--steps", type=int, default=8, help="Inference steps")
    parser.add_argument("--lang", default="en", help="Language code")
    parser.add_argument("--output", default="voice_test.wav", help="Output filename")
    parser.add_argument("--no-play", action="store_true", help="Disable playback")
    parser.add_argument("--play", action="store_false", dest="no_play", help="Enable playback (default)")
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
    # duration is a numpy array scalar, use item() to get python float
    d_val = duration.item() if hasattr(duration, 'item') else float(duration)
    print(f"Saved to {args.output} (Duration: {d_val:.2f}s)")

    if not args.no_play:
        if not play_audio(args.output, args.player):
            print("Warning: No audio player found.")

if __name__ == "__main__":
    main()
