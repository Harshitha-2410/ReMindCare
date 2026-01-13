import cv2
import os
from datetime import datetime
from django.core.files import File
from .models import EmotionSnapshot

SNAPSHOT_DIR = "snapshots"
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

CAMERA_ENABLED = os.getenv("ENABLE_CAMERA", "false") == "true"

class VideoCamera:
    def __init__(self, switch_threshold=2):
        self.video = None
        self.previous_emotion = None
        self.last_switch_time = None
        self.switch_threshold = switch_threshold

    def start(self):
        if CAMERA_ENABLED and self.video is None:
            self.video = cv2.VideoCapture(0)

    def stop(self):
        if self.video:
            self.video.release()
            self.video = None

    def capture_snapshot(self, frame, emotion):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"emotion_{emotion}_{timestamp}.jpg"
        filepath = os.path.join(SNAPSHOT_DIR, filename)

        cv2.imwrite(filepath, frame)

        try:
            with open(filepath, "rb") as f:
                django_file = File(f)
                snapshot = EmotionSnapshot(emotion=emotion)
                snapshot.image.save(filename, django_file, save=True)
        except Exception as e:
            print("Snapshot DB error:", e)

    def get_frame(self):
        if not CAMERA_ENABLED:
            return None, "Camera disabled"

        from .helpers.emotion_detector import detect_emotion

        if self.video is None:
            self.start()

        success, frame = self.video.read()
        if not success:
            return None, None

        emotion = detect_emotion(frame)

        now = datetime.now()
        if self.previous_emotion and emotion != self.previous_emotion:
            if not self.last_switch_time or (
                now - self.last_switch_time
            ).total_seconds() <= self.switch_threshold:
                self.capture_snapshot(frame, emotion)
            self.last_switch_time = now

        self.previous_emotion = emotion

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
