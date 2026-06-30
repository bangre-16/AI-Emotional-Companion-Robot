# emotion_react.py
import time
import requests

from modules.ollama_module import get_response
from modules.tts_module import speak
from modules.stt_module import listen_once

# URL of your backend emotion API (Pi backend)
BACKEND_URL = "http://10.87.245.7:5000/predict_camera"  # change if IP changes

# Cooldown so it doesn't trigger every second when sad
COOLDOWN_SECONDS = 30
LAST_SAD_TS = 0


def talk_and_listen_for_reply():
    """
    1) Robot says a comforting line (Ollama).
    2) Then listens once on the mic.
    3) Replies again using Ollama.
    All output goes through TTS -> Bluetooth speaker.
    """

    # --- Step 1: first comforting sentence ---
    first = get_response(
        "The person in front of you looks sad. "
        "Say one short, warm, comforting sentence in simple English."
    )
    first_text = first.get("text") or "You are not alone, I am here with you."
    print("Robot (first):", first_text)
    speak(first_text)  # goes to your Bluetooth speaker via tts_module


    # --- Step 2: listen to the patient once ---
    print("Listening for patient's reply...")
    user_text = listen_once()
    if not user_text:
        print("No speech detected after comforting line.")
        return

    print("User said:", user_text)

    # --- Step 3: respond to what they said ---
    follow = get_response(
        f"The user said: '{user_text}'. "
        "Reply in one or two short comforting sentences in simple English."
    )
    follow_text = follow.get("text") or "I am still here with you, you matter a lot."
    print("Robot (reply):", follow_text)
    speak(follow_text)


def main_loop():
    global LAST_SAD_TS
    print("Emotion reaction loop running... Ctrl+C to stop")

    while True:
        # 1) Ask backend for current emotion from camera
        try:
            r = requests.get(BACKEND_URL, timeout=5)
            data = r.json()
        except Exception as e:
            print("Error calling backend:", e)
            time.sleep(2)
            continue

        emotion = data.get("emotion")
        conf = data.get("confidence")
        print("Detected:", emotion, conf)

        now = time.time()

        # 2) Trigger only on "sad", with cooldown
        if emotion == "sad" and (now - LAST_SAD_TS) > COOLDOWN_SECONDS:
            LAST_SAD_TS = now
            talk_and_listen_for_reply()

        time.sleep(1)


if __name__ == "__main__":
    main_loop()
