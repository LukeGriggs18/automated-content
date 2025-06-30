from utils.openai_utils import generate_text
from utils.elevenlabs_utils import generate_speech_with_timestamps, save_audio_from_base64
from utils.ffmpeg_utils import *
from utils.gdrive_utils import download_clips_matching_duration
from utils.moviepy_utils import add_intro, add_outro, get_audio_duration, save_concatenated_video_with_transitions, combine_video_with_audio
import os
from dotenv import load_dotenv
from dataclasses import dataclass
from pathlib import Path



@dataclass
class VideoConfig:
    """Configuration for video generation"""
    profile_image: str = "images/bonsai.png"
    music_path: str = "music/track1.mp3"
    audio_path: str = "output/voiceover.mp3" 
    subtitle_path: str = "output/subtitles.ass"
    background_image: str = "black.png"
    final_video_path: str = "output/final_video.mp4"
    temp_concat_path: str = "output/concatenated.mp4"
    video_with_audio: str = "output/video_with_audio.mp4"
    video_with_vignette: str = "output/video_with_vignette.mp4"
    service_account_path: str = "service_account.json"

class ScriptGenerator:
    """Handles script generation using OpenAI"""
    
    def __init__(self):
        self.system_prompt = """You are a thoughtful, powerful narrator who writes short motivational scripts designed to inspire deep personal reflection. Your style is calm, introspective, and emotionally resonant. You focus on motivating the listener. Your flow is rhythmic capturing the listener. You write in a emagogic oratorical style. You use concise storytelling to communicate powerful ideas about growth, discipline, discomfort, and transformation. RESPONSE: Aim to produce scripts that are about 1 minute long when spoken. The response should only include the script, no additional information. Do not use archaic language. Your response is being sent to a text to speech model (elevenlabs) so only use punctuation to dictate the tempo. Do not hyphenate words, do not use the following punctuation { -, -,}."""
    
    def generate(self, topic_prompt: str) -> str:
        """Generate a motivational script based on the given prompt"""
        return generate_text(self.system_prompt, topic_prompt)

class AudioProcessor:
    """Handles audio generation and processing"""
    
    def generate_voiceover(self, script: str, audio_path: str, subtitle_path: str):
        """Generate voiceover and subtitles from script"""
        elevenlabs_response = generate_speech_with_timestamps(script)
        save_audio_from_base64(elevenlabs_response.audio_base_64, audio_path)
        generate_ass_from_alignment(elevenlabs_response.alignment, subtitle_path)
        return elevenlabs_response
    
    def get_duration(self, audio_path: str) -> float:
        """Get audio duration in seconds"""
        return get_audio_duration(audio_path)

class VideoProcessor:
    """Handles video processing operations"""
    
    def __init__(self, config: VideoConfig):
        self.config = config
    
    def download_and_concatenate_clips(self, duration: float):
        """Download clips from Google Drive and concatenate them"""
        folder_id = os.getenv("CLIPS_FOLDER_ID")
        clips = download_clips_matching_duration(
            self.config.service_account_path, 
            folder_id, 
            duration
        )
        save_concatenated_video_with_transitions(clips, self.config.temp_concat_path)
    
    def combine_audio_and_video(self):
        """Combine video with music and voiceover"""
        combine_video_with_audio(
            self.config.temp_concat_path,
            self.config.music_path,
            self.config.audio_path,
            self.config.video_with_audio
        )
    
    def add_effects(self):
        """Add vignette effect to video"""
        add_vignette(self.config.video_with_audio, self.config.video_with_vignette)
    
    def burn_subtitles(self):
        """Add subtitles to final video"""
        burn_subtitles(
            self.config.audio_path,
            self.config.subtitle_path,
            self.config.final_video_path,
            self.config.video_with_vignette
        )

    def add_intro(self):
        add_intro(self.config.profile_image, self.config.final_video_path)
    
    def add_outro(self):
        add_outro(self.config.profile_image, self.config.final_video_path)

class MotivationalVideoGenerator:
    """Main orchestrator class for generating motivational videos"""
    
    def __init__(self, config: VideoConfig = None):
        self.config = config or VideoConfig()
        self.script_generator = ScriptGenerator()
        self.audio_processor = AudioProcessor()
        self.video_processor = VideoProcessor(self.config)
        
        Path("output").mkdir(exist_ok=True)
    
    def generate_video(self, script_prompt: str):
        """Generate complete motivational video from script prompt"""
        print("Generating script...")
        script = self.script_generator.generate(script_prompt)
        
        print("Generating voiceover and subtitles...")
        self.audio_processor.generate_voiceover(
            script, 
            self.config.audio_path, 
            self.config.subtitle_path
        )
        
        print("Getting audio duration...")
        duration = self.audio_processor.get_duration(self.config.audio_path)
        
        print("Downloading and processing video clips...")
        self.video_processor.download_and_concatenate_clips(duration)
        
        print("Combining audio and video...")
        self.video_processor.combine_audio_and_video()
        
        print("Adding effects...")
        self.video_processor.add_effects()
        
        print("Burning subtitles...")
        self.video_processor.burn_subtitles()

        print("Adding intro...")
        self.video_processor.add_intro()

        print("Adding outro")
        self.video_processor.add_outro()

        print(f"Video generated successfully!")

class ContentUploader:
    """Handles uploading content"""
    def post_to_youtube(self, content_path: str):
        return
        
    def post_to_instagram(self, content_path: str ):
        return

def main():
    load_dotenv()
    
    script_prompt = """Create a script focusing on hard work and personal growth. The script will be used for a youtube channel, it should have an engaging opening that draws to a conclusion throughout. Focus on personal growth, suffering, success, hardwork and other similar topics as you see fit."""
    
    generator = MotivationalVideoGenerator()
    generator.generate_video(script_prompt)
    
    uploader = ContentUploader()
    uploader.post_to_youtube(generator.config.final_video_path)


if __name__ == "__main__":
    load_dotenv()
    main()
