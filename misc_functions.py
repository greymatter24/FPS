#!/usr/bin/env python
# -*- coding: utf-8 -*-

## misc_functions.py
##
## Miscellaneous Functions for FPS
##
## Daniel Little <daniel DOT little AT unimelb DOT edu DOT au>
import matplotlib.pyplot as plot
import numpy as np

def split_and_plot_wavform(audio):
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

def plot_channel(audio, fs):
    audio = np.fromstring(audio, dtype='Int16')
    ts = np.linspace(0, len(audio)/fs, num = len(audio))
    plot.plot(ts, audio)
    plot.show()
    return

def splitaudio_old(audio, whichchannel):
    signal = audio.readframes(-1)
    signal = np.frombuffer(signal, dtype='Int16')

    # Preallocate list
    channels = [[] for channel in range(audio.getnchannels())]

    # Split data into channels
    for index, datum in enumerate(signal):
        channels[index%len(channels)].append(datum)
    if audio.getnchannels()==2:
        if whichchannel == "left":
            audio = channels[0]
        else:
            audio = channels[1]
    else:
        audio = channels[0]
    return audio

def plotEM(em, data):
    x = np.linspace(min(data), max(data))
    logprob = em.score_samples(x.reshape(-1,1))
    pdf = np.exp(logprob)
    responsibilities = em.predict(x.reshape(-1,1))    
    pdf_individual=responsibilities * pdf[:,np.newaxis]
    fig = plot.figure()
    ax=fig.add_subplot(111)
    ax.hist(x_n, 30, normed=True, histtype="stepfilled", alpha = .4)
    ax.plot(x,pdf, '-k')
    ax.plot(x, pdf_individual, '--k')
    ax.text(0.04, 0.96, "Best-fit mixture", ha="left", va="top",transform=ax.transAxes)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$p(x)$")
    plot.show()
    return
