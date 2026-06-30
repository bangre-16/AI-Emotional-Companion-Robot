#!/bin/bash
cd "$(dirname "$0")"
source .venv/bin/activate
mkdir -p logs
echo "Checking OLLAMA server from .env..."

python3 - <<'PY'
import os, requests
from dotenv import load_dotenv
# explicitly load .env from current working directory (avoid find_dotenv frame issues)
env_path = os.path.join(os.getcwd(), ".env")
loaded = load_dotenv(dotenv_path=env_path)
print("Loaded .env:", loaded, "path:", env_path)
base = os.getenv("OLLAMA_SERVER", "http://127.0.0.1:5000").rstrip('/')
url = base + "/generate"
try:
    r = requests.post(url, json={"prompt":"ping - model check"}, timeout=10)
    print("OLLAMA generate response:", r.status_code, (r.text[:200] + '...') if len(r.text)>200 else r.text)
except Exception as e:
    print("OLLAMA ping failed:", e)
PY

echo "Starting main.py (logs/main.log)..."
nohup python3 main.py > logs/main.log 2>&1 &
echo "Started. tail -f logs/main.log to watch."
