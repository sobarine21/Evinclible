import os
import speech_recognition as sr
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)

def transcribe_audio_with_sphinx(audio_path):
    """Transcribe WAV audio file using CMU Sphinx."""
    recognizer = sr.Recognizer()

    try:
        # Open the audio file with SpeechRecognition
        with sr.AudioFile(audio_path) as source:
            logging.info(f"Processing {audio_path} for transcription...")
            audio_data = recognizer.record(source)

            # Perform transcription using CMU Sphinx
            logging.info("Transcribing audio using CMU Sphinx...")
            transcription = recognizer.recognize_sphinx(audio_data)
            logging.info("Transcription successful!")
            return transcription

    except FileNotFoundError:
        logging.error(f"File {audio_path} not found.")
    except Exception as e:
        logging.error(f"Error occurred during transcription: {e}")
    return None


def process_audio_files(audio_files):
    """Process a list of WAV audio files and transcribe."""
    results = {}

    for audio_file in audio_files:
        # Check if file exists
        if not os.path.exists(audio_file):
            logging.warning(f"Audio file {audio_file} does not exist.")
            results[audio_file] = "File not found"
            continue

        # Transcribe the audio file
        transcription = transcribe_audio_with_sphinx(audio_file)
        if transcription:
            results[audio_file] = transcription
        else:
            results[audio_file] = "Transcription failed"
    
    return results


# Example usage
if __name__ == "__main__":
    # List of WAV audio files to process (provide full paths)
    audio_files = [
        'path_to_audio_file1.wav',  # Replace with your audio file paths
        'path_to_audio_file2.wav',  # Replace with your audio file paths
        'path_to_audio_file3.wav',  # Replace with your audio file paths
    ]
    
    # Process and transcribe audio files
    results = process_audio_files(audio_files)

    # Output the transcription results
    for audio_file, result in results.items():
        print(f"Audio File: {audio_file}")
        print(f"Transcription: {result}\n")
