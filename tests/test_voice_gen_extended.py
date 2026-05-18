import subprocess
import os
import sys
import pytest

def test_speed_parameter():
    test_out = "test_speed.wav"
    if os.path.exists(test_out): os.remove(test_out)
    
    # Test with fast speed
    result = subprocess.run([
        sys.executable, "scripts/generate_voice.py", 
        "Speed test", "--output", test_out, "--no-play", "--speed", "2.0"
    ], capture_output=True, text=True)
    assert result.returncode == 0
    assert os.path.exists(test_out)
    
    # Check output for duration (should be short)
    # Saved to test_speed.wav (Duration: 0.XXs)
    assert "Duration:" in result.stdout

def test_steps_parameter():
    test_out = "test_steps.wav"
    if os.path.exists(test_out): os.remove(test_out)
    
    # Test with high steps
    result = subprocess.run([
        sys.executable, "scripts/generate_voice.py", 
        "Steps test", "--output", test_out, "--no-play", "--steps", "12"
    ], capture_output=True, text=True)
    assert result.returncode == 0
    assert os.path.exists(test_out)

def test_voice_parameter():
    test_out = "test_voice.wav"
    if os.path.exists(test_out): os.remove(test_out)
    
    # Test with F1 voice
    result = subprocess.run([
        sys.executable, "scripts/generate_voice.py", 
        "Voice test", "--output", test_out, "--no-play", "--voice", "F1"
    ], capture_output=True, text=True)
    assert result.returncode == 0
    assert os.path.exists(test_out)

def test_empty_text_fails():
    # Argparse should fail if positional 'text' is missing
    result = subprocess.run([
        sys.executable, "scripts/generate_voice.py", "--no-play"
    ], capture_output=True, text=True)
    assert result.returncode != 0

def test_invalid_speed_fails():
    result = subprocess.run([
        sys.executable, "scripts/generate_voice.py", "test", "--speed", "0", "--no-play"
    ], capture_output=True, text=True)
    assert result.returncode != 0
    assert "Error: Speed must be positive." in result.stdout

def test_invalid_steps_fails():
    result = subprocess.run([
        sys.executable, "scripts/generate_voice.py", "test", "--steps", "0", "--no-play"
    ], capture_output=True, text=True)
    assert result.returncode != 0
    assert "Error: Steps must be at least 1." in result.stdout
