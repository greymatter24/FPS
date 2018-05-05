#!/usr/bin/env python
# -*- coding: utf-8 -*-

## aud_functions.py
##
## Functions for reading and processing audio files
##
## Daniel Little <daniel DOT little AT unimelb DOT edu DOT au>

import wave, os
import numpy as np
import audioop
from misc_functions import *
import scipy

def highpass(data, fs, cutoff=300.0):
    cutoff = 300.0
    hpf = scipy.signal.firwin(65, cutoff/(fs/2), pass_zero=False)
    x_h = scipy.signal.lfilter(hpf, 1, x)
    return x_h

def lowpass(data, fs, tfs):
    # resample data
    rc = audioop.ratecv(data, 2, 2, fs, tfs, None)
    return rc
    
def splitaudio(audio, whichchannel="left"):
    if whichchannel == "left":
        channel = audioop.tomono(audio[0], 2, 1, 0)
    else:
        channel = audioop.tomono(audio[1], 2, 1, 0)
    return channel

def read_audio_file(filename):
    wavfile = open(filename, 'rb')
    audio = wave.open(wavfile)
    return audio

def process_audio(fileloc, filelist):
    #for i in range(0, len(filelist)):
    fn = fileloc + os.sep + filelist[0]
    audio = read_audio_file(fn)

    n_frames = audio.getnframes()
    audio_data = audio.readframes(n_frames)

    # Low pass filter data
    fs = audio.getframerate() 
    tfs = 16000 # target frequency
    lp = lowpass(audio_data, fs, tfs) 

    # Separate stereo data into channels
    channel = splitaudio(lp, "left")
    x = np.fromstring(channel, dtype='Int16')
 
    # High pass filter data
    x_h = highpass(x, tfs)

    # Do Voice Activity Detection


    #plot_wavform(audio)

   
 
    return
