#!/usr/bin/env python
import logging
import os
import re
import subprocess
import whisper
from whisper.utils import get_writer

from constants import (
    SUPPORTED_FORMATS,
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Main transcription function
def transcribe(input_path, output_path, device_type, is_directory):
    if is_directory:
        for filename in os.listdir(input_path):
            if [filename for format in SUPPORTED_FORMATS if(format in filename)]:
                print(f'Transcribing file: {filename}')
                try:
                    # attempt to transcribe the file
                    transcription_text = create_transcription(filename, device_type)

                    # output the text to a file with the same file name
                    move_transcription(output_path, filename, transcription_text)
                    
                    # move successfully transcribed file to completed directory
                    move_completed(input_path, output_path, filename)

                except Exception as e:
                    # TODO log the exception error to file
                    logger.exception(e)
            else:
                move_unsupported(input_path, output_path, filename)
    else:
        # get file name from path
        filename = os.path.basename(input_path)
        path = os.path.dirname(input_path)
        if [filename for format in SUPPORTED_FORMATS if(format in filename)]:
            print(f'Transcribing file: {filename}')
            try:
                # attempt to transcribe the file
                transcription_text = create_transcription(input_path, device_type)

                # output the text to a file with the same file name
                move_transcription(output_path, filename, transcription_text)

                # move successfully transcribed file to completed directory
                move_completed(path, output_path, filename)
                
            except Exception as e:
                # TODO log the exception error to file
                logger.exception(e)
        else:
            move_unsupported(path, output_path, filename)

# Transcription functions parts
def convert_video_to_audio(input):
    try:
        input_file_name = os.path.splitext(input)[0].replace('./RevInput\\', '')
        audio_file_path = f'./Audio/{input_file_name}.wav'
        command = f'ffmpeg -i \"{input}\" -vn -ar 44100 -ac 2 -b:a 192k \"{audio_file_path}\"'
        subprocess.call(command, shell=True)
        return audio_file_path
    except Exception as e:
        # TODO log the exceptiopn error to file
        logger.exception(e)

def language_check(audio):
    model = whisper.load_model("base")
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    return f'{max(probs, key=probs.get)}'

def choose_model(audio, device_type):
    language = language_check(audio)
    if device_type == 'cuda':
        model = whisper.load_model('large')
    else:
        model = whisper.load_model('medium')
        if language == 'en':
            model = whisper.load_model('medium.en')
        else:
            model = whisper.load_model('medium')
    return model, language

def create_transcription(input, device_type):
    audio_path = convert_video_to_audio(input)
    audio = whisper.load_audio(audio_path)
    logging.debug(f'DEBUG - {audio}')
    model, language = choose_model(audio, device_type)
    # mel = whisper.log_mel_spectrogram(audio).to(model.device)
    # for some reason the spectrogram does not work properly in the transcribe() function
    if device_type == 'cuda':
        transcription_text = model.transcribe(audio=audio, language=language, without_timestamps=False)
    else:
        try:
            transcription_text = model.transcribe(audio=audio, language=language, without_timestamps=False, fp16=False)
        except Exception as e:
            logger.exception(e)
    return transcription_text['text'], transcription_text['segments']

# File Movement Functions
def move_transcription(output_path, filename, transcription_text):
    filename = os.path.splitext(filename)[0]

    print(f'Saving transcription to {filename}_transcript.txt in {output_path}/TranscriptOutput directory...')
    with open(f'{output_path}/TranscriptOutput/{filename}_transcript.vtt', 'w', encoding='utf-8') as transcript_file:
        transcript_file.write(f'WEBVTT \n\n') # the space after webvtt is REQUIRED
        # logging.debug(transcription_text)
        for item in transcription_text[1]:
            start = format_time(item.get('start'))
            end = format_time(item.get('end'))
            transcript_file.write(f'{start} --> {end}\n')
            transcript_file.write(f'- {item.get("text").lstrip()}\n\n')

def move_completed(input_path, output_path, filename):
    print(f'Attempting to move {filename} to {output_path}/CompletedFiles directory...')
    os.rename(f'{input_path}/{filename}', f'{output_path}/CompletedFiles/{filename}')
    print(f'Successfully moved file {filename}')

def move_unsupported(input_path, output_path, filename):
    print(f'Unsupported file format for: {filename} \r\nSupported file formats are: {SUPPORTED_FORMATS}')
    
    print(f'Attempting to move {filename} to {output_path}/UnsupportedFiles directory...')
    os.rename(f'{input_path}/{filename}', f'{output_path}/UnsupportedFiles/{filename}')
    print(f'Successfully moved file {filename}')

def format_time(time):
    # desired format 00:00:00.000
    # hh:mm:ss.zzz
    time = float(time)
    if time == 0.0:
        formatted_time = '00:00:00.000'
    else:
        minutes = time // 60
        hours = time // 3600
        seconds = time - (minutes * 60)
        formatted_time = "{:02}:{:02}:{:06.3f}".format(int(hours), int(minutes), seconds)

    return formatted_time
