#!/usr/bin/env python
import whisper

model = whisper.load_model("base")

# load audio and pad/trim it to fit 30 seconds
audio = whisper.load_audio("./test.mp4")
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio).to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
options = whisper.DecodingOptions(fp16=False)
result = whisper.decode(model, mel, options)

# print the recognized text
print(result.text)

print("\r\n-----------------------------\r\n")

model = whisper.load_model("base")
temp_result = model.transcribe(audio=mel)

print(temp_result["text"])



# model = whisper.load_model("large")
# result = model.transcribe("test.mp4")
# print(result["text"])