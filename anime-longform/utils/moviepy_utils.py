from moviepy import AudioFileClip, concatenate_videoclips

def get_audio_duration(audio_path):
    audio = AudioFileClip(audio_path)
    return audio.duration

def save_concatenated_video(clips, output_path, fps=60):
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=fps)
    for clip in clips:
        clip.close()