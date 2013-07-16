#!/usr/bin/env python

"""
    Routine for Fluorescence Maps 
    
    Input: 
        parameter 1: 2D x 1D line profiles path
        parameter 2: output maps image name 
    Output:
        2D maps image
    Example:
        $> python MAPS.py 'PEAKS/' 'maps.tif'
        or
        $> python MAPS.py
"""

import sys
import time
import numpy as np
import scipy as sp
import Image as im

def maps(maps_path, maps_image):
    #do something here
    maps = np.zeros((256, 256))
    
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
                maps[i][j] = 128
            if ((cx1 - i)*(cx1 - i) + (cy1 - j)*(cy1 - j)) <= radius1:
                maps[i][j] = 255
            if ((cx2 - i)*(cx2 - i) + (cy2 - j)*(cy2 - j)) <= radius2:
                maps[i][j] = 64
    
    #save to files
    im.fromarray(np.uint8(maps)).save(maps_image)


if __name__ == '__main__':
    # set default values
    maps_path = ''
    maps_image = 'maps.tif'
    
    if len(sys.argv) == 3:
        maps_path = sys.argv[1]
        maps_image = sys.argv[2]
    elif len(sys.argv) != 1:
        raise "Please enter the path and output filename"
        exit()
    
    maps(maps_path, maps_image)
    