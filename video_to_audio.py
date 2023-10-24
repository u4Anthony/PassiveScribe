#!/usr/bin/env python
import subprocess

# it is necessary to extract video audio to .wav for speaker diatrization
def convert_video_to_audio(video_file_path, audio_file_path):
    command = f'ffmpeg -i \"{video_file_path}\" -vn -ar 44100 -ac 2 -b:a 192k \"{audio_file_path}\"'
    subprocess.call(command, shell=True)

convert_video_to_audio(r'./RevOutput/CompletedFiles/A Time for Choosing by Ronald Reagan.mp4', './RevOutput/CompletedFiles/audio.wav')