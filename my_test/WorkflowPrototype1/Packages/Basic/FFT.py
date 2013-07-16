#! usr/bin python

import sys
import time
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
import Image

def fourier(filename):
#plt.ion()
#im = mpimg.imread('/Users/weixu/Desktop/lena.png')
#plt.subplot(211)
#plt.imshow(im)
#plt.draw()
#start = time.time()
    im = Image.open('test.png')
    fim = np.fft.fft2(im)
    fim = np.log(fim)
    fim = np.fft.fftshift(fim)
    fim = np.abs(fim)
#print "It took", time.time() - start, "seconds."
#plt.subplot(212)
#plt.imshow(fim)
#plt.draw()
#plt.ioff()
    fim = 255*(fim-fim.min())/(fim.max()-fim.min())
    Image.fromarray(np.uint8(fim)).save(filename)

if __name__ == '__main__':
    filename = ''
    if len(sys.argv) < 2:
        print 'Use default filename: ofile.png'
        filename = 'ofilefft.png'
    else:
        filename = str(sys.argv[1])
    fourier(filename)
