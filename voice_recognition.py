import speech_recognition as sr
import recorder # type: ignore
import sys
import threading

recognizer = sr.Recognizer()
mic = sr.Microphone()
debug_mode = True

def listen_for_command():
    """ Continuously listens for 'Jarvis' and then waits for a command. """
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            if debug_mode:
                command = input("Type command: ")
            else:
                print("Listening for 'Jarvis'...")
                try:
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio).lower()
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    print("Error connecting to speech recognition service.")
                    continue

            print(f"Command received: {command}")
            if "Jarvis" in command:
                print("Jarvis activated. Waiting for command...")
                execute_command(source)

def execute_command(source):
    """ Listens for the next command. """
    if debug_mode:
        command = input("Type next command: ")
    else:
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            return
        except sr.RequestError:
            print("Error processing command.")
            return

    if "clip that" in command:
        recorder.save_clip()
    elif "offline" in command:
        print("Shutting down")
        sys.exit()

def start_listening():
    """ Starts the voice recognition in a separate thread. """
    thread = threading.Thread(target=listen_for_command, daemon=True)
    thread.start()
