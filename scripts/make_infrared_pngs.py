import os
import sys
import glob

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import Image

IMAGE_DIM = 424

def make_png(f, vmin, vmax):
  name = os.path.splitext(f)[0]
  
  # Get flux
  data = fits.getdata(f)
  data = np.flipud(data)
  
  data = np.log10(data)
  data = np.clip(data, vmin, vmax)
  data = (255 * (data - vmin) / (vmax - vmin)).astype('uint8')
  
  cmap = plt.get_cmap('gist_heat')
  data = (255 * cmap(data)).astype('uint8')
  im = Image.fromarray(data)
  im = im.resize( (IMAGE_DIM, IMAGE_DIM), Image.ANTIALIAS)
  im.save("%s.png" % (name.replace("_ir", "")))


if __name__ == '__main__':
  
  if len(sys.argv) < 2:
    print "Usage: python make_png.py [directory] [vmin] [vmax]"
    sys.exit()
  
  directory = sys.argv[1]
  if len(sys.argv) == 4:
    vmin = float(sys.argv[2])
    vmax = float(sys.argv[3])
  else:
    vmin = -1.3
    vmax = -0.5
  
  os.chdir(directory)
  for f in glob.glob("*ir.fits"):
    make_png(f, vmin, vmax)