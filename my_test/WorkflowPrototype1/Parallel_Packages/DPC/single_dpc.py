#! /local/bin/env python

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imsave
from scipy.optimize import fmin
from time import time
import Image

def rss(v, xdata, ydata):
    '''Define the function to be minimized in the Nelder Mead algorithm
    '''
    length = len(xdata)
    fittedCurve = np.zeros(length, dtype=complex)
    for i in range(length):
        temp = v[0] * xdata[i] * np.exp(1j*v[1]*(i+1-(np.floor(length/2.0)+1)))
        fittedCurve[i] = temp
    rss = (abs(ydata-fittedCurve)**2).sum()
    return rss

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise 'You need to enter current node ID!'
        exit()

    #############################
    ## start the process
    #############################
    t0 = time()

    p = 55
    L = 1.46e6
    dx = 0.1
    dy = 0.1
    row = 121
    column = 121
    energy = 19.5
    referenceStart = 1  # be careful about the specific number
    lambda_ = (12.4/energy)*1e-4
    dataDir = '/kbase/home/wxu/data/SOFC/SOFC_'

    # read the reference image: only one reference image
    refNum = '%05d' % referenceStart
    fileName = dataDir + refNum + '.tif'
    reference = plt.imread(fileName)

    xline1 = [sum(x) for x in zip(*reference)]
    yline1 = [sum(x) for x in reference]
    yline1 = yline1[46 : 61]
    # the results of xline1 and yline1 are the same with MATLAB

    fx1 = np.fft.fftshift(np.fft.ifft(xline1))
    fy1 = np.fft.fftshift(np.fft.ifft(yline1))
    # fx1 and fy1 are the same as MATLAB

    start = 1 # it's 2 in Hanfei's code
                                                                            
    # set up environmental parameters
    frame_start = 0
    frame_end = 0
    nodeID = int(sys.argv[1])
    # environment related numbers
    nodes = 8
    ppn = 10
    ntotal = nodes * ppn
    label_x = column * row / ntotal #int type
    label_rest = column * row - label_x * ntotal

    if nodeID < label_rest:
        frame_start = nodeID*(label_x+1) + 1
        frame_end = (nodeID+1)*(label_x+1) + 1 #range doesn't count the last number
    else:
        frame_start = label_rest*(label_x+1) + (nodeID-label_rest)*label_x + 1
        frame_end = label_rest*(label_x+1) + (nodeID-label_rest+1)*label_x + 1 #range doesn't count the last number
    
    # create corresponding file to save a, gx and gy
    directory = 'experiment'
    if not os.path.exists(directory):
        os.mkdir(directory)
    out_file_name = directory + '/' + str(nodeID) + '.txt'
    out_file = open(out_file_name, 'wb')
    
    for frameNum in range(frame_start, frame_end):                                     
        fraNum = '%05d' % frameNum                                          
        fileName = dataDir + fraNum + '.tif'                                
        img = plt.imread(fileName)                                          
                                                                            
        xline2 = [sum(x) for x in zip(*img)]                                
        yline2 = [sum(x) for x in img]                                      
        yline2 = yline2[46 : 61]                                            
                                                                            
        fx2 = np.fft.fftshift(np.fft.ifft(xline2))                          
        fy2 = np.fft.fftshift(np.fft.ifft(yline2))                          
                                                                            
        startPoint = [1, 0]                                                 
        vx = fmin(rss, startPoint, args=(fx1, fx2), maxiter=1000, maxfun=1000, disp=0)    
        vy = fmin(rss, startPoint, args=(fy1, fy2), maxiter=1000, maxfun=1000, disp=0)    
                                                                            
        vx[1] = -vx[1] * len(fx1) * p / (lambda_*L)                         
        vy[1] = vy[1] * len(fy1) * p / (lambda_*L)                          
                                                                            
        out_file.write(str(vx[0]))
        out_file.write(' ')                                                     
        out_file.write(str(vx[1]))
        out_file.write(' ')                                                    
        out_file.write(str(vy[1])) 
        out_file.write(' ')           

    out_file.close()

    t1 = time()
    print nodeID, ' spent ', t1-t0 
