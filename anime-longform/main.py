from utils.openai_utils import generate_text
from utils.elevenlabs_utils import generate_speech_with_timestamps, save_audio_from_base64
from utils.ffmpeg_utils import *
from utils.gdrive_utils import download_clips_matching_duration
from utils.moviepy_utils import get_audio_duration, save_concatenated_video_with_transitions, combine_video_with_audio
import os
from dotenv import load_dotenv

def main():
    script_prompt = "Create a script focussing on hard work and personal growth. The script will be used for a youtube channel, it should have an engaging opening that draws to a conclusion throughout. Focus on personal growth, suffering, success, hardwork and other similiar topics as you see fit."
    system_prompt = "You are a thoughtful, powerfull narrator who writes short motivational scripts designed to inspire deep personal reflection. Your style is calm, introspective, and emotionally resonant. You focus on motivating the listener. Your flow is rhythmic capturing the listener. You write in a emagogic oratorical style. You use concise storytelling to communicate powerful ideas about growth, discipline, discomfort, and transformation. RESPONSE: Aim to produce scripts that are about 1 minute long when spoken. The response should only include the script, no additional information. Do not use archaiec language. Your response is being sent to a text to speach model (elevenlabs) so only use punctuation to dicatate the tempo. Do not use the following - - that is do not use EM dashes."
    # script = generate_text(system_prompt, script_prompt)
    # elevenlabs_response = generate_speech_with_timestamps(script)
    # save_audio_from_base64(elevenlabs_response.audio_base_64, audio_path)
    # generate_ass_from_alignment(elevenlabs_response.alignment, subtitle_path)

    music_path = "music/track1.mp3"
    audio_path = "output/voiceover.mp3"
    subtitle_path = "output/subtitles.ass"
    background_image = "black.png"
    final_video_path = "output/final_video.mp4"
    temp_concat_path = "output/concatenated.mp4"
    video_with_audio = "output/video_with_audio.mp4"
    video_with_vignette = "output/video_with_vignette.mp4"

    service_account_path = "service_account.json"
    folder_id = os.getenv("CLIPS_FOLDER_ID")

    #total_duration = get_audio_duration(audio_path)
    #clips = download_clips_matching_duration(service_account_path, folder_id, total_duration)
    #save_concatenated_video_with_transitions(clips, temp_concat_path)

    # Combine video with music and voiceover
   # combine_video_with_audio(temp_concat_path, music_path, audio_path, video_with_audio)

    # Add vignette effect to combined video
    add_vignette(video_with_audio, video_with_vignette)

    # Burn subtitles onto the vignette video
    burn_subtitles(audio_path, subtitle_path, final_video_path, video_with_vignette)
    

if __name__ == "__main__":
    load_dotenv()
    main()
