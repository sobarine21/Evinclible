import streamlit as st
from moviepy.audio.io.AudioFileClip import AudioFileClip
import os

def convert_audio(input_file, output_file, output_format):
    """
    Converts an audio file to the specified format using moviepy.

    Args:
        input_file (str): Path to the input file.
        output_file (str): Path to save the converted file.
        output_format (str): Desired output format (e.g., 'mp3', 'wav').
    """
    try:
        with AudioFileClip(input_file) as audio:
            audio.write_audiofile(output_file, codec='libmp3lame' if output_format == 'mp3' else None)
        st.success(f"Conversion successful: {output_file}")
    except Exception as e:
        st.error(f"Error converting file: {e}")

def main():
    st.title("Audio Converter")

    # Ensure the 'temp' directory exists
    if not os.path.exists("temp"):
        os.makedirs("temp")

    uploaded_file = st.file_uploader("Upload an audio file", type=["m4a", "wav", "mp3"])

    if uploaded_file is not None:
        file_details = {
            "filename": uploaded_file.name,
            "filetype": uploaded_file.type
        }
        st.write(file_details)

        # Save the uploaded file to the 'temp' directory
        input_file = os.path.join("temp", uploaded_file.name)
        with open(input_file, "wb") as f:
            f.write(uploaded_file.read())

        output_format = st.selectbox("Select output format", ("wav", "mp3"))

        if st.button("Convert"):
            output_file = os.path.join("temp", f"{uploaded_file.name.split('.')[0]}.{output_format}")
            convert_audio(input_file, output_file, output_format)

            # Provide a download button for the converted file
            with open(output_file, "rb") as f:
                st.download_button(
                    label="Download converted file",
                    data=f,
                    file_name=f"{uploaded_file.name.split('.')[0]}.{output_format}"
                )

            # Clean up temporary files
            os.remove(input_file)
            os.remove(output_file)

if __name__ == "__main__":
    main()
