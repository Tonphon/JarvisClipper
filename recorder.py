import cv2
import numpy as np
import pyautogui
import sounddevice as sd
import wave
import os
import time
import threading
import ffmpeg
from collections import deque
import config  # type: ignore

FRAME_RATE = config.FRAME_RATE
SAMPLE_RATE = config.SAMPLE_RATE
CHANNELS = config.CHANNELS
DURATION = config.DURATION
OUTPUT_DIR = config.OUTPUT_DIR
VIDEO_TEMP_DIR = config.VIDEO_TEMP_DIR
DEVICE_INDEX = config.DEVICE_INDEX

video_buffer = deque(maxlen=FRAME_RATE * DURATION)
audio_buffer = deque(maxlen=SAMPLE_RATE * DURATION)

screen_width, screen_height = pyautogui.size()
fourcc = cv2.VideoWriter_fourcc(*"XVID")

print(f"Using Stereo Mix (Device Index: {DEVICE_INDEX})")

def record_audio():
    """ Continuously records system audio into a buffer. """
    def callback(indata, frames, time, status):
        if status:
            print(status)
        audio_buffer.append(indata.copy())

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, device=DEVICE_INDEX, callback=callback, dtype="int16"):
        while True:
            time.sleep(0.1)

def record_screen():
    """ Continuously records screen frames into a buffer. """
    while True:
        frame = pyautogui.screenshot()
        frame = np.array(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        video_buffer.append(frame)
        time.sleep(1 / FRAME_RATE)

def save_clip():
    """ Saves the last 1 minute of screen recording and audio as a video file. """
    print("Saving clip...")

    video_file = os.path.join(OUTPUT_DIR, "screen_recording.avi")
    audio_file = os.path.join(OUTPUT_DIR, "system_audio.wav")
    final_output = os.path.join(OUTPUT_DIR, "final_clip.mp4")

    if not video_buffer or not audio_buffer:
        print("Error: No recording data available. Skipping save.")
        return

    video_frames = list(video_buffer)
    audio_data = np.concatenate(list(audio_buffer), axis=0)

    print(f"Saving {len(video_frames)} frames to {video_file}...")
    video_writer = cv2.VideoWriter(video_file, fourcc, FRAME_RATE, (screen_width, screen_height))
    for frame in video_frames:
        video_writer.write(frame)
    video_writer.release()

    print(f"Saving audio ({len(audio_data)} samples) to {audio_file}...")
    with wave.open(audio_file, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())

    if not os.path.exists(video_file) or not os.path.exists(audio_file):
        print("Error: Video or audio file not found. Merge skipped.")
        return

    print("Merging video and audio...")
    video_input = ffmpeg.input(video_file)
    audio_input = ffmpeg.input(audio_file)
    ffmpeg.output(video_input, audio_input, final_output, vcodec='libx264', acodec='aac', r=FRAME_RATE).run(overwrite_output=True)

    print(f"Clip saved: {final_output}")

def start_recording():
    """ Starts the recording threads. """
    threading.Thread(target=record_audio, daemon=True).start()
    threading.Thread(target=record_screen, daemon=True).start()
