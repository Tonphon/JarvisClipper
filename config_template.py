import os
import sounddevice as sd

# General Settings
FRAME_RATE = 30
SAMPLE_RATE = 44100
CHANNELS = 2
DURATION = 5  # Duration for the recording buffer (in seconds)

# Output Directories (Users should replace "your/path/here" with actual paths)
OUTPUT_DIR = "your/path/here"
VIDEO_TEMP_DIR = "your/path/here"

# Check if paths are still placeholders
if OUTPUT_DIR == "your/path/here" or VIDEO_TEMP_DIR == "your/path/here":
    print("WARNING: Please update OUTPUT_DIR and VIDEO_TEMP_DIR in config.py")

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(VIDEO_TEMP_DIR, exist_ok=True)

# Auto-detect Stereo Mix
def find_stereo_mix():
    devices = sd.query_devices()
    hostapis = sd.query_hostapis()
    for i, device in enumerate(devices):
        if "Stereo Mix" in device["name"]:
            hostapi_name = hostapis[device["hostapi"]]["name"]
            return i if "MME" in hostapi_name else None
    return None

# Allow users to manually set DEVICE_INDEX; otherwise, auto-detect
if DEVICE_INDEX is None:
    DEVICE_INDEX = find_stereo_mix()

if DEVICE_INDEX is None:
    print("Error: Stereo Mix not found. Please enable it in sound settings.")
    exit()

print(f"Using Stereo Mix (Device Index: {DEVICE_INDEX})")
