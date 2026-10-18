"""
Audio Transcriber Script

This script converts an MP3 audio file to WAV format, splits the WAV file into 60-second chunks,
and uses the Google Web Speech API to transcribe the audio chunks into text.

Dependencies:
- os
- logging
- speech_recognition
- pydub

Ensure you have the following installed:
- pydub: pip install pydub
- SpeechRecognition: pip install SpeechRecognition
- ffmpeg: Download from https://ffmpeg.org/download.html and add to your system's PATH

Usage:
1. Set the path to your MP3 file in the `mp3_file_path` variable.
2. Define the language of the MP3 file in the `language` variable.
3. Run the script.

The script will output the transcriptions of the audio chunks and combine them into a full transcription.
"""

import os
import logging
import speech_recognition as sr
from pydub import AudioSegment

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Path to your MP3 file
mp3_file_path = "path/to/your/audio.mp3"
wav_file_path = "converted_audio.wav"

# Convert MP3 to WAV
logging.info("Converting MP3 to WAV...")
audio = AudioSegment.from_mp3(mp3_file_path)
audio.export(wav_file_path, format="wav", parameters=["-ar", "16000", "-ac", "1"])
logging.info(f"WAV file saved to {wav_file_path}")

# Initialize Recognizer
recognizer = sr.Recognizer()

# Load the WAV audio file
audio = AudioSegment.from_wav(wav_file_path)

# Split the audio into 60-second chunks
chunk_length_ms = 60 * 1000  # 60 seconds in milliseconds
chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

# Directory to save temporary audio chunks
chunk_dir = "audio_chunks"
os.makedirs(chunk_dir, exist_ok=True)

# Define the language of the MP3 file
language = "en-EN"  # Example: English (United States)

# Process each chunk
transcriptions = []

for i, chunk in enumerate(chunks):
    chunk_filename = os.path.join(chunk_dir, f"chunk{i}.wav")
    chunk.export(chunk_filename, format="wav")
    logging.info(f"Processing chunk {i}...")

    with sr.AudioFile(chunk_filename) as source:
        audio_data = recognizer.record(source)
        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio_data, language=language)
            transcriptions.append(text)
            logging.info(f"Chunk {i} transcription: {text}")
        except sr.UnknownValueError:
            logging.warning(f"Chunk {i} could not be understood.")
        except sr.RequestError as e:
            logging.error(f"Could not request results from Google Web Speech API; {e}")

# Combine all transcriptions
full_transcription = " ".join(transcriptions)
logging.info(f"Full transcription: {full_transcription}")

# Print the final transcription
print("Final Transcription:")
print(full_transcription)

# Optional: Save the transcription to a file
with open("transcription.txt", "w", encoding="utf-8") as f:
    f.write(full_transcription)
logging.info("Transcription saved to transcription.txt.")
