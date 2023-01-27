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

import pandas as pd

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


def write_hdu(data, filename: str, hduname: str = None, data_type='image'):
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
    if data_type=='image':
        hdr = fits.Header()
        hdr['NAME'] = hduname
        hdu = fits.PrimaryHDU(data, header=hdr)
        hdu.writeto(filename, overwrite=True)
    elif data_type=='table':       
        means = []
        covariances = []
        num_peaks = []
        gmm_weights = []
        for i in data:
            means.append(i[0])
            covariances.append(i[1])
            num_peaks.append(i[2])
            gmm_weights.append(i[3])

        df = pd.DataFrame({'Means': means, 'Covariances': covariances, 'Number of Peaks': num_peaks, 'Mixture Weights': gmm_weights})
        df.to_csv(filename, index=False)
    else:
        pass

def read_parameter_table(csv_file):
    """
    A utility function to read in a parameter map

    Parameters
    ----------
    csv_file : .csv file
        The csv file containing the parameter data output.

    Returns
    -------
    means : TYPE: list(float), length = num_peaks
        DESCRIPTION: The means of each of the Gaussian modes calculated by GMM
    var : TYPE: list(float), length = num_peaks
        DESCRIPTION: The covariance of each Gaussian mode calculated by GMM
    num_peaks : TYPE: int
        DESCRIPTION: The number of Gaussians used to model the distribution of values of the pixel
    amps : TYPE: list(float)
        DESCRIPTION: The weights of each gaussian in the mixture. All weights sum to 1.

    """
    gmm_df = pd.read_csv(csv_file, header = 0)
    means = gmm_df['Means']
    var = gmm_df['Covariances']
    num_peaks = gmm_df['Number of Peaks']
    amps = gmm_df['Mixture Weights']
    return means, var, num_peaks, amps