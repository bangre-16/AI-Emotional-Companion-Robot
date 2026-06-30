from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
import base64
import os
import threading
import time
import subprocess

app = Flask(__name__)
CORS(app)

# ------------------------------
# Load Models
# ------------------------------
MODEL_PATHS = {
    "train": "train-model.h5",
    "best": "best-emotion-model.h5"
}

models = {}
for name, path in MODEL_PATHS.items():
    if os.path.exists(path):
        try:
            models[name] = keras.models.load_model(path)
            print(f"Loaded model: {path}")
        except Exception as e:
            print(f"Failed loading {path}: {e}")
            models[name] = None
    else:
        print(f"Missing: {path}")
        models[name] = None

model = models.get("train")
EMOTIONS = ['angry','disgust','fear','happy','neutral','sad','surprise']

# ------------------------------
# FFmpeg Camera Capture (Always works)
# ------------------------------
CAM_SRC = os.environ.get("CAMERA_SOURCE", "1")
DEVICE = f"/dev/video{CAM_SRC}" if CAM_SRC.isdigit() else CAM_SRC
IN_FMT = os.environ.get("FFMPEG_INPUT_FORMAT", "yuyv422")

FFMPEG_CMD = [
    "ffmpeg", "-hide_banner", "-loglevel", "fatal",
    "-f", "v4l2", "-input_format", IN_FMT,
    "-video_size", "640x480",
    "-i", DEVICE,
    "-f", "image2pipe", "-vcodec", "mjpeg", "-"
]

latest_frame = None
lock = threading.Lock()

def capture_loop():
    global latest_frame
    print(f"FFmpeg capturing from {DEVICE} ({IN_FMT})")

    while True:
        try:
            p = subprocess.Popen(FFMPEG_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, _ = p.communicate(timeout=6)

            if not out:
                time.sleep(0.1)
                continue

            img = cv2.imdecode(np.frombuffer(out, np.uint8), cv2.IMREAD_COLOR)
            if img is None:
                continue

            with lock:
                latest_frame = img.copy()

            time.sleep(0.03)
        except Exception:
            time.sleep(0.1)

threading.Thread(target=capture_loop, daemon=True).start()

# ------------------------------
# Preprocess Image
# ------------------------------
def preprocess(b64):
    try:
        b64 = b64.split(",")[1]
        img = cv2.imdecode(np.frombuffer(base64.b64decode(b64), np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            return None

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face.detectMultiScale(gray, 1.2, 5)

        if len(faces):
            x,y,w,h = max(faces, key=lambda f: f[2]*f[3])
            pad = int(max(w,h)*0.2)
            face_gray = gray[max(0,y-pad):y+h+pad, max(0,x-pad):x+w+pad]
        else:
            h,w = gray.shape
            s = min(h,w)
            face_gray = gray[(h-s)//2:(h+s)//2, (w-s)//2:(w+s)//2]

        face_gray = cv2.resize(face_gray, (48,48))
        face_gray = face_gray.astype("float32")/255.0
        return face_gray.reshape(1,48,48,1)
    except:
        return None

# ------------------------------
# Routes
# ------------------------------
@app.route("/")
def home():
    return {"status":"online", "models":list(models.keys())}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if "image" not in data:
        return {"error":"no image"}, 400

    m = models.get(data.get("model","train"))
    if m is None:
        return {"error":"model not loaded"}, 500

    img = preprocess(data["image"])
    if img is None:
        return {"error":"invalid image"}, 400

    p = m.predict(img, verbose=0)[0]
    idx = int(np.argmax(p))
    return {"emotion": EMOTIONS[idx], "confidence": float(p[idx])}

@app.route("/predict_camera")
def predict_cam():
    if model is None:
        return {"error":"model not loaded"}, 500
    if latest_frame is None:
        return {"error":"no camera frame"}, 503

    ok, jpeg = cv2.imencode(".jpg", latest_frame)
    b64 = base64.b64encode(jpeg).decode()
    img = preprocess(f"data:image/jpeg;base64,{b64}")

    if img is None:
        return {"error":"bad frame"}, 500

    p = model.predict(img, verbose=0)[0]
    idx = int(np.argmax(p))
    return {"emotion": EMOTIONS[idx], "confidence": float(p[idx])}

@app.route("/video_feed")
def video():
    def gen():
        while True:
            if latest_frame is not None:
                _, jpeg = cv2.imencode(".jpg", latest_frame)
                yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" +
                       jpeg.tobytes() + b"\r\n")
            time.sleep(0.05)
    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")

# ------------------------------
# Start Server
# ------------------------------
if __name__ == "__main__":
    print("Server running on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
