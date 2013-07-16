#!/usr/bin/env python

"""
    Routine for Differential Phase Constrast 
    
    Input: 
        parameter 1: 2D x 2D images path 
        parameter 2: output phase image name 
        parameter 3: output amplitude image name 
    Output:
        2D phase image, 2D amplitude image
    Example:
        $> python DPC.py 'SOFC/' 'phase.tif' 'amplitude.tif'
        or
        $> python DPC.py
"""

import sys
import time
import numpy as np
import scipy as sp
import Image as im

def diffPhaseContrast(dpc_path, dpc_phase, dpc_amp):
    #do something here
    phase = np.zeros((256, 256))
    amp = np.zeros((256, 256))
    
    cx = 128
    cy = 128
    cx1 = 100
    cy1 = 100
    cx2 = 140
    cy2 = 140
    radius = 60**2
    radius1 = 10**2
    radius2 = 15**2
    for i in np.arange(256):
        for j in np.arange(256):
            if ((cx - i)*(cx - i) + (cy - j)*(cy - j)) <= radius:
                phase[i][j] = 128
                amp[255-i][255-j] = 128
            if ((cx1 - i)*(cx1 - i) + (cy1 - j)*(cy1 - j)) <= radius1:
                phase[i][j] = 255
                amp[255-i][255-j] = 255
            if ((cx2 - i)*(cx2 - i) + (cy2 - j)*(cy2 - j)) <= radius2:
                phase[i][j] = 64
                amp[255-i][255-j] = 64
    
    #save to files
    im.fromarray(np.uint8(phase)).save(dpc_phase)
    im.fromarray(np.uint8(amp)).save(dpc_amp)


if __name__ == '__main__':
    # set default values
    dpc_path = ''
    dpc_phase = 'output1.tif'
    dpc_amp = 'output2.tif'
    
    if len(sys.argv) == 4:
        dpc_path = sys.argv[1]
        dpc_phase = sys.argv[2]
        dpc_amp = sys.argv[3]
    elif len(sys.argv) != 1:
        raise "Please enter the path and output filenames (phase and amplitude)"
        exit()
    
    diffPhaseContrast(dpc_path, dpc_phase, dpc_amp)
    