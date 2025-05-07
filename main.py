#!/usr/bin/env python3
"""
A Python script to download YouTube videos as MP3 files using yt-dlp and FFmpeg.

Usage:
    python youtube_to_mp3_downloader.py <video_url> [-o OUTPUT_DIR] [--ffmpeg-location FFMPEG_PATH]

Requirements:
    - Python 3.6+
    - yt-dlp: pip install yt-dlp
    - FFmpeg installed and in your PATH, or specify the path with --ffmpeg-location
      * On Ubuntu/Debian: sudo apt-get install ffmpeg
      * On macOS (Homebrew): brew install ffmpeg

Example:
    python youtube_to_mp3_downloader.py \
        https://www.youtube.com/watch?v=HGC5E5m17Fg \
        -o /home/user/Music \
        --ffmpeg-location /usr/bin/ffmpeg
"""
import argparse
import sys
from yt_dlp import YoutubeDL


def download_audio(url: str, output_dir: str, ffmpeg_location: str = None) -> None:
    """
    Download the audio from a YouTube video and convert it to MP3.

    :param url: YouTube video URL
    :param output_dir: Directory where the MP3 file will be saved
    :param ffmpeg_location: Path to FFmpeg binaries (ffmpeg and ffprobe)
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'noplaylist': True,
    }

    if ffmpeg_location:
        # yt-dlp expects the directory containing ffmpeg binaries
        ydl_opts['ffmpeg_location'] = ffmpeg_location

    try:
        with YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading and converting: {url}")
            ydl.download([url])
            print("Download complete! MP3 saved to ", output_dir)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Download YouTube video audio as MP3 using yt-dlp.'
    )
    parser.add_argument(
        'url', help='URL of the YouTube video'
    )
    parser.add_argument(
        '-o', '--output', default='.',
        help='Output directory (default: current directory)'
    )
    parser.add_argument(
        '--ffmpeg-location', default=None,
        help='Path to FFmpeg binaries if not in PATH'
    )
    args = parser.parse_args()

    download_audio(args.url, args.output, args.ffmpeg_location)


if __name__ == '__main__':
    main()