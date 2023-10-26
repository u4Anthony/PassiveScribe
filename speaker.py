#!/usr/bin/env python
import whisper
import datetime
import subprocess

import torch
import pyannote.audio
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding

from pyannote.audio import Audio
from pyannote.core import Segment

import wave
import contextlib

from sklearn.cluster import AgglomerativeClustering
import numpy as np

embedding_model = PretrainedSpeakerEmbedding("speechbrain/-ecapspkreca-voxceleb", device=torch.device("cuda"))

def speaker_transcribe(path):
    model = whisper.load_model('large')
    result = model