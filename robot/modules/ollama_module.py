# modules/ollama_module.py
import os
import requests
from dotenv import load_dotenv
import logging

# Setup logging for quick debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OllamaModule")

ROOT = os.path.dirname(os.path.dirname(__file__))
load_dotenv(os.path.join(ROOT, ".env"))

# Allow overriding server, timeout, and a demo stub mode from .env
OLLAMA_SERVER = os.getenv("OLLAMA_SERVER", "http://10.61.67.110:5000").rstrip('/')
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "60"))  # default 60s
OLLAMA_USE_STUB = os.getenv("OLLAMA_USE_STUB", "false").lower() in ("1", "true", "yes")

def get_response(prompt, emotion=None, timeout=None):
    """
    Query the Ollama bridge /generate endpoint and return a dict:
    {"text": <string>, "error": None} on success or
    {"text": <fallback str>, "error": <error str>} on failure.

    If OLLAMA_USE_STUB is enabled in .env, this returns a canned reply
    (useful for demos when the bridge/model is unreliable).
    """

    if OLLAMA_USE_STUB:
        logger.warning("OLLAMA_USE_STUB enabled � returning canned reply")
        return {"text": "You are not alone,Don't worry Empath is there with you.Never think you're alone,you deserve to be loved by everyone.", "error": None}

    url = f"{OLLAMA_SERVER}/generate"
    payload = {"prompt": prompt}
    t = timeout or OLLAMA_TIMEOUT

    try:
        logger.info("POST %s (timeout=%ss) prompt=%s", url, t, (prompt[:120] + '...') if len(prompt) > 120 else prompt)
        r = requests.post(url, json=payload, timeout=t)
        r.raise_for_status()
        # Safe parse
        if not r.content:
            return {"text": "", "error": "Empty response from server"}

        try:
            data = r.json()
        except ValueError:
            # Not JSON � return raw text
            logger.warning("Non-JSON response from server: %s", r.text[:200])
            return {"text": r.text, "error": None}

        # Try common shapes for returned text
        text = None
        if isinstance(data, dict):
            for k in ("text", "response", "output", "result"):
                if k in data and isinstance(data[k], (str,)):
                    text = data[k]
                    break

            # Handle nested choices (e.g., { "choices": [ { "text": "..." } ] })
            if text is None and "choices" in data and isinstance(data["choices"], list) and data["choices"]:
                first = data["choices"][0]
                if isinstance(first, dict):
                    text = first.get("text") or first.get("message") or None

        # Fallback: stringify whatever we got
        if text is None:
            text = str(data)

        return {"text": text, "error": None}

    except requests.exceptions.Timeout as e:
        logger.error("Timeout calling ollama bridge: %s", e)
        return {"text": "Sorry, the response took too long.", "error": str(e)}
    except requests.exceptions.ConnectionError as e:
        logger.error("Connection error calling ollama bridge: %s", e)
        return {"text": "Sorry, I couldn't reach the generation server.", "error": str(e)}
    except Exception as e:
        logger.exception("Unexpected error in get_response:")
        return {"text": "Sorry, I couldn't generate a reply right now.", "error": str(e)}
