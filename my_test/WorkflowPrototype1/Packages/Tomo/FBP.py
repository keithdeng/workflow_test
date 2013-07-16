#! usr/bin/env python
"""
    Filtered backprojection from phantom image
"""
import sys
import numpy as np
import matplotlib.pyplot as pl
import Image
import phantom
import parallel_beam as pb

def recon(projections, a_min = 0, a_max = 180, a_inc = 1):
    angle = np.arange (a_min, a_max, a_inc)
    reconstruction = pb.iradon (projections, angle)
    reconstruction = 255*(reconstruction-reconstruction.min())/(reconstruction.max()-reconstruction.min())
    #pl.figure()
    #pl.imshow (projections, cmap = pl.cm.gray)
    #pl.show ()
    #print "save file"
    return reconstruction

if __name__ == '__main__':
    filename = ''
    a_min = 0
    a_max = 180
    a_inc = 1

    if len(sys.argv) < 5:
        print len(sys.argv)
        print 'use default settings'
    else:
        filename = str(sys.argv[1])
        a_min = float(sys.argv[2])
        a_max = float(sys.argv[3])
        a_inc = float(sys.argv[4])
    oname = 'Data/Tomo/projs/projections_'+str(sys.argv[2])+'_'+str(sys.argv[3])+'_'+str(sys.argv[4])+'.npy'
    projs = np.load(oname)

    ###edited by Li
    """
    pl.ion()
    pl.figure(1)
    pl.subplot(121)
    pl.xlabel('Sinogram')
    pl.imshow(projs, cmap = pl.cm.gray)
    pl.draw()
    pl.ioff()
    """

    reconstruction = recon(projs, a_min, a_max, a_inc)
    im = Image.fromarray(np.uint8(reconstruction))

    #filename = "../static/"+filename
    im.save(filename)

    print "hi"
    #edited by Li
    """
    pl.ion()
    pl.figure(1)
    pl.subplot(122)
    pl.xlabel('Reconstructed Result')
    pl.imshow(im, cmap = pl.cm.gray)
    pl.draw()
    pl.ioff()
    pl.show()
    """
