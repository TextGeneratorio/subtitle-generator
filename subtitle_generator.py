import argparse

import requests
import os
import youtube_dl

API_KEY = os.getenv("TEXT_GENERATOR_API_KEY")
if API_KEY is None:
    raise Exception(
        "Please set TEXT_GENERATOR_API_KEY environment variable, login to https://text-generator.io to get your API key")
headers = {"secret": API_KEY}


def get_subtitles_for_audio_file(audio_file, output_file, output_filetype="srt"):
    audio_params = {
        "translate_to_english": False,
        "output_filetype": output_filetype,
    }

    files = {'audio_file': (audio_file, open(audio_file, 'rb'))}
    response = requests.post(
        "https://api.text-generator.io/api/v1/audio-file-extraction",
        files=files,
        data=audio_params,
        headers=headers
    )
    results = response.text
    print(results)
    with open(output_file, "wb") as f:
        f.write(results)
    print(f"Finished, written results to file {output_file}")


def get_subtitles_for_yt_video(video_url, output_file):
    print("Downloading video: ", video_url)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192'
        }],
        'postprocessor_args': [
            '-ar', '16000'
        ],
        'prefer_ffmpeg': True,
        'keepvideo': False,
        # download to temp file
        # 'outtmpl': '/tmp/audio.wav'
        # download to memory
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url], )
        audio_filename = ydl.prepare_filename(ydl.extract_info(video_url))

        # with open(audio_bytes, "rb") as f:
        #     audio_bytes = f.read()
        print("Download + conversion complete")
        print("Requesting subtitles from text-generator.io")
        # change extension to be .wav
        audio_filename = ".".join(audio_filename.split(".")[:-1]) + ".wav"

        get_subtitles_for_audio_file(audio_filename, output_file)


if __name__ == "__main__":
    # video_url and output_file are required
    parser = argparse.ArgumentParser(
        description="Generate subtitles for a youtube video"

    )
    parser.add_argument("--video_url", type=str, required=True)
    parser.add_argument("--output_file", type=str, required=True)
    args = parser.parse_args(
    )
    get_subtitles_for_yt_video(args.video_url, args.output_file)
