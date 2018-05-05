#!/usr/bin/env python
# -*- coding: utf-8 -*-

## fps_functions.py
##
## Functions for running the Fluency Profiling System.
##
## Daniel Little <daniel DOT little AT unimelb DOT edu DOT au>

from aud_functions import *
import re, os

## Loading parameters from saved files.
def load_parameter_file(parameter_filename):
    res = {}
    comment_pattern = re.compile("^#")
    key_value_pattern = re.compile(".*\W*=\W*.*")
    with open(parameter_filename, 'r') as fp:
        for line in fp: 
            if comment_pattern.match(line):
                continue
            if key_value_pattern.match(line):
                key, value = re.split("\W*=\W*", line)
                res[key.strip()] = value.strip()
    return res

def load_fps_settings(parameter_directory):
    parameter_file = parameter_directory + os.sep + "settings.par"
    return load_parameter_file(parameter_file)

def load_settings(parameter_directory):
    res = load_fps_settings(parameter_directory)
    return res

def read_audio_filenames(filename):
    res = []
    with open(filename, 'r') as fp:
        # Read filenames and strip newline character
        res = [r.rstrip("\n") for r in fp]
    return res

def run_fps(audio_list_filename):
    
    ## Load the system settings.
    par = load_settings("./parameters")

    filelist = read_audio_filenames("filelist.txt")
    process_audio(par["audio_directory"], filelist)


    return filelist
