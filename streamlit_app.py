import os
import streamlit as st
from vosk import Model, KaldiRecognizer
import wave
import json

# Initialize Streamlit app
st.title("Speech-to-Text App with Vosk")
st.write("Upload a WAV file for transcription.")

# File upload
uploaded_file = st.file_uploader("Upload a WAV file", type=["wav"])

# Define Vosk model directory
MODEL_DIR = "vosk-model"

# Download the model if it doesn't exist
def download_model():
    if not os.path.exists(MODEL_DIR):
        st.info("Downloading Vosk model. This may take some time...")
        import requests, zipfile, io
        url = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip"
        r = requests.get(url, stream=True)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(MODEL_DIR)
        st.success("Vosk model downloaded!")

# Transcribe WAV file
def transcribe_audio(file_path):
    if not os.path.exists(MODEL_DIR):
        download_model()

    model = Model(MODEL_DIR)
    recognizer = KaldiRecognizer(model, 16000)

    # Open the audio file
    with wave.open(file_path, "rb") as wf:
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            st.error("Audio file must be WAV format with 16kHz, mono, and 16-bit.")
            return None

        transcription = ""
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                transcription += result.get("text", "") + " "

        # Finalize the transcription
        final_result = json.loads(recognizer.FinalResult())
        transcription += final_result.get("text", "")
        return transcription

if uploaded_file:
    st.info("Processing your file...")
    
    # Save uploaded file temporarily
    temp_file_path = "temp_audio.wav"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Transcribe and display
    transcription = transcribe_audio(temp_file_path)
    if transcription:
        st.success("Transcription completed!")
        st.text_area("Transcription:", transcription, height=300)

    # Clean up
    os.remove(temp_file_path)
