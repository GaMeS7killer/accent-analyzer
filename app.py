import streamlit as st
from deepgram import Deepgram
import asyncio
import os

# ====== READ DEEPGRAM API KEY FROM ENVIRONMENT =======
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# Async function to call Deepgram API directly on uploaded file
async def transcribe_with_deepgram(file_buffer):
    dg_client = Deepgram(DEEPGRAM_API_KEY)
    source = {'buffer': file_buffer, 'mimetype': 'video/mp4'}
    response = await dg_client.transcription.prerecorded(
        source,
        {'language': 'en', 'detect_language': True, 'punctuate': True, 'smart_format': True}
    )
    return response

# Streamlit UI
st.title("🎤 English Accent Detector (Upload Version)")

uploaded_file = st.file_uploader("Upload an MP4 file", type=["mp4"])

if uploaded_file is not None:
    if st.button("Analyze Accent"):
        try:
            st.info("Sending file to Deepgram for analysis...")
            response = asyncio.run(transcribe_with_deepgram(uploaded_file))

            # Check if we got valid results before accessing
            channels = response['results'].get('channels', [])
            if channels and channels[0]['alternatives']:
                transcript = channels[0]['alternatives'][0]['transcript']
                confidence = channels[0]['alternatives'][0].get('confidence', 0)
                language = response['results'].get('language', 'Unknown')

                st.success("✅ Analysis Completed!")
                st.write(f"**Transcript:** {transcript}")
                st.write(f"**Detected Language:** {language}")
                st.write(f"**Confidence:** {round(confidence * 100, 2)} %")
            else:
                st.warning("No speech detected in the video.")

        except Exception as e:
            st.error(f"Error: {str(e)}")
