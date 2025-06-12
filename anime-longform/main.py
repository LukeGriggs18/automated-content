from utils.openai_utils import generate_text
from utils.elevenlabs_utils import generate_speech_with_timestamps, save_audio_from_base64
from utils.ffmpeg_utils import generate_srt_from_alignment, burn_subtitles

def main():
    script_prompt = "Create a script focussing on hard work and personal growth. The script will be used for a youtube channel, it should have an engaging opening that draws to a conclusion throughout. Focus on personal growth, suffering, success, hardwork and other similiar topics as you see fit."
    system_prompt = "You are a thoughtful, powerfull narrator who writes short motivational scripts designed to inspire deep personal reflection. Your style is calm, introspective, and emotionally resonant. You focus on motivating the listener. Your flow is rhythmic capturing the listener. You write in a emagogic oratorical style. You use concise storytelling to communicate powerful ideas about growth, discipline, discomfort, and transformation. RESPONSE: Aim to produce scripts that are about 1 minute long when spoken. The response should only include the script, no additional information. Do not use archaiec language. Your response it being sent to a text to speach model (elevenlabs) so only use punctuation to dicatate the tempo."
    
    script = generate_text(system_prompt, script_prompt)

   # response = generate_speech_with_timestamps(script)

    audio_path = "output/voiceover.mp3"
    subtitle_path = "output/subtitles.srt"
    background_image = "black.png" 
    final_video_path = "output/final_video.mp4"

   # save_audio_from_base64(response.audio_base_64, audio_path)
   # generate_srt_from_alignment(response.alignment, subtitle_path)

    burn_subtitles(audio_path, subtitle_path, final_video_path, background_image, duration=60)

if __name__ == "__main__":
    main()
