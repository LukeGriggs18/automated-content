from moviepy import AudioFileClip, VideoFileClip, afx, concatenate_videoclips, CompositeAudioClip, ImageClip
from moviepy.video.fx import FadeIn, FadeOut
import moviepy.video.fx as vfx

def add_intro(image="images/bonsai.png"):
    image = ImageClip("")
    return

def add_outro():
    return

def get_audio_duration(audio_path):
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    audio.close()
    return duration

def save_concatenated_video(clips, output_path, fps=30):
    final = concatenate_videoclips(clips, method="compose")
    final.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=fps)
    for clip in clips:
        clip.close()

def save_concatenated_video_with_transitions(clips, output_path, fps=30, transition_duration=0.5):
    if len(clips) <= 1:
        # No transitions needed for single clip
        final = clips[0] if clips else None
    else:
        # Create crossfade transitions between clips
        transition_clips = []
        
        for i in range(len(clips)):
            if i == 0:
                # First clip - fade out at end only
                clip = clips[i].with_effects([FadeOut(transition_duration)])
            elif i == len(clips) - 1:
                # Last clip - fade in at start only
                clip = clips[i].with_effects([FadeIn(transition_duration)])
            else:
                # Middle clips - fade in at start and fade out at end
                clip = clips[i].with_effects([
                    FadeIn(transition_duration),
                    FadeOut(transition_duration)
                ])
            
            transition_clips.append(clip)
        
        # Concatenate with overlapping transitions
        final = concatenate_videoclips(transition_clips, method="compose")
    
    if final:
        final.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=fps)
    
    # Clean up
    for clip in clips:
        clip.close()
    if final:
        final.close()

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

        if music.duration > video.duration:
            music = music.with_duration(video.duration)
        
        music = music.with_effects([afx.MultiplyVolume(0.3)])  
        voiceover = voiceover.with_effects([afx.MultiplyVolume(1.0)])  

        final_audio = CompositeAudioClip([music, voiceover])
        final_clip = video.with_audio(final_audio)

        
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        
        video.close()
        music.close()
        voiceover.close()
        final_audio.close()
        final_clip.close()

        print(f"Successfully combined video with music and voiceover. Output saved at: {output_path}")
    except Exception as e:
        print(f"Error combining video with audio: {str(e)}")
        raise
