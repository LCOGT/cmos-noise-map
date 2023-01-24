# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 11:07:17 2023

@author: prera
"""
from get_rts import readnoise, get_rts, data_to_pixel
from read_write_fns import read_bias_frames, write_hdu
import numpy as np
    
#Need at least 50 images

def per_pixel_readnoise(p, tol=0.05, upper_q = 3, min_peak_sep = 10):
    means, variances, num_peaks, amplitudes = get_rts(p, tol = 0.05, upper_q = 3, min_peak_sep = 10)
    pixel_readnoise = readnoise(means, variances, num_peaks, amplitudes)
    return pixel_readnoise

#read in one row at a time, iterate over it pixel by pixel
def do_rts(path, *args):
    ims = read_bias_frames(path)
    im_test = ims[0].data
    dshape = np.shape(im_test)
    readnoise_map = np.zeros((dshape[0], dshape[1]))
    
    for row_no in range(0,dshape[0]):
        data = []
        for im in ims:
            data.append(im.data[row_no,:]+32768)
            
        #convert data to stacked pixels
        pixels = data_to_pixel(data)
        stdimage = np.std(data, axis=0)
        upper_q = np.quantile(stdimage, 0.8)
        
        #Append it all to a pixel map
        for i, p in enumerate(pixels):
            noise = per_pixel_readnoise(p, upper_q)
            if not np.isnan(noise):
                readnoise_map[row_no,i] = noise
            else:
                readnoise_map[row_no, i] = np.std(p)
    return readnoise_map

def do_std(path, *args):
    ims = read_bias_frames(path)
    im_test = ims[0].data
    dshape = np.shape(im_test)
    readnoise_map = np.zeros((dshape[0], dshape[1]))
    for row_no in range(0, dshape[0]):
        data = []
        for im in ims:
            data.append(im.data[row_no,:]+32768)
            
        #convert data to stacked pixels
        stdimage = np.std(data, axis=0)
        readnoise_map[row_no, :] = stdimage
    return readnoise_map

def do_rts_params(path, *args):
    ims = read_bias_frames(path)
    im_test = ims[0].data
    dshape = np.shape(im_test)
    param_map = []
    
    for row_no in range(0,dshape[0]):
        data = []
        for im in ims:
            data.append(im.data[row_no,:]+32768)
            
        #convert data to stacked pixels
        pixels = data_to_pixel(data)
        stdimage = np.std(data, axis=0)
        upper_q = np.quantile(stdimage, 0.8)
        
        #Append it all to a pixel map
        for i, p in enumerate(pixels):
            params = get_rts(p, upper_q, *args)
            param_map.append(params)
    return param_map

path = '/run/media/pkottapalli/Untitled/411_mod3_gain30_bin1_telegraph/*.fits'
readnoise_map = do_std(path)
write_hdu(readnoise_map)