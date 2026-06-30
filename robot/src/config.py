# modules/config.py
import os
from dotenv import load_dotenv
ROOT = os.path.dirname(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(ROOT, ".env"))

OLLAMA_SERVER = os.getenv("OLLAMA_SERVER")
MEDICINE_TIME = os.getenv("MEDICINE_TIME", "05:14")
REMINDER_INTERVAL = int(os.getenv("REMINDER_INTERVAL", "300"))
