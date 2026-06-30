from modules.dfplayer_module import play_track
import time

print("Testing DFPlayer: playing track 1 then 2...")

print("Play track 1 (should be 0001.mp3)")
play_track(1)
time.sleep(3)

print("Play track 2 (should be 0002.mp3)")
play_track(2)
time.sleep(3)

print("Done.")
