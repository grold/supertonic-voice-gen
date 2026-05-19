import argparse
import sys
from supertonic import TTS
import os
import subprocess
import shutil
import socket
import http.server
import socketserver
import threading
import pychromecast

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

def start_temporary_server(file_path, port=8000):
    # handler for serving just the directory of the file
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd

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
    
    # Validation
    if args.speed <= 0:
        print("Error: Speed must be positive.")
        sys.exit(1)
    if args.steps < 1:
        print("Error: Steps must be at least 1.")
        sys.exit(1)

    try:
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
    except Exception as e:
        print(f"Error during synthesis: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
