#!/usr/bin/env python3
"""
Fetch YouTube video transcript with timestamps.
Usage: python fetch_transcript.py VIDEO_ID
"""

import sys
import os

def fetch_transcript(video_id):
    """Fetch transcript using youtube-transcript-api"""
    from youtube_transcript_api import YouTubeTranscriptApi

    # Create transcripts directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    transcripts_dir = os.path.join(os.path.dirname(script_dir), "transcripts")
    os.makedirs(transcripts_dir, exist_ok=True)

    output_file = os.path.join(transcripts_dir, f"{video_id}.txt")

    # Try different languages in order
    languages = ['zh-TW', 'zh-CN', 'zh-Hant', 'zh-Hans', 'en']

    transcript = None
    for lang in languages:
        try:
            transcript = YouTubeTranscriptApi().fetch(video_id, languages=[lang])
            print(f"Successfully fetched transcript with language: {lang}")
            break
        except Exception as e:
            print(f"Failed to fetch with language {lang}: {e}")
            continue

    if transcript is None:
        # Try without language specification
        try:
            transcript = YouTubeTranscriptApi().fetch(video_id)
            print("Successfully fetched transcript (default language)")
        except Exception as e:
            print(f"Failed to fetch transcript: {e}")
            sys.exit(1)

    # Write transcript with timestamps
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in transcript:
            start = entry.start
            # Convert to HH:MM:SS format
            hours = int(start // 3600)
            minutes = int((start % 3600) // 60)
            seconds = int(start % 60)
            if hours > 0:
                timestamp = f"[{hours:02d}:{minutes:02d}:{seconds:02d}]"
            else:
                timestamp = f"[{minutes:02d}:{seconds:02d}]"

            text = entry.text
            f.write(f"{timestamp} {text}\n")

    print(f"Transcript saved to: {output_file}")
    return output_file

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fetch_transcript.py VIDEO_ID")
        sys.exit(1)

    video_id = sys.argv[1]
    fetch_transcript(video_id)
