import os
import logging
from groq import Groq

def transcribe_with_groq(GROQ_API_KEY, audio_filepath, stt_model="whisper-large-v3"):
    """Transcribe audio using Groq's Whisper API"""
    try:
        client = Groq(api_key=GROQ_API_KEY)
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )
            return transcription.text
    except Exception as e:
        logging.error(f"Transcription error: {str(e)}")
        return None