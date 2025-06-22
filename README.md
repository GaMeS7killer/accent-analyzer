# English Accent Detector

This is a simple proof-of-concept tool that:

- Accepts a public video URL (direct MP4 link)
- Downloads the video
- Extracts the audio
- Transcribes speech using Deepgram API
- Returns detected language, transcript, and confidence score

---

## Tech Stack

- Python
- Streamlit (for UI)
- MoviePy (for audio extraction)
- Deepgram API (for transcription & analysis)

---

## How to run locally:

1. Install requirements:

```bash
pip install -r requirements.txt
