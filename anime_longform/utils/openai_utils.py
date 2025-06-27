import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_text(system_prompt, prompt, temperature=1.0):
    response = openai_client.responses.create(
        model="gpt-4.1",
        input=[
            {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
            {"role": "user", "content": [{"type": "input_text", "text": prompt}]}
        ],
        temperature=temperature,
    )
    return response.output_text
