import os
import json
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

def generate_speach_with_timestamps():
    response = elevenlabs_client.text_to_speech.convert_with_timestamps(
        voice_id="QmjByzWKP81NN7b1lfIQ",
        text="There is a moment—quiet, almost invisible—when you feel the pull to choose comfort, to stay right where you are. It’s tempting, that familiar place. Safe. Predictable. But growth never blooms in comfort’s shadow. Everything you dream of becoming waits beyond the easy path.",
        output_format="mp3_44100_192"
        )
    return response

def save_audio_from_base64(audio_base64_str, filename):
    # Decode the base64 string into bytes
    audio_bytes = base64.b64decode(audio_base64_str)
    
    # Write the bytes to a file
    with open(filename, "wb") as audio_file:
        audio_file.write(audio_bytes)

    print(f"Audio saved to {filename}")

def seconds_to_srt_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

def generate_srt_from_alignment(alignment, output_file="subtitles.srt", max_words_per_line=4):
    chars = alignment.characters
    starts = alignment.character_start_times_seconds
    ends = alignment.character_end_times_seconds

    # Step 1: Extract words with their start/end times
    words = []
    current_word = ""
    word_start = None
    word_end = None

    for i, c in enumerate(chars):
        if c.strip() == "":  # space or whitespace
            if current_word:
                words.append({
                    "word": current_word,
                    "start": word_start,
                    "end": word_end
                })
                current_word = ""
                word_start = None
                word_end = None
            continue

        if current_word == "":
            word_start = starts[i]
        current_word += c
        word_end = ends[i]

    # Add last word if needed
    if current_word:
        words.append({
            "word": current_word,
            "start": word_start,
            "end": word_end
        })

    # Step 2: Group words into subtitle lines
    srt_lines = []
    line_words = []
    line_start = None
    line_end = None

    for i, w in enumerate(words):
        if not line_words:
            line_start = w["start"]
        line_words.append(w["word"])
        line_end = w["end"]

        # If max words reached or last word, write line
        if len(line_words) >= max_words_per_line or i == len(words) - 1:
            srt_lines.append({
                "start": line_start,
                "end": line_end,
                "text": " ".join(line_words)
            })
            line_words = []
            line_start = None
            line_end = None

    # Step 3: Write to SRT file
    with open(output_file, "w", encoding="utf-8") as f:
        for idx, entry in enumerate(srt_lines, 1):
            start_ts = seconds_to_srt_timestamp(entry["start"])
            end_ts = seconds_to_srt_timestamp(entry["end"])
            f.write(f"{idx}\n")
            f.write(f"{start_ts} --> {end_ts}\n")
            f.write(f"{entry['text']}\n\n")

    print(f"SRT saved to {output_file}")

def main():
    title_system_prompt = "You generate short, memorable, and emotionally resonant video titles. Each title is designed to intrigue and inspire, often using metaphor, contradiction, or impactful phrasing. You focus on engaging the viewer, grabbing their interest by resonating with them personally. \n\nRESPONSE:\nYou produce outputs with one title\nYou do not inlcude quotation marks\nEach title ends with a period (.)"
    title_prompt = "invent a concise, impactful title for a motivational video. Be creative with the output. The title should be short and concise followed by a peroid (.). Relate it to any themes in the realm of personal development, suffering, success, life and any other similar topics. Make the prompt personal, call out the viewer, make it"
    #title = generate_text(title_system_prompt, title_prompt, 1.7)

    script_system_prompt ="You are a thoughtful, powerfull narrator who writes short motivational scripts designed to inspire deep personal reflection. Your style is calm, introspective, and emotionally resonant. You focus on motivating the listener. Your flow is rhythmic capturing the listener. You write in a emagogic oratorical style. You use concise storytelling to communicate powerful ideas about growth, discipline, discomfort, and transformation. RESPONSE: Aim to produce scripts that are about 1 minute long when spoken. The response should only include the script, no additional information. Do not use archaiec language. Your response it being sent to a text to speach model (elevenlabs) so only use punctuation to dicatate the tempo."
    script_prompt = "Create a script focussing on hard work and personal growth. The script will be used for a youtube channel, it should have an engaging opening that draws to a conclusion throughout. Focus on personal growth, suffering, success, hardwork and other similiar topics as you see fit."
    #script = generate_text(script_system_prompt, script_system_prompt, 1.0)

    ellevenlabs_response = generate_speach_with_timestamps()

    audio_base64_str = ellevenlabs_response.audio_base_64
    save_audio_from_base64(audio_base64_str, "voiceover.mp3")

    alignment = ellevenlabs_response.alignment
    generate_srt_from_alignment(alignment, "subtitles.srt")
    print(alignment)

if __name__ == "__main__":
    main()   


