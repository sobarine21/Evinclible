import os
import streamlit as st
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import soundfile as sf

# Function to transcribe audio using Wav2Vec2 from Hugging Face
def transcribe_audio(audio_file):
    # Load pre-trained Wav2Vec2 model and processor
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
    
    # Read the audio file (ensure it's in WAV format)
    audio_input, samplerate = sf.read(audio_file)
    
    # Process the audio and predict transcription
    inputs = processor(audio_input, return_tensors="pt", sampling_rate=samplerate)
    with torch.no_grad():
        logits = model(input_values=inputs.input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    
    # Decode the prediction to text
    transcription = processor.batch_decode(predicted_ids)
    return transcription[0]

# Streamlit app
st.title("Audio Transcription and AI Analysis")
uploaded_file = st.file_uploader("Choose an audio file", type=["wav"])

if uploaded_file is not None:
    # Save the uploaded file to disk
    file_path = "temp_audio.wav"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Transcribe the audio using Wav2Vec2
    try:
        transcript = transcribe_audio(file_path)
        st.write("Transcript:")
        st.write(transcript)

    except Exception as e:
        st.error(f"Error with transcription: {e}")
    
    # Clean up the saved file after processing
    if os.path.exists(file_path):
        os.remove(file_path)
