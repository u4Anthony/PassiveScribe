#!/usr/bin/env python
import torch
from filechecker import Checker
from transcribe import transcribe

def device_check():
    if torch.cuda.is_available():
        device_type = 'cuda'
        print(f'GPU Acceleration available, utilizing cuda as Whisper device type.')
    else:
        device_type = 'cpu'
    return device_type

def callback(input_path, output_path, device_type, is_directory):
    print('callback')
    transcribe(input_path, output_path, device_type, is_directory)

def main():
    device_type = device_check()
    checker = Checker(device_type)
    checker.watch(callback)

if __name__ == '__main__':
    main()