# main.py
import threading
import time
import traceback
import os
from datetime import datetime
from dotenv import load_dotenv
import requests

# Load environment vars from Robot/.env
ROOT = os.path.dirname(__file__)
load_dotenv(os.path.join(ROOT, ".env"))

# Local modules
from modules import (
    ollama_module,
    dfplayer_module,
    gsm_module,
    touch_sensor_module,
    rtc_module,
)
from modules.tts_module import speak
from modules.stt_module import listen_once          # <--- STT import for mic input

# ---------------------------------------------------------------------
# CONFIG (env overrides available)
# ---------------------------------------------------------------------
MEDICINE_INTERVAL = int(os.getenv("REMINDER_INTERVAL", "300"))  # seconds (default 5 minutes)
MEDICINE_TIME = os.getenv("MEDICINE_TIME", "14:00")  # "HH:MM" 24-hour format
# Default to local Pi emotion backend. You can override EMOTION_API_URL in .env if required.
EMOTION_API_URL = os.getenv("EMOTION_API_URL", "http://127.0.0.1:5000/predict_camera").rstrip("/")
CARETAKER = os.getenv("TWILIO_TO_NUMBER", "")

# Internal state
_patient_took_medicine = False
_state_lock = threading.Lock()
_last_emotion_speak_ts = 0
EMOTION_COOLDOWN = int(os.getenv("EMOTION_COOLDOWN_SECONDS", "30"))  # seconds between spoken messages

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------
def speak_text(text: str):
    """
    Speak text via tts_module.speak (gTTS/mpg123). On failure, print fallback.
    """
    try:
        speak(text)
    except Exception as e:
        print("[Main] speak_text error:", e)
        print("[Main] (fallback) ->", text)


def handle_gpt_for_emotion(emotion: str) -> str:
    """
    Ask Ollama for a warm, short reply based on detected emotion.
    """
    prompt = (
        f"The patient seems {emotion}. "
        "Reply in 1-2 warm, simple English sentences that validate their feelings "
        "and suggest one tiny helpful action (take a deep breath, sip water, or rest briefly)."
    )
    res = ollama_module.get_response(prompt)
    if isinstance(res, dict):
        text = res.get("text") or ""
    else:
        text = str(res)
    if not text.strip():
        text = "hey,isee you're sad.You are not alone,Take a slow deep breath.I'm here with you."
    return text


def fetch_remote_emotion(timeout=3):
    """
    Call the emotion backend /predict_camera and return emotion string.
    Returns 'neutral' on failure.
    Expected JSON: { "emotion": "sad", "confidence": 0.92, ... }
    """
    try:
        r = requests.get(EMOTION_API_URL, timeout=timeout)
        if r.status_code != 200:
            print(f"[Main] Emotion API returned {r.status_code}")
            return "neutral"
        data = r.json()
        emotion = data.get("emotion", "neutral")
        conf = data.get("confidence", None)
        print(f"[Main] Emotion API -> emotion={emotion}, confidence={conf}")
        return emotion
    except Exception as e:
        # keep logs readable in long-running service
        print("[Main] Emotion fetch failed:", e)
        return "neutral"

# ---------------------------------------------------------------------
# Medicine reminder loop
# ---------------------------------------------------------------------
def medicine_reminder_loop():
    """
    Monitor medicine time, play reminders, detect touch, and send alerts if missed.
    Uses: rtc_module, touch_sensor_module, dfplayer_module, gsm_module
    """
    global _patient_took_medicine

    touch_sensor_module.setup_touch_sensor()
    print(f"[Main] Medicine reminder started (MEDICINE_TIME={MEDICINE_TIME})")

    try:
        while True:
            now = rtc_module.get_time()

            try:
                if rtc_module.is_medicine_time(now) and not _patient_took_medicine:
                    print("[Main] It's medicine time:", now.strftime("%H:%M"))

                    # First reminder (ensure this track number exists on DFPlayer)
                    dfplayer_module.play_track(3)
                    speak_text("It's time to take your medicine. Please take your pills.")
                    start = time.time()

                    # Wait MEDICINE_INTERVAL seconds looking for touch confirmation
                    while time.time() - start < MEDICINE_INTERVAL:
                        if touch_sensor_module.is_touched():
                            with _state_lock:
                                _patient_took_medicine = True
                            dfplayer_module.play_track(5)
                            speak_text("Good job. I see you took your medicine.")
                            print("[Main] Medicine taken (first window).")
                            break
                        time.sleep(1)

                    # Second reminder if still not taken
                    if not _patient_took_medicine:
                        dfplayer_module.play_track(4)
                        speak_text(
                            "You haven't taken your medicine yet. "
                            "Please take it now; it's important for your health."
                        )
                        start = time.time()

                        while time.time() - start < MEDICINE_INTERVAL:
                            if touch_sensor_module.is_touched():
                                with _state_lock:
                                    _patient_took_medicine = True
                                dfplayer_module.play_track(5)
                                speak_text("Thank you — I see you took the tablet.")
                                print("[Main] Medicine taken (second window).")
                                break
                            time.sleep(1)

                        # Still not taken -> alert caretaker via GSM/Twilio (if configured)
                        if not _patient_took_medicine and CARETAKER:
                            msg = f"Patient missed medicine twice at {now.strftime('%H:%M')}."
                            print("[Main] Sending alert:", msg)
                            try:
                                gsm_module.send_alert(msg)
                            except Exception as e:
                                print("[Main] Failed to send alert:", e)

                else:
                    # Reset _patient_took_medicine when time moves on (so next day works)
                    if _patient_took_medicine and now.strftime("%H:%M") != MEDICINE_TIME:
                        with _state_lock:
                            _patient_took_medicine = False

            except Exception:
                traceback.print_exc()

            time.sleep(20)

    finally:
        try:
            touch_sensor_module.cleanup()
        except Exception:
            pass

# ---------------------------------------------------------------------
# Emotion monitoring loop
# ---------------------------------------------------------------------
def emotion_monitor_loop():
    """
    Periodically check emotion from backend and speak a short supportive
    reply when patient seems low (sad/depressed/angry), using cooldown.
    """
    global _last_emotion_speak_ts
    print("[Main] Emotion monitor started.")

    try:
        while True:
            try:
                emotion = fetch_remote_emotion()

                if emotion in ("sad", "depressed", "angry"):
                    now_ts = time.time()
                    if now_ts - _last_emotion_speak_ts > EMOTION_COOLDOWN:
                        reply = handle_gpt_for_emotion(emotion)
                        print("[Main] Emotional support reply:", reply)
                        speak_text(reply)
                        _last_emotion_speak_ts = now_ts

                time.sleep(10)

            except Exception:
                traceback.print_exc()
                time.sleep(5)
    except KeyboardInterrupt:
        pass

# ---------------------------------------------------------------------
# Voice interaction loop (MIC -> OLLAMA -> SPEAKER)
# ---------------------------------------------------------------------
def voice_interaction_loop():
    """
    Listen from microphone once, send text to Ollama, speak the reply.
    Uses modules.stt_module.listen_once and ollama_module.get_response.
    This runs as a background thread so the robot can also do medicine/emotion tasks.
    """
    print("[Main] Voice interaction started.")
    while True:
        try:
            print("[Main] Listening for user speech...")
            user_text = listen_once()   # blocks until speech or timeout

            if not user_text:
                # no speech recognized
                continue

            print("[Main] User said:", user_text)
            reply = ollama_module.get_response(
                f"The user said: '{user_text}'. Reply in one or two short comforting sentences in simple English."
            )

            bot_text = reply.get("text") if isinstance(reply, dict) else str(reply)
            if not bot_text:
                bot_text = "I'm here with you. Take a slow breath."
            print("[Main] Ollama reply:", bot_text)
            speak_text(bot_text)

        except Exception as e:
            print("[Main] Voice loop error:", e)
            # keep it alive and try again
            time.sleep(1)

# ---------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------
if __name__ == "__main__":
    print("[Main] Robot starting.")

    # Startup greeting
    try:
        dfplayer_module.play_track(1)
    except Exception as e:
        print("[Main] greeting DFPlayer failed:", e)

    try:
        speak_text("Hello, I am here with you.")
    except Exception as e:
        print("[Main] greeting TTS failed:", e)

    # Start background threads
    t_med = threading.Thread(target=medicine_reminder_loop, daemon=True)
    t_emo = threading.Thread(target=emotion_monitor_loop, daemon=True)
    t_voice = threading.Thread(target=voice_interaction_loop, daemon=True)

    t_med.start()
    t_emo.start()
    t_voice.start()

    # Main loop keep-alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("[Main] Exiting.")
