#!/usr/bin/env python
'''
Example of simple manipulation / image plotting from data
converted from LCLS XTC raw data files.
'''
from __future__ import print_function

import h5py

import matplotlib.pyplot as plt

ifile = h5py.File('/dev/shm/scratch/MC0017-T0000-e500-no-comp.h5','r')
#ifile = h5py.File('/dev/shm/scratch/MC0027-T0000-e500-c=64k-hw.h5','r')
data1 = ifile['/instrument/CspadElement/CxiDs1-0:Cspad-0/data']

img_idx = 300
img = data1[img_idx,:]
img.shape

# img2k = img.reshape(2048, 1121)
# 
# For CspadElement/CxiDs1
img2k = img[:2048*1121].reshape(1121, 2048)

plt.imshow(img2k)
plt.show()

data_frame = ifile['/instrument/Frame/CxiDg3-0:Opal1000-0/data']
frame = data_frame[200,:]
frame.shape
frame2k = frame[:2048*1024+1].reshape(1024, 2048)
plt.imshow(frame2k)
plt.show()
