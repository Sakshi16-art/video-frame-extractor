from fastapi import FastAPI, File, UploadFile
import uvicorn
import cv2
import numpy as np
import base64
import tempfile
import os

app = FastAPI()

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(await file.read())
        video_path = tmp.name

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    if total_frames <= 0:
        cap.release()
        os.remove(video_path)
        return {"frames": [], "count": 0, "error": "Could not read video"}

    # Dynamic frame count (avoids OpenAI input limits)
    if total_frames > 300:    # > 10 sec video approx
        num_frames = 4
    else:
        num_frames = 6

    indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
    frame_list = []

    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
        ret, frame = cap.read()
        if not ret:
            continue

        # Resize + compress
        frame = cv2.resize(frame, (512, 288))
        ok, buffer = cv2.imencode(".jpg", frame, [
            int(cv2.IMWRITE_JPEG_QUALITY), 45
        ])
        if not ok:
            continue

        timestamp_sec = idx / fps
        timestamp = round(timestamp_sec, 2)

        base64_data = base64.b64encode(buffer).decode("utf-8")
        frame_list.append({
            "timestamp": timestamp,
            "image": base64_data
        })

    cap.release()
    os.remove(video_path)

    return {"frames": frame_list, "count": len(frame_list)}
