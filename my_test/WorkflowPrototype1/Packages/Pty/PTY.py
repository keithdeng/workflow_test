#!/usr/bin/env python

"""
    Routine for Ptychography 
    
    Input: 
        parameter 1: n x 2D images path 
        parameter 2: output image name 1
        parameter 3: output image name 2
    Output:
        2 2D output images
    Example:
        $> python PTY.py '' 'output1.tif' 'output2.tif'
        or
        $> python PTY.py
"""

import sys
import time
import numpy as np
import scipy as sp
import Image as im

def ptychography(pty_path, pty_out1, pty_out2):
    """
    Ptychography reconstruction routine
    """
    #do something here
    pty1 = np.zeros((256, 256))
    pty2 = np.zeros((256, 256))
    
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
                pty1[i][j] = 128
                pty2[255-i][255-j] = 128
            if ((cx1 - i)*(cx1 - i) + (cy1 - j)*(cy1 - j)) <= radius1:
                pty1[i][j] = 255
                pty2[255-i][255-j] = 255
            if ((cx2 - i)*(cx2 - i) + (cy2 - j)*(cy2 - j)) <= radius2:
                pty1[i][j] = 64
                pty2[255-i][255-j] = 64
    
    #save to files
    im.fromarray(np.uint8(pty1)).save(pty_out1)
    im.fromarray(np.uint8(pty2)).save(pty_out2)


if __name__ == '__main__':
    # set default values
    pty_path = ''
    pty_out1 = 'output1.tif'
    pty_out2 = 'output2.tif'
    
    if len(sys.argv) == 4:
        pty_path = sys.argv[1]
        pty_out1 = sys.argv[2]
        pty_out2 = sys.argv[3]
    elif len(sys.argv) != 1:
        raise "Please enter the path and output filenames (out1 and out2)"
        exit()
    
    ptychography(pty_path, pty_out1, pty_out2)
    
