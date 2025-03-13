import threading
import recorder
import voice_recognition

if __name__ == "__main__":
    print("Starting...")
    threading.Thread(target=recorder.start_recording, daemon=True).start()
    voice_recognition.listen_for_command()
