import subprocess
import os
import sys

def test_driver_runs():
    # Ensure script exists and can be called with --help
    result = subprocess.run([sys.executable, "scripts/generate_voice.py", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "usage: generate_voice.py" in result.stdout

def test_wav_generation():
    test_out = "test_output.wav"
    if os.path.exists(test_out): os.remove(test_out)
    
    # Mocking or using a tiny text for speed
    result = subprocess.run([
        sys.executable, "scripts/generate_voice.py", 
        "Hello", "--output", test_out, "--no-play"
    ], capture_output=True, text=True)
    
    assert os.path.exists(test_out)
    assert os.path.getsize(test_out) > 0
