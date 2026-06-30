# modules/rtc_module.py
from datetime import datetime
import os
from dotenv import load_dotenv

ROOT = os.path.dirname(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(ROOT, ".env"))

MEDICINE_TIME = os.getenv("MEDICINE_TIME", "10:43")

# If you have a real RTC (DS3231) library, replace the get_time() implementation
def get_time():
    # returns datetime object - prefer real RTC reads if you have RTC hardware
    return datetime.now()

def is_medicine_time(now):
    return now.strftime("%H:%M") == MEDICINE_TIME

def check_medicine_taken():
    # Integrate with touch sensor or last-known flag
    # This function must be managed by main.py which sets the flag
    return False
