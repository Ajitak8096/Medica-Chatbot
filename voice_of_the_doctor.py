import os
import platform
import subprocess
from elevenlabs import save
from elevenlabs.client import ElevenLabs
from gtts import gTTS

# Initialize clients
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=ELEVENLABS_API_KEY) if ELEVENLABS_API_KEY else None

def play_audio(filepath):
    """Play audio file using system default player"""
    try:
        if platform.system() == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{filepath}").PlaySync()'])
        elif platform.system() == "Darwin":
            subprocess.run(['afplay', filepath])
        else:  # Linux
            subprocess.run(['aplay', filepath])
    except Exception as e:
        print(f"Playback error: {str(e)}")

def text_to_voice_with_elevenlabs(input_text, output_filepath="response.mp3"):
    """Main text-to-speech function with fallback to gTTS"""
    try:
        # Try ElevenLabs first
        if client:
            audio = client.generate(
                text=input_text[:1000],  # Truncate long text
                voice="Rachel",
                model="eleven_turbo_v2"
            )
            save(audio, output_filepath)
            play_audio(output_filepath)
            return output_filepath
    except Exception:
        pass  # Fall through to gTTS
    
    # Fallback to gTTS
    try:
        tts = gTTS(text=input_text, lang='en')
        tts.save(output_filepath)
        play_audio(output_filepath)
        return output_filepath
    except Exception as e:
        print(f"TTS Error: {str(e)}")
        return None