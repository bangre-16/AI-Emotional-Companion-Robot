import time
from modules.dfplayer_module import play_track, play_audio, play_tts

print("Testing DFPlayer functions...\n")

print("? Test 1: play_track(1)")
play_track(1)
time.sleep(1)

print("? Test 2: play_audio('test.mp3')")
play_audio("test.mp3")  # Must exist inside Robot/audio/
time.sleep(1)

print("? Test 3: TTS: Hello human")
play_tts("Hello human! I am speaking from Raspberry Pi.")
time.sleep(1)

print("\n? DFPlayer test finished.")
