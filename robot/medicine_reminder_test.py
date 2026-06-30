import time
from datetime import timedelta

from modules.rtc_module import get_time, is_medicine_time
from modules.dfplayer_module import play_track  # <- use play_track now

# CONFIG
FORGET_DELAY_MINUTES = 5  # after how long to play "forgot" warning

print("Medicine reminder test running... (Ctrl+C to stop)")

reminder_played = False
forget_warning_played = False
forget_deadline = None  # time after which we consider it 'forgotten'

try:
    while True:
        now = get_time()
        now_str = now.strftime("%H:%M:%S")
        print("Now:", now_str)

        # 1) When it's medicine time -> play 0001.mp3 once (track 1)
        if is_medicine_time(now) and not reminder_played:
            print(">>> MEDICINE TIME: playing track 1 (0001.mp3)")
            play_track(1)  # DFPlayer plays 0001.mp3
            reminder_played = True
            forget_deadline = now + timedelta(minutes=FORGET_DELAY_MINUTES)

        # 2) If medicine time passed and still no confirmation -> play 0002.mp3 once (track 2)
        if (
            reminder_played
            and not forget_warning_played
            and forget_deadline is not None
            and now >= forget_deadline
        ):
            print(">>> MEDICINE POSSIBLY MISSED: playing track 2 (0002.mp3)")
            play_track(2)  # DFPlayer plays 0002.mp3
            forget_warning_played = True

        # 3) Simple daily reset at midnight (so next day works again)
        if now.hour == 0 and now.minute == 0 and now.second < 5:
            reminder_played = False
            forget_warning_played = False
            forget_deadline = None
            print("New day: reminder state reset.")

        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopped medicine reminder test.")
