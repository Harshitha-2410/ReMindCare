import os

def detect_emotion(frame):
    """
    Detect emotion from a video frame.
    DeepFace is loaded lazily to avoid memory crash on startup.
    """

    # 🔒 Disable AI on low-memory environments like Render
    if os.getenv("ENABLE_AI", "false") != "true":
        return "disabled"

    try:
        # 🔥 Lazy import (CRITICAL FIX)
        from deepface import DeepFace

        result = DeepFace.analyze(
            frame,
            actions=["emotion"],
            enforce_detection=False
        )

        if isinstance(result, list):
            return result[0]["dominant_emotion"]
        return result["dominant_emotion"]

    except Exception as e:
        print("Emotion error:", e)
        return "Unknown"

# import cv2
# from deepface import DeepFace

# def detect_emotion(frame):
#     try:
#         result = DeepFace.analyze(
#             frame,
#             actions=['emotion'],
#             enforce_detection=False
#         )

#         if isinstance(result, list):
#             return result[0]['dominant_emotion']
#         else:
#             return result['dominant_emotion']

#     except Exception as e:
#         print("Emotion error:", e)
#         return "Unknown"
