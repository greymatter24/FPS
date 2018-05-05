#!/usr/bin/env python
# -*- coding: utf-8 -*-

## aud_functions.py
##
## Functions for reading and processing audio files
##
## Daniel Little <daniel DOT little AT unimelb DOT edu DOT au>

import wave, os, math
import numpy as np
import audioop
from misc_functions import *
import scipy

def doAverage(x, fs, tr=5e-3):
    alpha = math.exp(-2.2/(fs*tr))
    #x_n = scipy.signal.lfilter(1-alpha, [1, -alpha], x**2)
    x_n = scipy.signal.filtfilt(1-alpha, [1, -alpha], abs(x**2))
    x_n = np.log(x_n)
    return x_n

def vad(x):
    minsd = 0.02
    minnsd = 0.015
    fs = 16000
    
    x_n = doAverage(x, fs)
    minval = np.mean(x_n) - 3.0 * np.std(x_n)
    maxval = np.mean(x_n) + 3.0 * np.std(x_n)
    x_n = x_n[(x_n > minval) & (x_n < maxval)]
    
    # TODO: EM algorithm to separate speech and pause
    
    return x_n

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
    x_n = vad(x_h)

  
 
    return
