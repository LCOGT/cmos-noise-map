# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 11:07:17 2023

@author: prera
"""
from get_rts import readnoise, get_rts
from astropy.io import fits
from glob import glob
import numpy as np

files = glob('/run/media/pkottapalli/Untitled/411_mod3_gain30_bin1_telegraph/*.fits', recursive = True) #Need at least 50

def per_pixel_readnoise(p, tol = 0.05, upper_q = 3, min_peak_sep = 10):
    means, variances, num_peaks, amplitudes = get_rts(p, tol = 0.05, upper_q = 3, min_peak_sep = 10)
    pixel_readnoise = readnoise(means, variances, num_peaks, amplitudes)
    return pixel_readnoise

#Collect images to open
im_test = fits.open(files[0])[0].data
data = []
shape = np.shape(im_test)
for t in glob('/run/media/pkottapalli/Untitled/bias_temp/*', recursive = True):
    temp = np.memmap(t, dtype = im_test.dtype , mode = 'r', shape = (1,shape[1]))
    data.append(temp)
    del temp

#memory map the bias images in

#read in one row at a time, iterate over it pixel by pixel

dshape = np.shape(data)
x, y = np.meshgrid(range(dshape[1]),range(dshape[2]), indexing = 'ij')
indices = np.column_stack((x[-1].ravel(),y[-1].ravel())).tolist()
pixels = np.reshape(np.transpose(data), (dshape[2]*dshape[1], dshape[0])).tolist()

stdimage = np.std(data, axis=0)
upper_q = np.quantile(stdimage, 0.8)


#Append it all to a pixel map
readnoise_map = np.zeros((dshape[1], dshape[2]))
row_no = 0
for i, p in enumerate(pixels):
    noise = per_pixel_readnoise(p, upper_q)
    if not np.isnan(noise):
        readnoise_map[row_no,i] = noise
    else:
        readnoise_map[row_no, i] = np.std(p)