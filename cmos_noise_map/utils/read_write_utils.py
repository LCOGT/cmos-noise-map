#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 13:42:45 2023

@author: pkottapalli
"""
from cmos_noise_map.utils.data_utils import qc_input
from astropy.io import fits
from glob import glob
import numpy as np


def read_bias_frames(path: str, data_ext=0):
    """
    A function to open up fits files with memory mapping.

    Parameters
    ----------
    path : str
        DESCRIPTION. The path to your fits files without the .fits at the end
    data_ext : integer or string, optional
        DESCRIPTION. The default is 0. This is the extension to the data header data unit (hdu) that is to be processed.

    Returns
    -------
    ims : array
        DESCRIPTION. And array of opened, memory mapped, fits hdus. Not the data itself.

    """
    # Assumes trimmed and processed bias frames
    files = glob(path + str("*.fits"), recursive=True)
    images = [
        fits.open(f, memmap=True, do_not_scale_image_data=True) for f in files
    ]  # Doesn't work unless not scaled
    qc_input(images)
    images = np.array(images)[:, 0]
    return images


def write_hdu(data, filename: str, hduname: str = None):
    """
    A function to write the data out to a fits file containing a read nosie map

    Parameters
    ----------
    data : NxN array of floats
        DESCRIPTION. The data to be written out into the fits file. This is where the readnoise map goes.

    Returns
    -------
    None.

    """
    hdu = fits.PrimaryHDU(data)
    hdu.writeto(filename, overwrite=True)
