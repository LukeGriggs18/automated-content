from moviepy import AudioFileClip, VideoFileClip, afx, concatenate_videoclips, CompositeAudioClip

def get_audio_duration(audio_path):
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    audio.close()
    return duration

def save_concatenated_video(clips, output_path, fps=60):
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=fps)
    for clip in clips:
        clip.close()

def combine_video_with_audio(video_path, music_path, voiceover_path, output_path):
    """
    Combine a video with both background music and voiceover using MoviePy.
    
    Args:
        video_path (str): Path to the input video file
        music_path (str): Path to the background music file
        voiceover_path (str): Path to the voiceover audio file
        output_path (str): Path where the output video will be saved
    """
    try:
        # Load all clips
        video = VideoFileClip(video_path)
        music = AudioFileClip(music_path)
        voiceover = AudioFileClip(voiceover_path)

        # If music is longer than video, trim it
        if music.duration > video.duration:
            music = music.with_duration(video.duration)
        
        # Adjust volumes (make music quieter to not overpower voiceover)
        music = music.with_effects([afx.MultiplyVolume(0.3)])  # Reduce music volume to 30%
        voiceover = voiceover.with_effects([afx.MultiplyVolume(1.0)])  # Keep voiceover at full volume

        # Combine audio tracks
        final_audio = CompositeAudioClip([music, voiceover])
        
        # Set the mixed audio to the video
        final_clip = video.with_audio(final_audio)

        # Write the final video
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        # Clean up
        video.close()
        music.close()
        voiceover.close()
        final_audio.close()
        final_clip.close()

        print(f"Successfully combined video with music and voiceover. Output saved at: {output_path}")
    except Exception as e:
        print(f"Error combining video with audio: {str(e)}")
        raise
