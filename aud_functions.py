#!/usr/bin/env python
# -*- coding: utf-8 -*-

## aud_functions.py
##
## Functions for reading and processing audio files
##
## Daniel Little <daniel DOT little AT unimelb DOT edu DOT au>

import wave, os
import numpy as np
import matplotlib.pyplot as plot

def plot_wavform(audio):
    signal = audio.readframes(-1)
    signal = np.frombuffer(signal, dtype='Int16')
    fs = audio.getframerate() 
    #
    if audio.getnchannels()==2:
        # Split data into channels
        channels = [[] for channel in range(audio.getnchannels())]
        for index, datum in enumerate(signal):
            channels[index%len(channels)].append(datum)
    else:
        channels = signal

    # plot
    plot.figure(1)
    plot.title("Signal Wave")
    for channel in channels:
        ts = np.linspace(0, len(channel)/fs, num = len(channel))
        plot.plot(ts, channel)
    plot.show()
    return


def read_audio_file(filename):
    audio = wave.open(filename, "r")
    return audio

def process_audio(fileloc, filelist):
    #for i in range(0, len(filelist)):
    fn = fileloc + os.sep + filelist[0]
    audio = read_audio_file(fn)

    # Test
    plot_wavform(audio)       
 
    return
