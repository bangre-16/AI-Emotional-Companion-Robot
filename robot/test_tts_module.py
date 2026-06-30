# test_tts_module.py

from modules.ollama_module import get_response
from modules.tts_module import speak

reply = get_response("Say one short comforting sentence for someone feeling lonely.")
print("GPT Reply:", reply)

speak(reply["text"])
