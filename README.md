# FPS
Fluency Profiling System BETA V1.0: This version of the FPS is a port from Matlab to Python. The present version differs from the version in Little2012 in the following ways: (1) There is currently no breath classification algorithm implemented. Otherwise the details match the details of the FPS described in papers/Little2012 [FPS].pdf

To run, type:

       python fps.py
       
from the command window.

This will run the fps analysis on the first entry in filelist.txt (to be updated to allow multiple files to be run)

Requirements:

       Python Version 2.x (install from https://www.python.org/downloads/release/python-2715/)
              
              Windows Users should use the: https://www.python.org/ftp/python/2.7.15/python-2.7.15.amd64.msi install file
              
                     Python will be installed to C:\Python27
              
                     You will also need to add Python to the Windows path
                     
                     You can modify the Windows path by right-clicking "My Computer" in the start menu, then clicking "Properties", and then clicking "Advanced system settings" in the left bar. 
                     
                     Click "Environment Variables..." in the menu that comes up, and find "Path" in the bottom window (named "System variables"). 
                     
                     Add the text ;C:\Python27; C:\Python27\Scripts; to the end of your Path. 
                     
                     
       
       Python libraries:
       
              numpy, scipy
              
                     These libraries can be downloaded here: https://www.scipy.org/scipylib/download.html
              
              sklearn
              
                     Once you've installed numpy and scipy, you can install sklearn by opening a command/terminal window typing:
                     
                     pip install -U scikit-learn
                     
                     (You might need to navigate to C:\Python27\Scripts\ first, but if you have added that location to the path then pip should work from the command line)
                     
                     To open a terminal on windows, go to the start menu, in the search bar, type cmd and press enter
                     
        
==============================================================================


Files:

       fps.py - Main file to run the FPS 
       
       fps_functions.py - Functions for reading input files and calling the audio processing functions
       
       aud_functions.py - Functions for processing audio using FPS
       
       out_functions.py - Functions for writing output from FPS
       
       misc_functions.py - Some earlier versions of functions and code for plotting 
       
       filelist.txt - list of .wav files (located in /audio) for processing
            
       /audio/ - Folder for placing .wav files for processing
       
       /output/ - Folder containing output of FPS
       
       /papers/ - Contains relevant publications about FPS (note that the Python version is a simplified version of the one published in Little2012.pdf
       
       /parameters/ - Contains the settings.par file which has some basic parameter settings for the FPS
==============================================================================

TODO: Add Breath classification
      
==============================================================================

CHANGE LOG

180510 V1.0 Major Upgrade

       Added DP-GMM option for energy classification

180510 Added duration output

180509 Fixed several bugs in parse_speech_and_pause function 

180508 Added in ability to process multiple files
    
       Added progress bar
       
       Added parse speech and pause durations into long speech and long pause, write diagnostics for long speech and long pause data

180508 BETA V0.1

180508 Added short-long pause classification
       
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
