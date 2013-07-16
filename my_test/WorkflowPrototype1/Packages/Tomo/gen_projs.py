#! usr/bin/env python
"""
    Generate projections
    Example for random object:
    $> python gen_projs.py 'object.png' 0 180 1
    Example for Shepp-Logan Phantom:
    $> python gen_projs.py 'phantom' 0 90 2 512
"""

import sys
import numpy as np
import matplotlib.pyplot as pl
import matplotlib.image as pim
import Image
import phantom
import parallel_beam as pb

def gen_projs(image, a_min = 0, a_max = 180, a_inc = 1, size = 512):
    if image == 'phantom':
        image = phantom.phantom (size)
    else:
        image = pim.imread(image)

    angle = np.arange (a_min, a_max, a_inc)
    projections = pb.radon (image, angle)

    return projections


if __name__ == '__main__':
    projs = None
    
    if str(sys.argv[1]).lower() == 'phantom' and len(sys.argv) == 6:
        projs = gen_projs('phantom', float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]))
    elif len(sys.argv) == 5:
        projs = gen_projs(str(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))
    else:
        print "Please enter enough parameters!"
        exit()

    print "save file"
    oname = 'Data/Tomo/projs/projections_'+str(sys.argv[2])+'_'+str(sys.argv[3])+'_'+str(sys.argv[4])
    np.save(oname, projs)

    pl.figure()
    pl.imshow (projs, cmap = pl.cm.gray)
    pl.show ()
