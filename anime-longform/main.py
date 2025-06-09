import os
import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

client = OpenAI()

def generate_title(prompt):
    response = client.responses.create(
        model="gpt-4.1",
        input=prompt,
        temperature=1.0,
        top_p=1.0
    )
    return response.output_text

title_prompt = "invent a concise, impactful title for a motivational video. Be creative with the output. The title should be short and concise followed by a peroid (.). Relate it to any themes in the realm of personal development, suffering, success, life and any other similar topics. Make the prompt personal, call out the viewer, make it"
script_prompt = "Write a 1-minute motivational script for a YouTube channel.Do not include any instructions on audio or video. Your only job is to write the script. Only include the words to be spoken by the narrator. The tone should be thoughtful, inspiring, and slightly philosophical. Focus on the idea that real growth often comes from embracing discomfort and uncertainty, and that the struggle itself is what shapes us into stronger, better versions of ourselves. Use vivid imagery and a calm, reflective voice."

title = generate_title(title_prompt)
#script = generate(script_prompt)

print(title)