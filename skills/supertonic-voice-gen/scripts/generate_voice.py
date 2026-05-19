# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pychromecast>=14.0.10",
#     "supertonic>=1.3.1",
# ]
# ///

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
import time

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        return s.getsockname()[0]
    except Exception:
        return socket.gethostbyname(socket.gethostname())
    finally:
        s.close()

class LoggingCORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    def log_message(self, format, *args):
        pass

def start_temporary_server(port=8080):
    handler = LoggingCORSHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    try:
        httpd = socketserver.TCPServer(("", port), handler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        return httpd
    except Exception as e:
        print(f"DEBUG: Failed to start server on port {port}: {e}")
        return None

def play_on_chromecast(file_path, friendly_name, local_ip, port, volume=None):
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[friendly_name])
    if not chromecasts:
        return False
    
    cast = chromecasts[0]
    cast.wait()
    
    if volume is not None:
        print(f"Setting Chromecast volume to {volume}%")
        cast.set_volume(volume / 100.0)

    if cast.app_id != pychromecast.APP_MEDIA_RECEIVER:
        cast.start_app(pychromecast.APP_MEDIA_RECEIVER)
        time.sleep(2)
        cast.wait()

    mc = cast.media_controller
    url = f"http://{local_ip}:{port}/{file_path}"
    mc.play_media(url, 'audio/mp3')
    
    start_wait = time.time()
    while time.time() - start_wait < 5:
        time.sleep(1)
        if mc.status.player_state in ['PLAYING', 'BUFFERING']:
            break

    while mc.status.player_state in ['PLAYING', 'BUFFERING'] and time.time() - start_wait < 120:
        time.sleep(1)
        if mc.status.player_state == 'IDLE':
            break

    return True

def play_audio(file_path, player_override=None, volume=None):
    players = [player_override] if player_override else ["mpv", "vlc", "ffplay"]
    for p in players:
        if p and shutil.which(p):
            cmd = [p, file_path]
            
            if p == "mpv":
                cmd.append("--no-video")
                if volume is not None:
                    cmd.append(f"--volume={volume}")
            elif p == "vlc":
                cmd.extend(["--intf", "dummy", "--play-and-exit"])
                if volume is not None:
                    cmd.append(f"--gain={volume/100.0}")
            elif p == "ffplay":
                cmd.extend(["-nodisp", "-autoexit"])
                if volume is not None:
                    cmd.extend(["-volume", str(volume)])

            print(f"Playing locally via {p}...")
            subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
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
    parser.add_argument("--cast", default="Bedroom speaker", help="Chromecast device name")
    parser.add_argument("--no-cast", action="store_true", help="Disable Chromecast playback")
    parser.add_argument("--volume", type=int, help="Volume level (0-100)")

    args = parser.parse_args()
    
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
        d_val = duration.item() if hasattr(duration, 'item') else float(duration)
        print(f"Saved to {args.output} (Duration: {d_val:.2f}s)")

    except Exception as e:
        print(f"Error during synthesis: {e}")
        sys.exit(1)

    if not args.no_play:
        played_remotely = False
        if not args.no_cast:
            try:
                mp3_output = args.output.replace('.wav', '.mp3')
                if not mp3_output.endswith('.mp3'): mp3_output += '.mp3'
                
                subprocess.run([
                    "ffmpeg", "-y", "-i", args.output, 
                    "-codec:a", "libmp3lame", "-qscale:a", "2", 
                    mp3_output
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                local_ip = get_local_ip()
                port = 8080
                httpd = start_temporary_server(port)
                if httpd:
                    if play_on_chromecast(mp3_output, args.cast, local_ip, port, volume=args.volume):
                        played_remotely = True
                    else:
                        print(f"Warning: Chromecast '{args.cast}' failed to play.")
                    httpd.shutdown()
                else:
                    print("Warning: Could not start local server.")
            except Exception as cast_err:
                print(f"Warning: Chromecast playback failed: {cast_err}")

        if not played_remotely:
            if not play_audio(args.output, args.player, volume=args.volume):
                print("Warning: No audio player found.")

if __name__ == "__main__":
    main()
