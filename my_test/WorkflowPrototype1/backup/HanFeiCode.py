#!/usr/bin/env python
## Brookhaven National Lab

from numpy import *
from scipy.optimize import fmin
import time
import scipy
import matplotlib.pyplot as plt

def sse(v, xdata, ydata):
    FittedCurve = []
    length = len(xdata)
    for i in range(length):
        temp = v[0]*xdata[i]*exp(1j*v[1]*(i+1-(floor(length/2.0)+1)))
        FittedCurve.append(temp)
    sse = ((abs(ydata - FittedCurve))**2).sum()
    return sse

reference_start = 1 # be careful about the specific number!!!
energy = 19.5
#data_dir = '/Users/admin/Documents/SOFC/SOFC_'
data_dir = 'C:\Install applications\SOFC\SOFC_'
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
data_dir = 'C:\Install applications\SOFC\SOFC_'

a  = []
gx = []
gy = []

for i in range(row):
    a.append([])
    gx.append([])
    gy.append([])
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
        a[i].append(vx[0])
        gx[i].append(vx[1])
        gy[i].append(vy[1])
    print i
    
scipy.misc.imsave('a.jpg', a)
savetxt('a.txt', a)
scipy.misc.imsave('gx.jpg', gx)
savetxt('gx.txt', gx)
scipy.misc.imsave('gy.jpg', gy)
savetxt('gy.txt', gy)

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
scipy.misc.imsave('phi.jpg', phi)
savetxt('phi.txt', phi)
