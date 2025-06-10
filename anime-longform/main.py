import os
import openai
import base64
from openai import OpenAI
from dotenv import load_dotenv
from elevenlabs import ElevenLabs


load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI()

elevenlabs_client = ElevenLabs(
    api_key= os.getenv("ELEVENLABS_API_KEY")
)

def generate_text(system_prompt, prompt, temp):
    response = openai_client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role":"system", 
                "content": [
                    {
                    "type": "input_text",
                    "text": system_prompt
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                    "type": "input_text",
                    "text": prompt
                    }
                ]
            },

        ],
        temperature=temp,
    )
    return response.output_text

def generate_voice():

    response = elevenlabs_client.text_to_speech.convert_with_timestamps(
        voice_id="QmjByzWKP81NN7b1lfIQ",
        text="There is a moment—quiet, almost invisible—when you feel the pull to choose comfort, to stay right where you are. It’s tempting, that familiar place. Safe. Predictable. But growth never blooms in comfort’s shadow. Everything you dream of becoming waits beyond the easy path.",
        output_format="mp3_44100_192"
        )

    audio_base64_str = response.audio_base_64
    save_audio_from_base64(audio_base64_str, "output.mp3")

    print(response.json())


def save_audio_from_base64(audio_base64_str, filename="output.mp3"):
    # Decode the base64 string into bytes
    audio_bytes = base64.b64decode(audio_base64_str)
    
    # Write the bytes to a file
    with open(filename, "wb") as audio_file:
        audio_file.write(audio_bytes)

    print(f"Audio saved to {filename}")

title_system_prompt = "You generate short, memorable, and emotionally resonant video titles. Each title is designed to intrigue and inspire, often using metaphor, contradiction, or impactful phrasing. You focus on engaging the viewer, grabbing their interest by resonating with them personally. \n\nRESPONSE:\nYou produce outputs with one title\nYou do not inlcude quotation marks\nEach title ends with a period (.)"
title_prompt = "invent a concise, impactful title for a motivational video. Be creative with the output. The title should be short and concise followed by a peroid (.). Relate it to any themes in the realm of personal development, suffering, success, life and any other similar topics. Make the prompt personal, call out the viewer, make it"
#title = generate_text(title_system_prompt, title_prompt, 1.7)

script_system_prompt ="You are a thoughtful, powerfull narrator who writes short motivational scripts designed to inspire deep personal reflection. Your style is calm, introspective, and emotionally resonant. You focus on motivating the listener. Your flow is rhythmic capturing the listener. You write in a emagogic oratorical style. You use concise storytelling to communicate powerful ideas about growth, discipline, discomfort, and transformation. RESPONSE: Aim to produce scripts that are about 1 minute long when spoken. The response should only include the script, no additional information. Do not use archaiec language. Your response it being sent to a text to speach model (elevenlabs) so only use punctuation to dicatate the tempo."
script_prompt = "Create a script focussing on hard work and personal growth. The script will be used for a youtube channel, it should have an engaging opening that draws to a conclusion throughout. Focus on personal growth, suffering, success, hardwork and other similiar topics as you see fit."
#script = generate_text(script_system_prompt, script_system_prompt, 1.0)

voice_mp3 = generate_voice()

