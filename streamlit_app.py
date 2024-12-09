import streamlit as st
import speech_recognition as sr
import google.generativeai as genai
import librosa

# Configure the API key securely from Streamlit's secrets
# Make sure to add GOOGLE_API_KEY in secrets.toml (for local) or Streamlit Cloud Secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    if audio_file.name.endswith(".m4a"):
        # Convert m4a to wav for compatibility with speech_recognition
        y, sr = librosa.load(audio_file)
        librosa.output.write_wav("temp_audio.wav", y, sr=16000)
        audio_file = "temp_audio.wav"

    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return text

def analyze_text_with_gemini(text):
    prompt = f"Analyze the following text: {text}. Provide a summary, identify key points, and suggest potential insights or actions."
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

# Streamlit app
st.title("Audio Transcription and AI Analysis")
uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "m4a"])

if uploaded_file is not None:
    transcript = transcribe_audio(uploaded_file)
    st.write("Transcript:")
    st.write(transcript)

    try:
        analysis_result = analyze_text_with_gemini(transcript)
        st.write("AI Analysis:")
        st.write(analysis_result)
    except Exception as e:
        st.error(f"Error: {e}")
