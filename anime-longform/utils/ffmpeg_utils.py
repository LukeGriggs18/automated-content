import ffmpeg
import traceback


def generate_ass_from_alignment(alignment, output_file="subtitles.ass", max_words_per_line=1):
    chars = alignment.characters
    starts = alignment.character_start_times_seconds
    ends = alignment.character_end_times_seconds

    words = []
    current_word, word_start, word_end = "", None, None

    for i, c in enumerate(chars):
        if c.strip() == "":
            if current_word:
                words.append({"word": current_word, "start": word_start, "end": word_end})
                current_word, word_start, word_end = "", None, None
            continue

        if not current_word:
            word_start = starts[i]
        current_word += c
        word_end = ends[i]

    if current_word:
        words.append({"word": current_word, "start": word_start, "end": word_end})

    # ASS header with centered alignment
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1280
PlayResY: 720

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,24,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,2,0,5,10,10,30,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    def format_ass_timestamp(seconds):
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        cs = int((seconds - int(seconds)) * 100)  # centiseconds
        return f"{h:01}:{m:02}:{s:02}.{cs:02}"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(header)

        line_words, line_start = [], None
        for i, w in enumerate(words):
            if not line_words:
                line_start = w["start"]
            line_words.append(w["word"])
            line_end = w["end"]

            if len(line_words) >= max_words_per_line or i == len(words) - 1:
                text = " ".join(line_words)
                start = format_ass_timestamp(line_start)
                end = format_ass_timestamp(line_end)
                f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{text}\n")
                line_words, line_start = [], None

    print(f"ASS subtitles saved to {output_file}")


def burn_subtitles(audio_path, subtitle_path, output_path, video_path):
    try:
        input_video = ffmpeg.input(video_path)
        input_voiceover = ffmpeg.input(audio_path)

        # Create filter for mixing audio
        mixed_audio = ffmpeg.filter([input_video.audio, input_voiceover.audio], 
                                  'amix', 
                                  inputs=2, 
                                  duration='longest')

        # Burn subtitles and combine streams
        (
            ffmpeg
            .output(
                input_video.video,
                mixed_audio,
                output_path,
                vf=f"ass={subtitle_path}",
                acodec='aac'
            )
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print("FFmpeg stderr:\n", e.stderr.decode())
        raise RuntimeError("ffmpeg failed")


def add_audio_to_video(video_path, audio_path, output_path):
    """
    Add an audio track to a video clip using ffmpeg.
    
    Args:
        video_path (str): Path to the input video file
        audio_path (str): Path to the audio file to add
        output_path (str): Path where the output video will be saved
    """
    try:
        input_video = ffmpeg.input(video_path)
        input_audio = ffmpeg.input(audio_path)

        # Mix the audio tracks with the video
        (
            ffmpeg
            .output(
                input_video,
                input_audio,
                output_path,
                acodec='aac',
                map=0,  # Map all streams from first input (video)
                map_metadata=0,  # Map metadata from first input
                shortest=None,  # End when shortest input ends
                vcodec='copy'  # Copy video codec to avoid re-encoding
            )
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
        print(f"Successfully added audio to video. Output saved at: {output_path}")
    except ffmpeg.Error as e:
        print("FFmpeg stderr:\n", e.stderr.decode())
        raise RuntimeError("ffmpeg failed to add audio to video")
    
def add_vignette(input_path, output_path, angle="PI/2", mode="forward"):
    """
    Adds a vignette effect to a video using ffmpeg-python.
    """
    try:
        filter_str = f'vignette=angle={angle}:mode={mode}'

        (
            ffmpeg
            .input(input_path)
            .output(
                output_path,
                vf=filter_str,
                vcodec='libx264',
                acodec='aac',
                audio_bitrate='192k',
                strict='experimental'  # for aac if needed
            )
            .run(overwrite_output=True)
        )

        print(f"Vignette applied. Saved to {output_path}")
    
    except ffmpeg.Error as e:
        print("❌ FFmpeg error:", str(e))


