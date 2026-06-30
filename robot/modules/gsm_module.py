# modules/gsm_module.py
import os
from dotenv import load_dotenv

ROOT = os.path.dirname(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(ROOT, ".env"))

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM_NUMBER")
TWILIO_TO = os.getenv("TWILIO_TO_NUMBER")

def send_alert(message_text: str):
    if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_FROM and TWILIO_TO):
        print("[GSM] Twilio not configured, skipping SMS. Message would be:", message_text)
        return False
    try:
        from twilio.rest import Client
    except Exception as e:
        print("[GSM] twilio package not installed:", e)
        return False
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        msg = client.messages.create(from_=TWILIO_FROM, to=TWILIO_TO, body=message_text)
        print("[GSM] Sent SMS SID:", msg.sid)
        return True
    except Exception as e:
        print("[GSM] Twilio send error:", e)
        return False
