import os
import base64
from elevenlabs import ElevenLabs
from dotenv import load_dotenv

load_dotenv()
elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

def generate_speech_with_timestamps(text, voice_id="QmjByzWKP81NN7b1lfIQ", output_format="mp3_44100_192"):
    return elevenlabs_client.text_to_speech.convert_with_timestamps(
        voice_id=voice_id,
        text=text,
        output_format=output_format
    )

def save_audio_from_base64(audio_base64_str, filename):
    audio_bytes = base64.b64decode(audio_base64_str)
    with open(filename, "wb") as f:
        f.write(audio_bytes)
    print(f"Audio saved to {filename}")
