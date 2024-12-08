import streamlit as st
import librosa
import speech_recognition as sr
import spacy
import tensorflow as tf
import numpy as np

# Streamlit App UI
st.title("Customer Support Call Analysis")

# File upload
uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3", "ogg"])

if uploaded_file is not None:
    # Load audio file
    audio, sample_rate = librosa.load(uploaded_file, sr=None)
    
    # Display audio player
    st.audio(uploaded_file, format="audio/wav")

    # Speech-to-Text
    recognizer = sr.Recognizer()
    with sr.AudioFile(uploaded_file) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        text = "Google Speech Recognition could not understand the audio"
    except sr.RequestError as e:
        text = f"Could not request results from Google Speech Recognition service; {e}"
    
    # NLP Analysis
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Preprocess Text for Sentiment Analysis
    def preprocess_text(text):
        return " ".join([token.lemma_ for token in doc if not token.is_stop])
    
    processed_text = preprocess_text(text)

    # Load Pre-trained Sentiment Model (Assumes the model is already trained and saved as 'sentiment_model.h5')
    sentiment_model = tf.keras.models.load_model("sentiment_model.h5")
    
    # Predict Sentiment (Assumes the sentiment model is a text-based neural network)
    sentiment_input = np.array([processed_text])
    sentiment_score = sentiment_model.predict(sentiment_input)

    # Display results
    st.write("Transcript:")
    st.write(text)

    st.write("Sentiment Score:")
    st.write(sentiment_score[0])

    # Additional NLP Analysis
    st.write("Entities:")
    for ent in doc.ents:
        st.write(f"{ent.text} ({ent.label_})")

    st.write("Tokens and POS:")
    for token in doc:
        st.write(f"{token.text} ({token.pos_})")

    # Add any other analyses you wish to include...
