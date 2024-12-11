import streamlit as st
from whisper_timestamped import load_model, transcribe_with_timestamps
import tempfile
import os

# App Title
st.title("Long Audio to Text Transcription")
st.write("Upload a long audio file, and this app will transcribe it into text. Supports formats like WAV, MP3, M4A.")

# Upload audio file
uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"])

if uploaded_file:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(uploaded_file.read())
        temp_audio_path = temp_audio.name

    st.audio(uploaded_file, format="audio/wav")

    # Load Whisper model
    st.info("Loading transcription model (this might take a few seconds)...")
    model = load_model("base")  # "base" model is lightweight and quick to use.

    # Transcribe audio with timestamps
    st.info("Transcribing audio...")
    result = transcribe_with_timestamps(model, temp_audio_path)

    # Display transcription results
    st.success("Transcription completed!")
    st.text_area("Transcribed Text with Timestamps", result["text"], height=300)

    # Optional: Save transcription as a text file
    st.download_button(
        label="Download Transcription",
        data=result["text"],
        file_name="transcription.txt",
        mime="text/plain"
    )

    # Cleanup temporary file
    os.remove(temp_audio_path)

# Footer
st.write("Powered by OpenAI Whisper and Streamlit")
