
import sys
import os
import numpy as np

import matplotlib as mpl
mpl.use('Agg')
import pylab as pl

tv_array = np.loadtxt(sys.argv[1], skiprows=1)

pl.plot(tv_array.T[0], tv_array.T[1])

label = os.path.splitext(os.path.basename(sys.argv[1]))[0]

pl.savefig('data/img/%s.png' % label)
