import streamlit as st
import requests
from deepgram import Deepgram
import asyncio
import os

# ====== READ DEEPGRAM API KEY FROM ENVIRONMENT =======
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# Function to download video with proper headers
def download_video(video_url, output_path):
    headers = {'User-Agent': 'Mozilla/5.0'}  # VERY IMPORTANT FIX
    response = requests.get(video_url, stream=True, headers=headers)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        raise Exception("Failed to download video")

# Async function to call Deepgram API directly on video file
async def transcribe_with_deepgram(video_file):
    dg_client = Deepgram(DEEPGRAM_API_KEY)
    with open(video_file, 'rb') as f:
        source = {'buffer': f, 'mimetype': 'video/mp4'}
        response = await dg_client.transcription.prerecorded(
            source,
            {'language': 'en', 'detect_language': True, 'punctuate': True, 'smart_format': True}
        )
        return response

# Streamlit UI
st.title("🎤 English Accent Detector")

video_url = st.text_input("Enter public video URL (Direct MP4 Link)")

if st.button("Analyze Accent"):
    if video_url:
        try:
            st.info("Downloading video...")
            download_video(video_url, 'video.mp4')
            
            st.info("Sending video to Deepgram for analysis...")
            response = asyncio.run(transcribe_with_deepgram('video.mp4'))

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

            os.remove('video.mp4')

        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a valid video URL.")
