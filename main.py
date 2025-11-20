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
    # Save uploaded video temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(await file.read())
        video_path = tmp.name

    # Capture video
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Handle edge case where video couldn't be read
    if total_frames <= 0:
        cap.release()
        os.remove(video_path)
        return {"frames": [], "count": 0, "error": "Could not read video frames"}

    # Pick 6 evenly spaced frame indices
    indices = np.linspace(0, total_frames - 1, 6, dtype=int)

    frame_list = []

    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
        ret, frame = cap.read()
        if not ret or frame is None:
            continue
        ok, buffer = cv2.imencode(".jpg", frame)
        if not ok:
            continue
        encoded = base64.b64encode(buffer).decode("utf-8")
        frame_list.append(encoded)

    cap.release()
    os.remove(video_path)

    return {
        "frames": frame_list,
        "count": len(frame_list)
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
