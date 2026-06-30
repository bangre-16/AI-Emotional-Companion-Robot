import time
from modules.rtc_module import get_time, is_medicine_time

print("Testing Medicine Reminder... (Ctrl+C to exit)")
print("Waiting for configured MEDICINE_TIME...")

try:
    while True:
        now = get_time()
        time_str = now.strftime("%H:%M:%S")

        if is_medicine_time(now):
            print(f"{time_str} ?? IT'S MEDICINE TIME!")
        else:
            print(f"{time_str} - Not yet")

        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopped.")
