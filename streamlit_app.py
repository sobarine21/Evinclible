import streamlit as st
import whisper
import google.generativeai as genai

# Configure the API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Load Whisper model
model = whisper.load_model("base")  # Choose 'base' or another model size if needed

def transcribe_audio(audio_file):
    # Use Whisper to transcribe the audio file
    result = model.transcribe(audio_file)
    return result['text']

def analyze_text_with_gemini(text):
    prompt = f"Analyze the following text: {text}. Provide a summary, identify key points, and suggest potential insights or actions."
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

# Streamlit app
st.title("Audio Transcription and AI Analysis")
uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"])

if uploaded_file is not None:
    with open("temp_audio.wav", "wb") as f:
        f.write(uploaded_file.read())

    transcript = transcribe_audio("temp_audio.wav")
    st.write("Transcript:")
    st.write(transcript)

    try:
        analysis_result = analyze_text_with_gemini(transcript)
        st.write("AI Analysis:")
        st.write(analysis_result)
    except Exception as e:
        st.error(f"Error: {e}")
