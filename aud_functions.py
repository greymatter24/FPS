#!/usr/bin/env python
# -*- coding: utf-8 -*-

## aud_functions.py
##
## Functions for reading and processing audio files
##
## Daniel Little <daniel DOT little AT unimelb DOT edu DOT au>

## TODO: Take out misc_functions import
import wave, os, math, struct, copy, audioop, re, sys
import numpy as np
from misc_functions import *
from out_functions import *
from scipy import signal
from scipy.stats import norm
from operator import itemgetter
from sklearn.mixture import GaussianMixture as GMM
from sklearn.mixture import BayesianGaussianMixture as BGM 

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben
    return

def compute_fit_mixture(data, gmm_output):
    m, s, w = get_mix_parms(gmm_output)
    n_k = len(m)
    fit = 0.0
    for i in range(0, n_k):
        fit = fit - (sum(norm.logpdf(np.log(data), m[i], s[i]) * w[i]))
    return fit

def compute_fit_single(data):
    fit = -sum(norm.logpdf(np.log(data), np.mean(np.log(data)), np.std(np.log(data))))
    return fit

def compute_classification_error(slp_threshold, slp):
    slp_m, slp_s, slp_w = get_mix_parms(slp)
    err = [slp_w[0] * (1. - norm.cdf(slp_threshold, slp_m[0], slp_s[0])), slp_w[1] * (norm.cdf(slp_threshold, slp_m[1], slp_s[1]))]
    return err

def parse_speech_and_pause(pause_durations, speech_durations, threshold, first_onset_speech):
    # create a listof durations
    n_speech = len(speech_durations)
    n_pause = len(pause_durations)

    # correct for different list sizes
    if n_pause > n_speech: # More pause than speech (implies pause first)
        speech_durations.append(0.0)
        n_speech = len(speech_durations)
    elif n_speech > n_pause: # More speech than pause (implies pause first)
        pause_durations.insert(0, 0.0)
        n_pause = len(pause_durations)

    # Combine vectors
    all_d = zip(pause_durations, speech_durations)
    
    n_long_pause = sum(pause_durations > np.exp(threshold))

    # Preallocate
    long_pause_durations = [None] * (n_long_pause + 1)
    long_speech_durations = [None] * (n_long_pause + 1)

    # Assign first entry
    if all_d[0][0] >= np.exp(threshold):
        lp = all_d[0][0]
        ls = all_d[0][1]
    else:
        lp = 0.0
        ls = all_d[0][0] + all_d[0][1]

    counter = -1
    for i in range(1,n_pause):
        if all_d[i][0] < np.exp(threshold):
            ls = ls + all_d[i][0] + all_d[i][1]
        else:
            counter = counter + 1
            long_pause_durations[counter] = lp
            long_speech_durations[counter] = ls
            lp = all_d[i][0]
            ls = all_d[i][1]
    counter = counter + 1
    long_pause_durations[counter] = lp
    long_speech_durations[counter] = ls
    
    long_pause_durations = [x for x in long_pause_durations if x is not None]
    long_pause_durations = [x for x in long_pause_durations if x != 0]
    long_speech_durations = [x for x in long_speech_durations if x is not None]
    long_speech_durations = [x for x in long_speech_durations if x != 0]
    return long_pause_durations, long_speech_durations

def em_slp(log_pause_durations, n_components):
    slp_gmm = GMM(n_components, covariance_type="full", tol=1e-4, n_init=20)
    slp = slp_gmm.fit(log_pause_durations.reshape(-1,1)) 
    return slp

def compute_durations(x_s, tfs, targ_idx = 0):
    vec = copy.deepcopy(x_s)
    if targ_idx == 1:
        vec = [1 - x for x in vec]
    else:
        vec = [x for x in vec]
    vec.insert(0, 1) # Add 1 to beginning
    vec.append(1)    # Add 1 to end
    a = [i for i, x in enumerate(np.diff(vec) == 1) if x]
    b = [i for i, x in enumerate(np.diff(vec) == -1) if x]
    lengths = [a_i - b_i for a_i, b_i in zip(a, b)]
    durations = [x * 1./tfs for x in lengths]
    return durations

def remove_short_segments(invec, fs, min_dur, targ_idx=1):
    outvec = copy.deepcopy(invec)
    if targ_idx == 1:
        non_targ_idx = 0
    else:
        non_targ_idx = 1
    N = len(outvec)
    #
    onset = -1
    for i in range(0,N):
        if np.logical_and(outvec[i] == targ_idx, onset == -1):
             onset = i
        #
        if np.logical_and(outvec[i] == non_targ_idx, onset != -1):
            if ((i - onset) * (1./fs)) < min_dur:
                pos = range(onset,i)
                targ = np.full((len(pos)), non_targ_idx)
                for x,y in zip(pos, targ):
                    outvec[x] = y
            #
            onset = -1
        #    
    return outvec

def classify_speech(x_n, opt_cutoff):
    speech = np.zeros((len(x_n)))
    speech[np.nonzero(x_n > opt_cutoff)[0]] = 1
    return speech

def get_opt_cutoff(weights, thresholds):
    if weights[0] >= .01:
        opt_cut = thresholds[0]
    else:
        opt_cut = thresholds[2]
    return opt_cut    

def flatten_list(x):
    f = lambda i: [item for sublist in i for item in sublist]
    flattened_list = f(x)    
    return flattened_list

def find_threshold(mix, index1, index2):
    n = 101 # support
    sm, ss, sw = get_mix_parms(mix)
    low = min(np.add(sm, map(lambda x: x * -3, ss)))
    high = max(np.add(sm, map(lambda x: x * 3, ss)))
    step = (high - low)/(n - 1.)
    x = np.arange(low, high, step)
    e = np.add(sw[index1] * (1 - norm.cdf(x, sm[index1], ss[index1])), sw[index2] * norm.cdf(x, sm[index2], ss[index2]))
    midx = min(enumerate(e), key=itemgetter(1))[0]
    threshold = x[midx]
    return threshold

def get_mix_parms(mix):
    k = mix.n_components
    m = flatten_list(mix.means_.tolist())
    s = flatten_list(flatten_list(mix.covariances_.tolist()))
    w = mix.weights_.tolist()
    ss = [j for _,j in sorted(zip(m,s))]
    sw = [j for _,j in sorted(zip(m,w))]
    sm = sorted(m)
    return sm, ss, sw

def do_average(x, tfs, tr=5e-3):
    alpha = math.exp(-2.2/(tfs*tr))
    #x_n = signal.lfilter([1.-alpha], [1., -alpha], abs(x**2))
    x_n = signal.filtfilt([1.-alpha], [1., -alpha], abs(x**2.), axis=0)
    x_n = np.log(x_n)
    return x_n

def smooth_data(x, tfs=16000):
    x_n = do_average(x, tfs)
    minval = np.mean(x_n) - 3.0 * np.std(x_n)
    maxval = np.mean(x_n) + 3.0 * np.std(x_n)
    x_n = x_n[(x_n > minval) & (x_n < maxval)]
    return x_n

def vad(x_n, n_components, method = "em"):
    if method.lower() in ["em"]:
        gmm = GMM(n_components, covariance_type="full", tol=1e-3, n_init=5)
        mix = gmm.fit(x_n.reshape(-1,1)) # 1D input need to reshape to 2D 
    elif method.lower() in ["dpgmm"]:
        gmm = BGM(n_components, covariance_type="full", tol=1e-3, n_init=1)
        mix = gmm.fit(x_n.reshape(-1,1)) # 1D input need to reshape to 2D 
    thresholds = [[] for t in range(mix.n_components-1)]
    thresholds[0] = find_threshold(mix, 0, 1)
    thresholds[1] = find_threshold(mix, 1, 2)
    return mix, thresholds

def highpass(data, fs, cutoff=300.0):
    cutoff = 300.0
    hpf = signal.firwin(65, cutoff/(fs/2), pass_zero=False)
    x_h = signal.lfilter(hpf, 1, data)
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

def process_audio(par, filelist, index):
    progress(0, 100, suffix='')
    fn = par["audio_directory"] + os.sep + filelist[index]
    audio = read_audio_file(fn)
    n_frames = audio.getnframes()
    audio_data = audio.readframes(n_frames)

    # Low pass filter data
    fs = audio.getframerate() 
    tfs = 16000 # target frequency
    lp = lowpass(audio_data, fs, tfs) 
    progress(10, 100, suffix='')

    # Separate stereo data into channels
    channel = splitaudio(lp, "left")
    progress(20, 100, suffix='')
 
    # Convert from bytes to float 16
    x_i = np.fromstring(channel, dtype='Int16')
    x = [float(val) / pow(2, 15) for val in x_i]
    progress(30, 100, suffix='')
 
    # High pass filter data
    x_h = highpass(x, tfs)
    progress(40, 100, suffix='')

    # Do Voice Activity Detection
    x_n = smooth_data(x_h, tfs = 16000)
    mix, thresholds = vad(x_n, int(par["n_sp_components"]), par["classification_method"])
    progress(50, 100, suffix='')

    # Get EM model parameters
    m, s, w = get_mix_parms(mix)

    # Classify speech and nonspeech
    optcut = get_opt_cutoff(w, thresholds)

    # Get vector of 1 = speech, 0 = pause
    x_s = classify_speech(x_n, optcut)

    # Remove segments which are too short
    x_s = remove_short_segments(x_s, tfs, float(par["minimum_speech_duration"]), 1)
    progress(60, 100, suffix='')

    x_s = remove_short_segments(x_s, tfs, float(par["minimum_nonspeech_duration"]), 0)
    progress(70, 100, suffix='')

    # Compute speech durations from class vector
    speech_durations = compute_durations(x_s, tfs, 1)

    # Compute pause durations from class vector
    pause_durations = compute_durations(x_s, tfs, 0)

    # Write out speech and pause durations
    write_durations(filelist[index], par["output_directory"], pause_durations, speech_durations, "_speech_pause_durations", ["Pause_Durations", "Speech_Durations"])
    progress(80, 100, suffix='')

    # Run EM algorithm on log pauses
    slp = em_slp(np.log(pause_durations), int(par["n_slp_components"]))
    slp_m, slp_s, slp_w = get_mix_parms(slp)
    progress(90, 100, suffix='')

    # Find optimal cutoff between distributions  
    slp_threshold = find_threshold(slp, 0, 1)  

    # Compute classification error rate
    err = compute_classification_error(slp_threshold, slp)
    
    # Compute fits
    fitone = compute_fit_single(pause_durations)
    fitk = compute_fit_mixture(pause_durations, slp)
    fitspeech = compute_fit_single(speech_durations)

    # Parse times into long pause and long speech data
    lpd, lsd = parse_speech_and_pause(pause_durations, speech_durations, slp_threshold, x_s[0]) # problem with CharnReliability.wav
    
    # Write diagnostics
    write_diagnostics(filelist[index], par["output_directory"], speech_durations, pause_durations, optcut, slp_threshold, err, slp, slp_m, slp_s, slp_w, fitone, fitk, fitspeech, lpd, lsd) 
    write_durations(filelist[index], par["output_directory"], lpd, lsd, "_final_durations", ["Pause_Durations", "Speech_Durations"])
    progress(100, 100, suffix='')
    return

def process_audio_list(par, filelist):
    for i in range(0, len(filelist)):
         print("\n Processing" + " " + filelist[i] + "\n")
         process_audio(par, filelist, i)
    return
