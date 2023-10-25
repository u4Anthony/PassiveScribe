#!/usr/bin/env python
import logging
import os
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
        audio_file_path = os.path.splitext(input)[0] + "_audio.wav"
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
    audio = convert_video_to_audio(input)
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
    with open(f'{output_path}/TranscriptOutput/{filename}_transcript.txt', 'w', encoding='utf-8') as transcript_file:
        transcript_file.write(transcription_text)

def move_completed(input_path, output_path, filename):
    print(f'Attempting to move {filename} to {output_path}/CompletedFiles directory...')
    os.rename(f'{input_path}/{filename}', f'{output_path}/CompletedFiles/{filename}')
    print(f'Successfully moved file {filename}')

def move_unsupported(input_path, output_path, filename):
    print(f'Unsupported file format for: {filename} \r\nSupported file formats are: {SUPPORTED_FORMATS}')
    
    print(f'Attempting to move {filename} to {output_path}/UnsupportedFiles directory...')
    os.rename(f'{input_path}/{filename}', f'{output_path}/UnsupportedFiles/{filename}')
    print(f'Successfully moved file {filename}')
