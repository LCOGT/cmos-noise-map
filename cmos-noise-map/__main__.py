# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 11:07:17 2023

@author: prera
"""
from get_rts import readnoise, get_rts

#Collect images to open
data_shape = np.shape(images[0])
#memory map the bias images in

#read in one row at a time, iterate over it pixel by pixel

def per_pixel_readnoise(p, tol = 0.05, upper_q = 3, min_peak_sep = 10):
    means, variances, _, amplitudes = get_rts(p, tol = 0.05, upper_q = 3, min_peak_sep = 10)
    pixel_readnoise = readnoise(means, variances, amplitudes)
    return pixel_readnoise

#Append it all to a pixel map
readnoise_map = np.zeros(data_shape)