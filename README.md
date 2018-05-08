# FPS
Fluency Profiling System BETA V0.1

To run, type:

       python fps.py
       
This will run the fps analysis on the first entry in filelist.txt (to be updated to allow multiple files to be run)

Requirements:

       Python Version 2.x (install from https://www.python.org/downloads/release/python-2715/)
       
       Python libraries:
       
              numpy
              
              scipy
              
              sklearn
              
              [others?]
       
       

=================================================================================================================================

TODO: Parse speech and pause durations into long speech and long pause, write diagnostics for long speech and long pause data
          
      Add Dirichlet process classification of speech and pause durations
      
      Add Breath classification
      
=================================================================================================================================

CHANGE LOG

180608 Added in ability to process multiple files
    
       Added progress bar

180608 BETA V0.1

180608 Added short-long pause classification
       
       Added computation of fit 
       
       Added write out of diagnostics

180507 Added conversion to float 16 from int16

       Added speech/nonspeech classification
       
       Added classification error removal

180506 Added EM to separate speech from pause
       
       Found thresholds

180505 Initial audio input set up
       
       Read in wav file from filelist.txt and plot
       
       Downsample wavform
       
       High pass filter
       
       Initial VAD
