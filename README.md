# Video Frame Extractor API

A simple FastAPI service that receives a video file, extracts 6 evenly spaced frames using OpenCV, and returns them as base64 images.

## 🔥 Features
- Upload any `.mp4` video
- Extract 6 evenly spaced frames
- Returns frames as `.jpg` base64 strings
- Ideal for AI workflows (OpenAI, n8n, etc.)

---

## 🚀 Deploy Instantly on Railway

1. Push this repository to GitHub under your account: `Sakshi16-art/video-frame-extractor`
2. Then click this button:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new?templateUrl=https://github.com/Sakshi16-art/video-frame-extractor)

Railway will:
- Build the Docker image
- Run the FastAPI app
- Expose a public URL like:

`https://your-app-name.up.railway.app`

Your extract endpoint will be:

`POST https://your-app-name.up.railway.app/extract`

---

## 🛠 API Endpoint

### Endpoint

`POST /extract`

### Request (multipart/form-data)

| Field | Type        | Description         |
|-------|-------------|---------------------|
| file  | file (.mp4) | The uploaded video  |

Example using `curl`:

```bash
curl -X POST \
  -F "file=@/path/to/video.mp4" \
  https://your-app-name.up.railway.app/extract
```

### Response (JSON)

```json
{
  "frames": ["base64-frame-1", "base64-frame-2", "..."],
  "count": 6
}
```

---

## 🧩 Local Development

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open:

- Docs: http://127.0.0.1:8000/docs

---

## 🔗 Use with n8n

1. Create a workflow with:
   - **Webhook** (receives video as `data`)
   - **Move Binary Data** (move `data` → `video`)
   - **HTTP Request** (POST to this API, send binary `video`)
   - **HTTP Request** (to OpenAI API, send `frames` in body)
   - **HTTP Response** (return analysis)

2. Set the **Frame Extractor URL** in n8n to your deployed URL:

`https://your-app-name.up.railway.app/extract`

---

## ✅ Ready!

You can now:
- Deploy with one click on Railway (after pushing to GitHub)
- Plug the URL into n8n
- Start doing video → frame → AI analysis.
