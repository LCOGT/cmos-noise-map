#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 16:06:54 2023

@author: pkottapalli
"""
from astropy.io import fits
from glob import glob
import numpy as np


# Assumes that the data is being read into the system in order.
def data_to_pixel(data):
    """
    Takes data in the form of a series of opened images (of whatever shape) and
    returns the data as a list of pixel values across images, along with data.

    Parameters
    ----------
    data : list, shape(N images, rows, columns) #Is this true?
        DESCRIPTION. A list of images or cutout of images

    Returns
    -------
    pixels : list of shape(1, N images)
        DESCRIPTION. The list of pixel values across images, for all pixels given.

    """
    dshape = np.shape(data)
    x, y = np.meshgrid(range(dshape[1]), range(1), indexing="ij")
    pixels = np.reshape(np.transpose(data), (1 * dshape[1], dshape[0]))
    return pixels

def qc_input(path, data_ext=0):
    files = glob(path, recursive=True)
    num_files = len(files)
    assert num_files>=50
    dshape = np.shape(fits.open(files[0])[data_ext].data)
    for f in files[1:]:
        shape = np.shape(fits.open(f)[data_ext].data)
        assert shape==dshape
    