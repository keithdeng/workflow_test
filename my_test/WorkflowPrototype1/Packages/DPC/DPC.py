#!/usr/bin/env python

"""
    Routine for Differential Phase Constrast 
    Results:
        save four txt files: gx_test.txt, gy_test.txt, a_test.txt, phi_test.txt
        save one tif file for reconstructed phase image with user defined name
    Example:
    $> python DPC.py 'output.tif'
"""

from numpy import *
from scipy.optimize import fmin
import time
import scipy
import matplotlib.pyplot as plt
import Image
import sys

def sse(v, xdata, ydata):
    FittedCurve = []
    length = len(xdata)
    for i in range(length):
        temp = v[0]*xdata[i]*exp(1j*v[1]*(i+1-(floor(length/2.0)+1)))
        FittedCurve.append(temp)
    sse = ((abs(ydata - FittedCurve))**2).sum()
    return sse

def DPC(filename):
    reference_start = 1 # be careful about the specific number!!!
    energy = 19.5
    data_dir = 'SOFC/SOFC_'
    #data_dir = 'C:\Install applications\SOFC\SOFC_'
    row = 121
    column = 121
    p = 55
    lambda_m = (12.4/energy)*1e-4
    L = 1.46e6
    dx = 0.1
    dy = 0.1

    # read the reference image: only one reference image
    ref_num = '%05d' % reference_start
    file_name = data_dir + ref_num + '.tif'
    reference = plt.imread(file_name)

    xline1 = [sum(x) for x in zip(*reference)]
    yline1 = [sum(x) for x in reference]
    yline1 = yline1[46:61]
    # the results of xline1 and yline1 are the same with MATLAB

    fx1 = fft.fftshift(fft.ifft(xline1))
    fy1 = fft.fftshift(fft.ifft(yline1))
    # fy1 is the same as MATLAB, fx1 is not the same

    start = 1 # it's 2 in Hanfei's code
    #data_dir = 'C:\Install applications\SOFC\SOFC_'

    aa  = loadtxt('a copy.txt')
    gxx = loadtxt('gx copy.txt')
    gyy = loadtxt('gy copy.txt')
    
    a = aa.tolist()
    gx = gxx.tolist()
    gy = gyy.tolist()
    
    print "Routine starts now"
    for i in range(119, 121):
        a.append([])
        gx.append([])
        gy.append([])
        for j in range(column):
            a[i].append(0)
            gx[i].append(0)
            gy[i].append(0)
    
    for i in range(119, 121):
        for j in range(column):
            frame_num = start + i*column + j
            fra_num = '%05d' % frame_num
            file_name = data_dir + fra_num + '.tif'
            img = plt.imread(file_name)
        
            xline2 = [sum(x) for x in zip(*img)]
            yline2 = [sum(x) for x in img]
            yline2 = yline2[46:61]
        
            fx2 = fft.fftshift(fft.ifft(xline2))
            fy2 = fft.fftshift(fft.ifft(yline2))
            start_point = [1, 0]
            vx = fmin(sse, start_point, args=(fx1, fx2), maxiter=1000, maxfun=1000, disp=0)
            vy = fmin(sse, start_point, args=(fy1, fy2), maxiter=1000, maxfun=1000, disp=0)
            vx[1] = -vx[1]*len(fx1)*p/(lambda_m*L)
            vy[1] = vy[1]*len(fy1)*p/(lambda_m*L)
            a[i][j] = vx[0]
            gx[i][j] = vx[1]
            gy[i][j] = vy[1]
            
            if j % 10 == 0:
                #plot result
                plt.ion()
                plt.figure(2)
                plt.subplot(131)
                plt.xlabel('Gx')
                plt.imshow(gx, cmap = plt.cm.gray)
                plt.draw()
                plt.subplot(132)
                plt.xlabel('Gy')
                plt.imshow(gy, cmap = plt.cm.gray)
                plt.draw()
                plt.subplot(133)
                plt.xlabel('Amplitude')
                plt.imshow(a, cmap = plt.cm.gray)
                plt.draw()
                plt.ioff()
                #plot scan images
                plt.ion()
                plt.figure(3)
                plt.subplot(121)
                plt.xlabel('Reference Image')
                plt.imshow(reference)
                plt.draw()
                plt.subplot(122)
                plt.xlabel('Scan Image')
                plt.imshow(img)
                plt.draw()
                plt.ioff()
        
        print i
   
#scipy.misc.imsave('a.jpg', a)
    savetxt('a_test.txt', a)
#    scipy.misc.imsave('gx.jpg', gx)
    savetxt('gx_test.txt', gx)
#scipy.misc.imsave('gy.jpg', gy)
    savetxt('gy_test.txt', gy)

    w = 1 # weighting parameter
    tx = fft.fftshift(fft.fft2(gx))
    ty = fft.fftshift(fft.fft2(gy))
    c = []
    for i in range(row):
        c.append([])
        for j in range(column):
            kappax = 2*pi*(j+1-(floor(column/2.0)+1))/(column*dx)
            kappay = 2*pi*(i+1-(floor(row/2.0)+1))/(row*dy)
            if kappax == 0 and kappay == 0:
                c[i].append(0)
            else:
                c_temp = -1j*(kappax*tx[i][j]+w*kappay*ty[i][j])/(kappax**2 + w*kappay**2)
                c[i].append(c_temp)
    c = fft.ifftshift(c)
    phi = fft.ifft2(c)
    phi = phi.real
#    scipy.misc.imsave('phi_test.jpg', phi)
    savetxt('phi_test.txt', phi)
    aphi = array(phi)
    aphi = 255*(aphi - amin(aphi))/(amax(aphi) - amin(aphi))
    im = Image.fromarray(uint8(aphi))
    im.save(filename)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "please enter the filename of the phi image"
        exit()
    
    DPC(sys.argv[1])
    