#!/usr/bin/env python
# -*- coding: utf-8 -*-

## misc_functions.py
##
## Miscellaneous Functions for FPS
##
## Daniel Little <daniel DOT little AT unimelb DOT edu DOT au>
import matplotlib.pyplot as plot
import numpy as np


def parse_speech_and_pause_old(pause_durations, speech_durations, threshold, first_onset_speech):
    n_speech = len(speech_durations)
    n_pause = len(pause_durations)
    n_long_pauses = sum(np.log(pause_durations) >= threshold)
    speech_flag = [True] * n_speech
    short_pause_flag = np.log(pause_durations) < threshold
    if first_onset_speech == 0: # pause first
        all_d = [a for b in zip(pause_durations, speech_durations) for a in b]
        all_f = [a for b in zip(short_pause_flag, speech_flag) for a in b]
        if n_pause > n_speech:
            all_d.append(pause_durations[len(pause_durations)-1])
    else:
        all_d = [a for b in zip(speech_durations, pause_durations) for a in b]
        all_f = [a for b in zip(speech_flag, short_pause_flag) for a in b]
        if n_speech > n_pause:
            all_d.append(speech_durations[len(speech_durations)-1])
    flag = [1-int(x) for x in all_f] # Tag pause durations
    flag.insert(0, 1) # Add tag to beginning
    flag.append(1)    # Add tag to end
    # Find repeated speech tags (i.e., short pauses) and sum them
    a = [i for i, x in enumerate(np.diff(flag) == 1) if x]
    b = [i for i, x in enumerate(np.diff(flag) == -1) if x]
    idx = zip([x-1 for x in a], [x-1 for x in b])
    long_pause_durations = [None] * (n_long_pauses  + (n_pause - n_speech))
    long_speech_durations = [None] * (n_long_pauses + (n_speech - n_pause))
    for i in range(0, len(idx)):    
        if idx[i][1] >= 0:
            long_pause_durations[i] = all_d[idx[i][1]]    
        else:         
            long_pause_durations[i] = 0
        long_speech_durations[i] = sum([all_d[j] for j in range(idx[i][1]+1, idx[i][0]+1)])
    long_pause_durations = [i for (i,v) in zip(long_pause_durations, [x != 0 for x in long_pause_durations]) if v]
    long_pause_durations = [x for x in long_pause_durations if x is not None]
    long_speech_durations = [x for x in long_speech_durations if x is not None]
    return long_pause_durations, long_speech_durations

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
    ax.hist(data, 30, normed=True, histtype="stepfilled", alpha = .4)
    ax.plot(x,pdf, '-k')
    #ax.plot(x, pdf_individual, '--k')
    ax.text(0.04, 0.96, "Best-fit mixture", ha="left", va="top",transform=ax.transAxes)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$p(x)$")
    plot.show()
    return
