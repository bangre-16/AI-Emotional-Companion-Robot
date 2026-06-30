from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")
    try:
        result = subprocess.run(
            ["ollama", "run", "phi3", prompt],
            capture_output=True, text=True, timeout=60
        )
        text = result.stdout.strip() or "No response"
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("✅ Ollama local bridge running at http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000)
