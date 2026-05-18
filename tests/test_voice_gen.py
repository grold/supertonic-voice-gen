import subprocess
import os

def test_driver_runs():
    # Ensure script exists and can be called with --help
    result = subprocess.run(["python3", "scripts/generate_voice.py", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "usage: generate_voice.py" in result.stdout
