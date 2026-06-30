# test_mic_ollama_tts.py
from modules.stt_module import listen_once
from modules.ollama_module import get_response
from modules.tts_module import speak

print("Mic ? Ollama ? Speaker test. Ctrl+C to stop.")

try:
    while True:
        print("??  Speak now...")
        user_text = listen_once()
        if not user_text:
            print("No speech detected.")
            continue

        print("You said:", user_text)

        reply = get_response(
            f"The user said: '{user_text}'. "
            "Reply in one or two short comforting sentences in simple English."
        )
        print("Ollama:", reply["text"])
        speak(reply["text"])

except KeyboardInterrupt:
    print("Exiting.")
