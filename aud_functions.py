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
from em_functions import *
from scipy import signal
from scipy.stats import norm
from operator import itemgetter
from sklearn.mixture import GaussianMixture as GMM

def flatten_list(x):
    f = lambda i: [item for sublist in i for item in sublist]
    flattened_list = f(x)    
    return flattened_list

def find_threshold(em, index1, index2):
    n = 101 # support
    k = em.n_components
    m = flatten_list(em.means_.tolist())
    s = flatten_list(flatten_list(em.covariances_.tolist()))
    w = em.weights_.tolist()
    ss = [j for _,j in sorted(zip(m,s))]
    sw = [j for _,j in sorted(zip(m,w))]
    sm = sorted(m)
    low = min(np.add(sm, map(lambda x: x * -3, ss)))
    high = max(np.add(sm, map(lambda x: x * 3, ss)))
    step = (high - low)/(n - 1.)
    x = np.arange(low, high, step)
    e = np.add(sw[index1] * (1 - norm.cdf(x, sm[index1], ss[index1])), sw[index2] * norm.cdf(x, sm[index2], ss[index2]))
    midx = min(enumerate(e), key=itemgetter(1))[0]
    threshold = x[midx]
    return threshold

def do_average(x, fs, tr=5e-3):
    alpha = math.exp(-2.2/(fs*tr))
    #x_n = scipy.signal.lfilter(1-alpha, [1, -alpha], x**2)
    x_n = signal.filtfilt(1-alpha, [1, -alpha], abs(x**2))
    x_n = np.log(x_n)
    return x_n

def vad(x):
    minsd = 0.02
    minnsd = 0.015
    fs = 16000
    x_n = do_average(x, fs)
    minval = np.mean(x_n) - 3.0 * np.std(x_n)
    maxval = np.mean(x_n) + 3.0 * np.std(x_n)
    x_n = x_n[(x_n > minval) & (x_n < maxval)]
    gmm = GMM(n_components=3, covariance_type="full", tol=1e-3, n_init=5)
    em = gmm.fit(x_n.reshape(-1,1)) # 1D input need to reshape to 2D 
    thresholds = [[] for t in range(em.n_components-1)]
    thresholds[0] = find_threshold(em, 0, 1)
    thresholds[1] = find_threshold(em, 1, 2)
    return em, x_n, thresholds

def highpass(data, fs, cutoff=300.0):
    cutoff = 300.0
    hpf = signal.firwin(65, cutoff/(fs/2), pass_zero=False)
    x_h = signal.lfilter(hpf, 1, x)
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
    em, x_n, thresholds = vad(x_h)

  
 
    return
