#!/usr/bin/env python
''' 
Created on May 23, 2013, last modified on June 19, 2013
@author: Cheng Chang (cheng.chang.ece@gmail.com)
         Computer Science Group, Computational Science Center
         Brookhaven National Laboratory
        
This code is for Differential Phase Contrast (DPC) imaging based on Fourier-shift fitting
implementation. 

Reference: Yan, H. et al. Quantitative x-ray phase imaging at the nanoscale by multilayer 
           Laue lenses. Sci. Rep. 3, 1307; DOI:10.1038/srep01307 (2013).

Test data is available at:
https://docs.google.com/file/d/0B3v6W1bQwN_AdjZwWmE3WTNqVnc/edit?usp=sharing
'''

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
dataDir = '../Data/DPC/SOFC/SOFC_'
# dataDir = 'C:\Install applications\SOFC\SOFC_'

# read the reference image: only one reference image
refNum = '%05d' % referenceStart
fileName = dataDir + refNum + '.tif'
#reference = plt.imread(fileName)
reference = np.array(Image.open(fileName))

xline1 = [sum(x) for x in zip(*reference)]
yline1 = [sum(x) for x in reference]
yline1 = yline1[46 : 61]
# the results of xline1 and yline1 are the same with MATLAB

fx1 = np.fft.fftshift(np.fft.ifft(xline1))
fy1 = np.fft.fftshift(np.fft.ifft(yline1))
# fx1 and fy1 are the same as MATLAB

start = 1 # it's 2 in Hanfei's code
# dataDir = 'C:\Install applications\SOFC\SOFC_'
# dataDir = '/Users/admin/Documents/SOFC/SOFC_'

a = np.arange(row*column, dtype='d').reshape(row, column)
gx = np.arange(row*column, dtype='d').reshape(row, column)
gy = np.arange(row*column, dtype='d').reshape(row, column)

for i in range(row):
    for j in range(column):
        frameNum = start + i*column + j
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
        
        a[i, j] = vx[0]
        gx[i, j] = vx[1]
        gy[i, j] = vy[1]
    print i
    
imsave('a.jpg', a)
np.savetxt('a.txt', a)
imsave('gx.jpg', gx)
np.savetxt('gx.txt', gx)
imsave('gy.jpg', gy)
np.savetxt('gy.txt', gy)

#-------------reconstruct the final phase image using gx and gy--------------------#
w = 1 # Weighting parameter
tx = np.fft.fftshift(np.fft.fft2(gx))
ty = np.fft.fftshift(np.fft.fft2(gy))
c = np.arange(row*column, dtype=complex).reshape(row, column)
for i in range(row):
    for j in range(column):
        kappax = 2 * np.pi * (j+1-(np.floor(column/2.0)+1)) / (column*dx)
        kappay = 2 * np.pi * (i+1-(np.floor(row/2.0)+1)) / (row*dy)
        if kappax==0 and kappay==0:
            c[i, j] = 0
        else:
            cTemp = -1j * (kappax*tx[i][j]+w*kappay*ty[i][j]) / (kappax**2 + w*kappay**2)
            c[i, j] = cTemp
c = np.fft.ifftshift(c)
phi = np.fft.ifft2(c)
phi = phi.real
imsave('phi.jpg', phi)
np.savetxt('phi.txt', phi)

t1 = time()
print t1-t0
