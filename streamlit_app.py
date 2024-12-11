import streamlit as st
import whisper
import tempfile
import os
import traceback

# App Title
st.title("Audio to Text Transcription")
st.write("Upload an audio file to transcribe its content into text.")

# Add Debugging Option
debug_mode = st.checkbox("Enable Debug Mode")

# File Uploader
uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a", "ogg", "flac"])

if uploaded_file:
    try:
        st.info("Processing uploaded audio file...")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(uploaded_file.read())
            temp_audio_path = temp_audio.name

        st.audio(uploaded_file, format="audio/wav")
        st.success("File uploaded successfully!")

        # Load Whisper Model
        st.info("Loading transcription model (this may take a few seconds)...")
        model = whisper.load_model("base")  # Use "base" for lightweight, "small" for better accuracy
        
        # Transcribe Audio
        st.info("Transcribing audio...")
        transcription_result = model.transcribe(temp_audio_path)

        # Display Results
        st.success("Transcription completed!")
        st.text_area("Transcribed Text", transcription_result["text"], height=300)

        # Add Download Option
        st.download_button(
            label="Download Transcription",
            data=transcription_result["text"],
            file_name="transcription.txt",
            mime="text/plain"
        )
    
    except Exception as e:
        # Display error to the user
        st.error("An error occurred during processing:")
        st.error(str(e))
        
        # Show traceback in debug mode
        if debug_mode:
            st.error("Detailed Error Trace:")
            st.text(traceback.format_exc())
    
    finally:
        # Clean up the temporary audio file
        if 'temp_audio_path' in locals() and os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
            if debug_mode:
                st.info("Temporary file cleaned up.")

# Footer
st.write("Powered by OpenAI Whisper and Streamlit")
