import streamlit as st
import google.generativeai as genai
import librosa
import speech_recognition as sr

# Configure the API key securely from Streamlit's secrets
# Make sure to add GOOGLE_API_KEY in secrets.toml (for local) or Streamlit Cloud Secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    text = recognizer.recognize_google(audio_data)
    return text

def analyze_text_with_gemini(text):
    prompt = f"Analyze the following text: {text}. Provide a sentiment analysis (positive, negative, neutral) and identify the main topics."
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

def main():
    st.title("Customer Support Call Analysis with Gemini AI")

    uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "ogg"])

    if uploaded_file is not None:
        # Transcribe audio to text
        text = transcribe_audio(uploaded_file)

        # Analyze the text with Gemini AI
        analysis = analyze_text_with_gemini(text)

        # Display results
        st.write("Transcript:")
        st.write(text)

        st.write("Gemini AI Analysis:")
        st.write(analysis)

if __name__ == '__main__':
    main()
