# modules/tts_module.py
# gTTS -> MP3 -> play using system audio (mpg123), so it goes to Bluetooth speaker

import os
import time
import subprocess
from gtts import gTTS

TTS_TEMP_FILE = "/tmp/robot_tts.mp3"

def speak(text: str):
    """Convert text -> speech -> play via system audio (mpg123)."""
    try:
        print("[TTS] Generating speech...")
        tts = gTTS(text=text, lang="en")
        tts.save(TTS_TEMP_FILE)

        print("[TTS] Playing via mpg123...")
        # This uses the DEFAULT audio sink (you already set Bluetooth as default)
        subprocess.run(["mpg123", "-q", TTS_TEMP_FILE], check=False)

        # small delay is optional
        time.sleep(0.5)

    except Exception as e:
        print("[TTS ERROR]:", e)
        print(">>", text)  # fallback: at least print the text
    finally:
        try:
            if os.path.exists(TTS_TEMP_FILE):
                os.remove(TTS_TEMP_FILE)
        except Exception:
            pass
