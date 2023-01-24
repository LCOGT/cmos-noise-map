#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 13:42:45 2023

@author: pkottapalli
"""
from astropy.io import fits
from glob import glob
import numpy as np


def read_bias_frames(path: str, data_ext=0):
    """
    A function to open up fits files with memory mapping.

    Parameters
    ----------
    path : str
        DESCRIPTION. The path to your fits files with the *.fits at the end to indicate which files you want to be read.
    data_ext : integer or string, optional
        DESCRIPTION. The default is 0. This is the extension to the data header data unit (hdu) that is to be processed.

    Returns
    -------
    ims : array
        DESCRIPTION. And array of opened, memory mapped, fits hdus. Not the data itself.

    """
    # Assumes trimmed and processed bias frames
    files = glob(path, recursive=True)  # Need at least 50
    ims = [
        fits.open(f, memmap=True, do_not_scale_image_data=True) for f in files
    ]  # Doesn't work unless not scaled
    # Manually scale data?
    ims = np.array(ims)[:, 0]
    return ims


def write_hdu(data):
    """
    A function to write the data out to a fits file named ____

    Parameters
    ----------
    data : NxN array of floats
        DESCRIPTION. The data to be written out into the fits file. This is where the readnoise map goes.

    Returns
    -------
    None.

    """
    hdu = fits.PrimaryHDU(data)
    hdu.writeto("test.fits")
