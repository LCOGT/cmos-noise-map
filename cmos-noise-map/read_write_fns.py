#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 13:42:45 2023

@author: pkottapalli
"""
from astropy.io import fits
from glob import glob
import numpy as np

def read_bias_frames(path:str, data_ext=0):
    #Assumes trimmed and processed bias frames
    files = glob(path, recursive = True) #Need at least 50
    ims = [fits.open(f, memmap=True, do_not_scale_image_data=True) for f in files] #Doesn't work unless not scaled
    #Manually scale data?
    ims = np.array(ims)[:,0]
    return ims

def write_hdu(data):
    hdu = fits.PrimaryHDU(data)
    hdu.writeto('test.fits')
