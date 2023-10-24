#!/usr/bin/env python
import os
import torch
from filechecker import Checker
from transcribe import transcribe

def device_check():
    if torch.cuda.is_available():
        device_type = 'cuda'
        print(f'GPU Acceleration available, Whisper device type set to CUDA.')
    else:
        device_type = 'cpu'
        print(f'Whisper device type set to CPU')
    return device_type

def callback(input_path, output_path, device_type, is_directory):
    print('callback')
    transcribe(input_path, output_path, device_type, is_directory)

def dir_init():
    print('Checking if RevInput directory exists...')
    if not os.path.exists('./RevInput'):
        os.makedirs('./RevInput')
        print('Created RevInput directory')
    else:
        print('RevInput already available for use')
    
    print('Checking if RevOutput directory exists...')
    if not os.path.exists('./RevOutput'):
        os.makedirs('./RevOutput/CompletedFiles')
        os.makedirs('./RevOutput/TranscriptOutput')
        print('Create RevOutput directory and subdirectories')
    elif os.path.exists('./RevOutput'):
        print('RevOutput already available for use, checking if subdirectories exist...')
        if not os.path.exists('./RevOutput/CompletedFiles'):
            os.makedirs('./RevOutput/CompletedFiles')
            print('Created CompletedFiles subdirectory')
        else:
            print('CompletedFiles already available for use')
        if not os.path.exists('./RevOutput/TranscriptOutput'):
            os.makedirs('./RevOutput/TranscriptOutput')
            print('Created TranscriptOutput subdirectory')
        else:
            print('TranscriptOutput already available for use')
        

def main():
    dir_init()
    device_type = device_check()
    checker = Checker(device_type)
    checker.watch(callback)

if __name__ == '__main__':
    main()