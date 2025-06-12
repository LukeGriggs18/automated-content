import ffmpeg
import traceback




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

    srt_lines = []
    line_words, line_start = [], None

    for i, w in enumerate(words):
        if not line_words:
            line_start = w["start"]
        line_words.append(w["word"])
        line_end = w["end"]

        if len(line_words) >= max_words_per_line or i == len(words) - 1:
            srt_lines.append({
                "start": line_start,
                "end": line_end,
                "text": " ".join(line_words)
            })
            line_words, line_start = [], None

    with open(output_file, "w", encoding="utf-8") as f:
        for idx, entry in enumerate(srt_lines, 1):
            f.write(f"{idx}\n")
            f.write(f"{seconds_to_srt_timestamp(entry['start'])} --> {seconds_to_srt_timestamp(entry['end'])}\n")
            f.write(f"{entry['text']}\n\n")

    print(f"SRT saved to {output_file}")

def burn_subtitles(audio_path, subtitle_path, output_path="output/final_video.mp4", background_image="black.jpg", duration=60):
    try:
        # Step 1: Load background image as video and scale
        video_input = ffmpeg.input(background_image, loop=1, framerate=25, t=duration)
        scaled_video = video_input.filter('scale', 'trunc(iw/2)*2', 'trunc(ih/2)*2')

        # Step 2: Burn subtitles
        video_with_subs = scaled_video.filter('subtitles', subtitle_path, force_style='Alignment=2')

        # Step 3: Load audio
        audio = ffmpeg.input(audio_path)

        # Step 4: Output combined video and audio
        (
            ffmpeg
            .output(
                video_with_subs,  # Video stream after subtitles
                audio.audio,      # Audio stream
                output_path,
                vcodec='libx264',
                acodec='aac',
                **{'b:v': '3000k', 'b:a': '192k'},
                shortest=None,
                pix_fmt='yuv420p'
            )
            .overwrite_output()
            .run()
        )

        print(f"Final video with subtitles saved to {output_path}")

    except Exception as e:
        print("FFmpeg error:")
        traceback.print_exc()

