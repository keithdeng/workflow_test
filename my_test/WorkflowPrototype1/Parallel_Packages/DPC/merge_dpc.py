#! /local/bin/env python

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imsave
from scipy.optimize import fmin
from time import time

if __name__ == '__main__':

    if len(sys.argv) < 3:
        raise 'Please enter both node number and processor number'
        exit()

    t0 = time()

    node_num = sys.argv[1]*sys.argv[2]

    row = 121
    column = 121
    dx = 0.1
    dy = 0.1

    a = np.zeros(row*column, dtype='d')
    gx = np.zeros(row*column, dtype='d')
    gy = np.zeros(row*column, dtype='d')

    i = 0
    for n in range(node_num):
        filename = 'experiment/' + str(n) + '.txt'
        file = open(filename, 'rb')
        result = np.array(file.read().split(), dtype='d')
    
        for m in range(len(result)):
            if m % 3 == 0:
                a[i] = result[m]
            elif m % 3 == 1:
                gx[i] = result[m]
            elif m % 3 == 2:
                    gy[i] = result[m]
                    i += 1


    a = a.reshape(row, column)
    imsave('a.tif', a)
    gx = gx.reshape(row, column)
    imsave('gx.tif', gx)
    gy = gy.reshape(row, column)
    imsave('gy.tif', gy)

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
    imsave('phi.tif', phi)
    #np.savetxt('phi.txt', phi)

    t1 = time()
    print t1-t0


