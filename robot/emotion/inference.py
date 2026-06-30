import os
import time

try:
    import cv2
except Exception as e:
    cv2 = None
    print("[inference] OpenCV not available:", e)

try:
    import numpy as np
except Exception as e:
    np = None
    print("[inference] numpy not available:", e)

# Try to import tensorflow/keras but keep graceful fallback
try:
    from tensorflow.keras.models import load_model
except Exception as e:
    load_model = None
    print("[inference] tensorflow.keras not available:", e)
DEFAULT_MODEL_REL = os.path.join("models", "best-emotion-model.h5")
# Haar cascade that ships with OpenCV (often at /usr/share/opencv or in cv2.data)
DEFAULT_CASCADE = None
if cv2 is not None:
    try:
        DEFAULT_CASCADE = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    except Exception:
        DEFAULT_CASCADE = "haarcascade_frontalface_default.xml"


LABELS = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]

class EmotionEngine:
    def __init__(self, model_path=None, cascade_path=None, input_size=48):
        """
        model_path: path to .h5 Keras model (relative to this file if not absolute)
        cascade_path: path to Haar cascade xml for face detection
        input_size: square input size expected by model (default 48 for FER)
        """
        self.base_dir = os.path.dirname(__file__)
        self.model_path = model_path or os.path.join(self.base_dir, DEFAULT_MODEL_REL)
        self.cascade_path = cascade_path or (os.path.join(self.base_dir, DEFAULT_CASCADE) if DEFAULT_CASCADE else None)
        self.input_size = input_size
        self.model = None
        self.face_cascade = None
        self._loaded = False

        self._load_resources()
        def _load_resources(self):
        # load model
         if load_model is None:
            print("[EmotionEngine] keras load_model not available. Install tensorflow.")
         else:
            if not os.path.isabs(self.model_path):
                self.model_path = os.path.join(self.base_dir, self.model_path)
            if os.path.exists(self.model_path):
                try:
                    print(f"[EmotionEngine] Loading model from {self.model_path} ...")
                    self.model = load_model(self.model_path)
                    print("[EmotionEngine] Model loaded.")
                except Exception as e:
                    print("[EmotionEngine] Failed to load model:", e)
            else:
                print(f"[EmotionEngine] Model file not found at: {self.model_path}")

        # load cascade (optional)
        if cv2 is not None and self.cascade_path and os.path.exists(self.cascade_path):
            try:
                self.face_cascade = cv2.CascadeClassifier(self.cascade_path)
                print("[EmotionEngine] Haar cascade loaded:", self.cascade_path)
            except Exception as e:
                print("[EmotionEngine] Could not load cascade:", e)
        else:
            if cv2 is None:
                print("[EmotionEngine] OpenCV missing � camera/face-detection disabled.")
            else:
                print("[EmotionEngine] Haar cascade not found; will use center-crop fallback for face region.")

        self._loaded = (self.model is not None)

    def is_ready(self):
        return self._loaded

    def _preprocess_face(self, face_img):
        """
        face_img: BGR image region (numpy array)
        returns: preprocessed tensor (1, H, W, 1) or (1, H, W, C) depending on model
        Expected: grayscale 48x48 normalized [0,1]
        """
        if np is None:
            raise RuntimeError("numpy required for preprocessing")
          # Convert to grayscale if needed
        if len(face_img.shape) == 3 and face_img.shape[2] == 3:
            face = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        else:
            face = face_img.copy()

        face = cv2.resize(face, (self.input_size, self.input_size), interpolation=cv2.INTER_AREA)
        face = face.astype("float32") / 255.0
        # shape -> (H,W) -> (1,H,W,1)
        face = np.expand_dims(face, axis=0)
        face = np.expand_dims(face, axis=-1)
        return face

    def predict_from_frame(self, frame):
        """
        frame: BGR image from camera (np array)
        returns: (label (str), prob (float)) or ("neutral", 0.0) if model not ready
        """
        if not self._loaded:
            return ("neutral", 0.0)

        # face detection
        face_region = None
        if self.face_cascade is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
            if len(faces) > 0:
                # choose the largest face
                faces = sorted(faces, key=lambda r: r[2]*r[3], reverse=True)
                x,y,w,h = faces[0]
                face_region = frame[y:y+h, x:x+w]
        # fallback: center crop
        if face_region is None:
            h, w = frame.shape[:2]
            side = min(h, w)
            cx, cy = w//2, h//2
            half = side//2
            x1, y1 = max(0, cx-half), max(0, cy-half)
            x2, y2 = min(w, x1+side), min(h, y1+side)
            face_region = frame[y1:y2, x1:x2]
        try:
            inp = self._preprocess_face(face_region)
            preds = self.model.predict(inp)
            # model may output probabilities vector
            if preds.ndim == 2 and preds.shape[1] >= 1:
                probs = preds[0]
                idx = int(np.argmax(probs))
                label = LABELS[idx] if idx < len(LABELS) else str(idx)
                return (label, float(probs[idx]))
            else:
                # fallback if model returned scalar
                return ("neutral", 0.0)
        except Exception as e:
            print("[EmotionEngine] Predict failed:", e)
            return ("neutral", 0.0)

    def predict_from_camera_loop(self, camera_index=0, show_window=False, fps_print=False):
        """
        Demo loop: open camera, predict emotion per frame and print.
        show_window: if True, display camera with label overlay (requires X)
        """
        if cv2 is None:
            raise RuntimeError("OpenCV required to use camera loop")

        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            raise RuntimeError(f"Cannot open camera index {camera_index}")

        last = time.time()
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("[EmotionEngine] camera frame read failed")
                    time.sleep(0.1)
                    continue
                label, prob = self.predict_from_frame(frame)
                text = f"{label} ({prob:.2f})"
                print("[EmotionEngine]", text)
                if show_window:
                    cv2.putText(frame, text, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
                    cv2.imshow("Emotion", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                if fps_print:
                    now = time.time()
                    print("FPS:", 1.0/(now-last) if (now-last)>0 else 0.0)
                    last = now
                time.sleep(0.05)
        finally:
            cap.release()
            if show_window:
                cv2.destroyAllWindows()
if __name__ == "__main__":
    # Quick manual test: run camera loop if model exists
    engine = EmotionEngine()
    if not engine.is_ready():
        print("Engine not ready. Check model file at:", engine.model_path)
    else:
        print("Engine ready. Running camera demo. Press Ctrl+C to stop.")
        try:
            engine.predict_from_camera_loop(show_window=False, fps_print=True)
        except KeyboardInterrupt:
            print("Stopped.")