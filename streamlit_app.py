import streamlit as st
from transformers import pipeline
import os
import torchaudio
import torch

# Load Whisper Model
@st.cache_resource
def load_model():
    st.write("Loading Whisper model...")
    return pipeline("automatic-speech-recognition", model="openai/whisper-large-v3-turbo")

pipe = load_model()

# Function to Transcribe Audio
def transcribe_audio(file_path):
    st.write(f"Processing file: {file_path}")

    try:
        # Load audio using torchaudio
        waveform, sample_rate = torchaudio.load(file_path)

        # Ensure the waveform is in float32
        waveform = waveform.to(torch.float32)

        # Check the model expects the correct sample rate (Whisper models expect 16000 Hz)
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)

        # Transcribe the audio
        result = pipe(waveform.numpy())
        return result["text"]
    except Exception as e:
        st.error(f"Error during transcription: {e}")
        raise

# Speaker Labeling Function (Placeholder Logic)
def label_speakers(transcription):
    lines = transcription.split(". ")
    labeled_transcription = ""
    for i, line in enumerate(lines):
        speaker = "Agent" if i % 2 == 0 else "Customer"
        labeled_transcription += f"{speaker}: {line.strip()}\n"
    return labeled_transcription

# Streamlit App UI
def main():
    st.title("Call Transcription App")
    st.write("Upload a call recording to generate a transcription with labeled dialogues.")

    # Debugging Toggle
    debug_mode = st.checkbox("Enable Debugging")

    # Upload Audio File
    uploaded_file = st.file_uploader("Upload your audio file (wav, mp3, m4a):", type=["wav", "mp3", "m4a"])

    if uploaded_file is not None:
        # Save the uploaded file temporarily
        temp_file_path = f"temp_{uploaded_file.name}"
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Transcribe the audio
        with st.spinner("Transcribing audio..."):
            try:
                transcription = transcribe_audio(temp_file_path)
                labeled_transcription = label_speakers(transcription)

                # Display the transcription
                st.subheader("Transcription")
                st.text_area("Labeled Transcription:", labeled_transcription, height=300)

                # Download Transcription
                st.download_button(
                    label="Download Transcription as TXT",
                    data=labeled_transcription,
                    file_name="transcription.txt",
                    mime="text/plain",
                )
            except Exception as e:
                if debug_mode:
                    st.error(f"Debug Info: {e}")
                else:
                    st.error("An error occurred during transcription. Enable debugging for more details.")

        # Remove the temporary file
        os.remove(temp_file_path)

if __name__ == "__main__":
    main()
