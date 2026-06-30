# timed_gsm_alert.py
import time
from datetime import datetime
from modules.gsm_module import send_alert
import os
from dotenv import load_dotenv

ROOT = os.path.dirname(__file__)
load_dotenv(os.path.join(ROOT, ".env"))

# Time in HH:MM 24-hour format (from .env or hardcoded)
ALERT_TIME = os.getenv("ALERT_TIME", "10:44")  # change or set in .env

MESSAGE_TEXT = os.getenv(
    "ALERT_MESSAGE",
    "This is a reminder from the robot: the patient did not take the medicine."
)

def main():
    print(f"[Timed GSM] Waiting for time {ALERT_TIME} to send SMS...")
    sent_today = False

    while True:
        now = datetime.now()
        now_hm = now.strftime("%H:%M")

        # Reset flag at midnight
        if now_hm == "00:00":
            sent_today = False

        # When time matches and not yet sent today -> send once
        if now_hm == ALERT_TIME and not sent_today:
            print(f"[Timed GSM] Time matched ({now_hm}). Sending SMS...")
            ok = send_alert(MESSAGE_TEXT)
            if ok:
                print("[Timed GSM] SMS sent successfully.")
            else:
                print("[Timed GSM] SMS failed (check Twilio / config).")
            sent_today = True

            # Sleep 61s so we don't send multiple times in the same minute
            time.sleep(61)
            continue

        time.sleep(1)

if __name__ == "__main__":
    main()
