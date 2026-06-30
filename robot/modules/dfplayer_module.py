"""
Simple DFPlayer module (fallback to software playback).
Provides:
 - play_track(track_num)   : play audio/NN.mp3 (or send DFPlayer serial cmd if configured)
 - play_audio(filename)    : play specific file under audio/
 - play_tts(text)          : speak dynamic text via tts_module.speak()
"""

import os, subprocess, time
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Optional: if you have a physical DFPlayer connected over serial,
# set DFPLAYER_PORT in .env to the serial device (e.g. /dev/ttyS0).
DFPLAYER_PORT = os.getenv("DFPLAYER_PORT", "")

_serial = None
if DFPLAYER_PORT:
    try:
        import serial
        _serial = serial.Serial(DFPLAYER_PORT, int(os.getenv("DFPLAYER_BAUD", "9600")), timeout=1)
        print("[dfplayer_module] Serial opened:", DFPLAYER_PORT)
    except Exception as e:
        print("[dfplayer_module] Could not open serial, falling back to file playback:", e)
        _serial = None

def _play_file(path):
    path = os.path.abspath(path)
    if not os.path.exists(path):
        print("[dfplayer_module] file not found:", path)
        return
    # use mpg123 (installed earlier)
    try:
        subprocess.run(["mpg123", "-q", path], check=False)
    except Exception as e:
        print("[dfplayer_module] mpg123 playback failed:", e)

def play_track(track_num: int):
    """If DFPlayer hardware present, send play command; else play audio/<NN>.mp3"""
    if _serial:
        try:
            # DFPlayer basic protocol for "play track" (common) - may vary by module
            cmd = bytearray([0x7E, 0xFF, 0x06, 0x03, 0x00, 0x00, track_num & 0xFF, 0xEF])
            _serial.write(cmd)
            time.sleep(0.2)
            return
        except Exception as e:
            print("[dfplayer_module] DF serial play failed:", e)

    filename = os.path.join(os.path.dirname(__file__), "..", "audio", f"{track_num:02d}.mp3")
    _play_file(filename)

def play_audio(filename: str):
    """Play a named audio file from project audio/ or absolute path."""
    if not os.path.isabs(filename):
        filename = os.path.join(os.path.dirname(__file__), "..", "audio", filename)
    _play_file(filename)

# TTS: prefer your tts_module.speak() if available; otherwise fallback to gTTS quick flow.
def play_tts(text: str):
    try:
        # prefer your tts_module (gTTS wrapper)
        from modules.tts_module import speak as tts_speak
        return tts_speak(text)
    except Exception:
        # fallback: quick gTTS -> mpg123
        try:
            from gtts import gTTS
            tmp = "/tmp/robot_tts.mp3"
            gTTS(text=text, lang="en").save(tmp)
            _play_file(tmp)
            try:
                os.remove(tmp)
            except Exception:
                pass
        except Exception as e:
            print("[dfplayer_module] play_tts failed:", e)
            print(">>>", text)
