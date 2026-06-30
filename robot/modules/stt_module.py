# modules/stt_module.py
import speech_recognition as sr

_recognizer = sr.Recognizer()

def listen_once(timeout=5, phrase_time_limit=8):
    """
    Listen from default microphone once and return recognized text
    (or None if nothing understood).
    Uses Google's online speech recognition.
    """
    with sr.Microphone() as source:
        print("??  Speak now (listening)...")
        _recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = _recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("?  No speech detected (timeout).")
            return None

    try:
        text = _recognizer.recognize_google(audio)
        print("?? Recognized:", text)
        return text
    except sr.UnknownValueError:
        print("? Could not understand audio.")
        return None
    except sr.RequestError as e:
        print("? Speech recognition request failed:", e)
        return None
