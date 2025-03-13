# JarvisClipper

## Overview
JarvisClipper is a real-time AI-powered assistant that continuously records your screen and system audio. With voice commands, you can instantly save the last few seconds of your screen and system audio.

## Features
- "Jarvis, clip that" - Saves the last few seconds of screen and audio.
- "Jarvis, offline" - Turns off the assistant.
- Real-time screen recording with circular buffering.
- Records system audio with automatic Stereo Mix detection.
- Multi-threaded for smooth performance.
- Configurable settings for FPS, duration, and output paths.

## Installation

### Step 1: Install Dependencies
Ensure you have Python 3.8+ installed, then run:
```
pip install opencv-python numpy mss sounddevice scipy wave speechrecognition ffmpeg-python
```

### Step 2: Enable Stereo Mix (Windows Only)
1. Right-click on the sound icon in the taskbar and select "Sounds".
2. Go to the "Recording" tab.
3. Right-click and enable "Stereo Mix".
4. Set it as the default recording device.

## Configuration

### Step 1: Rename `config_template.py` to `config.py`

### Step 2: Edit `config.py`
Update the output directories and verify the device index:
```python
OUTPUT_DIR = "your/output/path/here"
VIDEO_TEMP_DIR = "your/output/path/here"
DEVICE_INDEX = None  # Set your Stereo Mix device index if needed
```

## Usage

### Start the assistant
```
python main.py
```

### Voice Commands
| Command            | Action |
|--------------------|----------------------------------|
| "Jarvis, clip that" | Saves the last few seconds of screen and audio |
| "Jarvis, offline" | Shuts down the assistant |

## Project Structure
```
JarvisClipper/
│── main.py              # Starts the assistant
│── recorder.py          # Handles screen/audio recording
│── voice_recognition.py # Listens for voice commands
│── config.py            # Stores user configuration (ignored in Git)
│── config_template.py   # Template for configuration
│── recordings/          # Saves the clipped videos
│── README.md            # Project documentation
```
