#!/usr/bin/env python

"""
    Routine for Tomography reconstruction 
    
    Input: 
        parameter 1: n x 2D images path 
        parameter 2: output volume path
    Output:
        1 stack of 2D images as a 3D volume
    Example:
        $> python TOMO.py '' ''
        or
        $> python TOMO.py
"""

import sys
import time
import numpy as np
import scipy as sp
import Image as im

def tomography(tomo_path, tomo_vol_path):
    """
    Tomography reconstruction routine
    """
    #do something here
    tomo = np.zeros((256, 256))
    
    cx = 128
    cy = 128
    cx1 = 100
    cy1 = 100
    cx2 = 140
    cy2 = 140
    radius = 60**2
    radius1 = 10**2
    radius2 = 15**2
    for k in np.arange(4):
        for i in np.arange(256):
            for j in np.arange(256):
                if ((cx - i)*(cx - i) + (cy - j)*(cy - j)) <= radius:
                    tomo[i][j] = 128 - k*10
                if ((cx1 - i)*(cx1 - i) + (cy1 - j)*(cy1 - j)) <= radius1:
                    tomo[i][j] = 255 - k*10
                if ((cx2 - i)*(cx2 - i) + (cy2 - j)*(cy2 - j)) <= radius2:
                    tomo[i][j] = 64 + k*10
        #save to files
        filename = tomo_vol_path + str(k) + '.tif'
        im.fromarray(np.uint8(tomo)).save(filename)

if __name__ == '__main__':
    # set default values
    tomo_path = ''
    tomo_vol_path = ''
    
    if len(sys.argv) == 3:
        tomo_path = sys.argv[1]
        tomo_vol_path = sys.argv[2]
    elif len(sys.argv) != 1:
        raise "Please enter the path and output file path"
        exit()
    
    tomography(tomo_path, tomo_vol_path)
    
