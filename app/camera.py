import cv2
import os
from datetime import datetime
from django.core.files import File
from .models import EmotionSnapshot

# =====================================================
# ENVIRONMENT GUARDS (CRITICAL FOR RENDER)
# =====================================================
CAMERA_ENABLED = os.getenv("ENABLE_CAMERA", "false").lower() == "true"

# Folder to store snapshots locally
SNAPSHOT_DIR = "snapshots"
os.makedirs(SNAPSHOT_DIR, exist_ok=True)


class VideoCamera:
    """
    Handles video capture, emotion detection, and snapshot saving.
    SAFE for cloud environments (Render).
    """

    def __init__(self, switch_threshold=2):
        # ❌ DO NOT open camera here
        self.video = None

        self.previous_emotion = None
        self.last_switch_time = None
        self.switch_threshold = switch_threshold  # seconds

    # -------------------------------------------------
    # SAFE CAMERA START (only when enabled)
    # -------------------------------------------------
    def start_camera(self):
        if not CAMERA_ENABLED:
            return False

        if self.video is None:
            self.video = cv2.VideoCapture(0)

        return self.video.isOpened()

    def __del__(self):
        if self.video is not None:
            self.video.release()

    # -------------------------------------------------
    # SNAPSHOT HANDLING
    # -------------------------------------------------
    def capture_snapshot(self, frame, emotion):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"emotion_{emotion}_{timestamp}.jpg"
        filepath = os.path.join(SNAPSHOT_DIR, filename)

        # Save locally
        cv2.imwrite(filepath, frame)
        print(f"[Snapshot] {emotion} captured at {timestamp}")

        # Save to DB
        try:
            with open(filepath, "rb") as f:
                django_file = File(f)
                snapshot = EmotionSnapshot(emotion=emotion)
                snapshot.image.save(filename, django_file, save=True)
        except Exception as e:
            print(f"[Snapshot DB Error]: {e}")

    # -------------------------------------------------
    # MAIN FRAME LOGIC
    # -------------------------------------------------
    def get_frame(self):
        """
        Capture frame, detect emotion, return JPEG bytes.
        SAFE: returns immediately if camera is disabled.
        """

        # 🚫 CAMERA DISABLED (Render-safe)
        if not CAMERA_ENABLED:
            return None, "Camera disabled"

        # Start camera safely
        if not self.start_camera():
            return None, "Camera unavailable"

        success, frame = self.video.read()
        if not success:
            return None, "Frame read failed"

        # 🔥 LAZY IMPORT (prevents TensorFlow load at startup)
        from .helpers.emotion_detector import detect_emotion

        emotion = detect_emotion(frame)

        # Detect rapid emotion switch
        now = datetime.now()
        if self.previous_emotion and emotion != self.previous_emotion:
            if (
                self.last_switch_time is None
                or (now - self.last_switch_time).total_seconds()
                <= self.switch_threshold
            ):
                self.capture_snapshot(frame, emotion)
            self.last_switch_time = now

        self.previous_emotion = emotion

        # Draw emotion label
        cv2.putText(
            frame,
            f"Emotion: {emotion}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        _, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes(), emotion
