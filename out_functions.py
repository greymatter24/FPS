#!/usr/bin/env python
# -*- coding: utf-8 -*-

## out_functions.py
##
## Functions for writing output from FPS analysis
##
## Daniel Little <daniel DOT little AT unimelb DOT edu DOT au>

import os, re
import numpy as np
from scipy.stats import norm

def format_line(str_text, total_str_length):
    str_length = len(str_text)
    n_spaces = total_str_length - str_length
    formatted_line = str_text + (" " * n_spaces) + "\t"
    return formatted_line

def write_diagnostics(file_name, output_dir, speech_durations, pause_durations, optcut, slp_threshold, err, slp, slp_m, slp_s, slp_w, fitone, fitk, fitspeech):
    fname = re.sub('\.wav$', '', file_name)
    output_file = output_dir + os.sep + fname + '_output' + '.dat'
    str_length = 62  

    # Open the file
    fid = open(output_file, 'w')
    fid.write("### Temporal Parameters - FPS Short vs Long Pause Analysis ###\n")
    fid.write(file_name + "\n\n")
    
    fid.write(format_line("Number Of Speech-Pause", str_length) + "%d\n" % len(speech_durations))
    fid.write(format_line("Duration of Pause Component (ms)", str_length) + "%.2f\n" % sum(pause_durations))
    fid.write(format_line("Duration of Speech Component (ms)", str_length) + "%.2f\n" % sum(speech_durations))
    fid.write(format_line("Duration of Sample - Speech + Pause (ms)", str_length) + "%.2f\n" % (sum(pause_durations) + sum(speech_durations)))
    fid.write(format_line("Speech to Pause Ratio", str_length) + "%.2f\n" % np.divide(sum(speech_durations), sum(pause_durations)))
    fid.write("\n")

    fid.write(format_line("High vs. Low Energy Classification Threshold (log Energy)", str_length) + "%.2f\n" %  optcut)
    fid.write("\n")

    fid.write(format_line("Pause Minimum (Log ms)", str_length) + "%.2f\n" % min(np.log(pause_durations)))
    fid.write(format_line("Pause Maximum (Log ms)", str_length) + "%.2f\n" % max(np.log(pause_durations)))
    fid.write(format_line("Pause Mean (Log ms)", str_length) + "%.2f\n" % np.mean(np.log(pause_durations)))
    fid.write(format_line("Pause Standard Deviation (Log ms)", str_length) + "%.2f\n" % np.std(np.log(pause_durations)))
    fid.write("\n")

    fid.write(format_line("Pause Minimum (ms)", str_length) + "%.2f\n" % min(pause_durations))
    fid.write(format_line("Pause Maximum (Log ms)", str_length) + "%.2f\n" % max(pause_durations))
    fid.write(format_line("Pause Mean (Log ms)", str_length) + "%.2f\n" % np.mean(pause_durations))
    fid.write(format_line("Pause Standard Deviation (Log ms)", str_length) + "%.2f\n" % np.std(pause_durations))
    fid.write("\n")

    fid.write(format_line("Speech Minimum (Log ms)", str_length) + "%.2f\n" % min(np.log(speech_durations)))
    fid.write(format_line("Speech Maximum (Log ms)", str_length) + "%.2f\n" % max(np.log(speech_durations)))
    fid.write(format_line("Speech Mean (Log ms)", str_length) + "%.2f\n" % np.mean(np.log(speech_durations)))
    fid.write(format_line("Speech Standard Deviation (Log ms)", str_length) + "%.2f\n" % np.std(np.log(speech_durations)))
    fid.write("\n")

    fid.write(format_line("Speech Minimum (ms)", str_length) + "%.2f\n" % min(speech_durations))
    fid.write(format_line("Speech Maximum (Log ms)", str_length) + "%.2f\n" % max(speech_durations))
    fid.write(format_line("Speech Mean (Log ms)", str_length) + "%.2f\n" % np.mean(speech_durations))
    fid.write(format_line("Speech Standard Deviation (Log ms)", str_length) + "%.2f\n" % np.std(speech_durations))
    fid.write("\n")

    fid.write(format_line("Short vs. Long Pause Classification Threshold (Log ms)", str_length) + "%.2f\n" % slp_threshold)
    fid.write(format_line("Short vs. Long Pause Classification Threshold (Log ms)", str_length) + "%.2f\n" % np.exp(slp_threshold))
    fid.write(format_line("Proportion (misclass): Short as Long", str_length) + "%.2f\n" % err[0])
    fid.write(format_line("Proportion (misclass): Long as Short", str_length) + "%.2f\n" % err[1])
    fid.write("\n")

    fid.write(format_line("Proportion of data contained in short pause distribution", str_length) + "%.2f\n" % slp_w[0])
    fid.write(format_line("Predicted Number of Short Pauses", str_length) + "%d\n" % round(len(pause_durations) * slp_w[0]))
    fid.write(format_line("Actual Number of Short Pauses", str_length) + "%d\n" % sum(np.log(pause_durations) <= slp_threshold))
    fid.write("\n")

    fid.write(format_line("Short Pause Mean (Log ms)", str_length) + "%.2f\n" % slp_m[0])
    fid.write(format_line("Short Pause Standard Deviation (Log ms)", str_length) + "%.2f\n" % slp_s[0])
    fid.write(format_line("Short Pause Mean Real (ms)", str_length) + "%.2f\n" % np.exp(slp_m[0]))
    # I suspect that this value is wrong
    fid.write(format_line("Short Pause Standard Deviation Real (ms)", str_length) + "%.2f\n" % np.exp(slp_s[0]))
    fid.write("\n")

    fid.write(format_line("Proportion of data contained in long pause distribution", str_length) + "%.2f\n" % slp_w[1])
    fid.write(format_line("Predicted Number of Long Pauses", str_length) + "%d\n" % round(len(pause_durations) * slp_w[1]))
    fid.write(format_line("Actual Number of Long Pauses", str_length) + "%d\n" % sum(np.log(pause_durations) > slp_threshold))
    fid.write("\n")

    fid.write(format_line("Long Pause Mean (Log ms)", str_length) + "%.2f\n" % slp_m[1])
    fid.write(format_line("Long Pause Standard Deviation (Log ms)", str_length) + "%.2f\n" % slp_s[1])
    fid.write(format_line("Long Pause Mean Real (ms)", str_length) + "%.2f\n" % np.exp(slp_m[1]))
    fid.write(format_line("Long Pause Standard Deviation Real (ms)", str_length) + "%.2f\n" % np.exp(slp_s[1]))
    fid.write("\n")

    # Need to roll short pauses into adjacent speech and parse in the long pause and long speech data
    # Descriptive statistics for long pause data in log time
    # Descriptive statistics for long pause data in real time
    
    # Descriptive statistics for long speech data in log time
    # Descriptive statistics for long speech data in real time
     

    fid.write(format_line("Fit of Single Distribution to Pause Data (-lnL)", str_length) + "%.2f\n" % fitone)
    fid.write(format_line("Fit of k-Mixture Distribution to Pause Data (-lnL)", str_length) + "%.2f\n" % fitk)
    fid.write(format_line("Fit of Single Distribution to Speech Data (-lnL)", str_length) + "%.2f\n" % fitspeech)
    fid.close()

    return
