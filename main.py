#!/usr/bin/env python
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

def main():
    device_type = device_check()
    checker = Checker(device_type)
    checker.watch(callback)

if __name__ == '__main__':
    main()