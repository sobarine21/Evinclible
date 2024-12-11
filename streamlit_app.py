import streamlit as st
import speech_recognition as sr

# Streamlit app configuration
st.title("WAV File Transcription")
st.write("Upload a WAV file, and the application will transcribe its audio.")

# File upload section
uploaded_file = st.file_uploader("Upload your WAV file", type=["wav"])

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    temp_file_path = "uploaded_audio.wav"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("File uploaded successfully!")

    # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    try:
        with sr.AudioFile(temp_file_path) as source:
            st.write("Processing the audio file...")
            audio_data = recognizer.record(source)

        # Transcribe the audio
        st.write("Transcribing the audio...")
        transcription = recognizer.recognize_google(audio_data)

        # Display the transcription
        st.subheader("Transcription:")
        st.write(transcription)

    except Exception as e:
        st.error(f"An error occurred during transcription: {e}")
