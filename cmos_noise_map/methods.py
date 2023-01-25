#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 16:02:56 2023

@author: pkottapalli
"""
from cmos_noise_map.get_rts import per_pixel_readnoise, get_rts
from cmos_noise_map.utils.misc_fns import data_to_pixel
from cmos_noise_map.read_write_fns import read_bias_frames
import numpy as np

# read in one row at a time, iterate over it pixel by pixel
def do_rts(path, upper_q, data_ext=0, *args):
    """
    A function wrapping all the methods to produce a full readnoise map

    Parameters
    ----------
    path : str
        DESCRIPTION. The path to the files to be read in
    upper_q : float
        DESCRIPTION. Upper standard deviation cutoff for noisy pixels for evaluation
    *args : 
        DESCRIPTION. The arguments to be passed to get_rts

    Returns
    -------
    readnoise_map : array of the same shape as the input data
        array where each element is the readnoise associated with that pixel.

    """
    ims = read_bias_frames(path, data_ext)
    im_test = ims[0].data
    dshape = np.shape(im_test)
    readnoise_map = np.zeros((dshape[0], dshape[1]))

    for row_no in range(0, dshape[0]):
        data = []
        for im in ims:
            data.append(im.data[row_no, :] + 32768)

        # convert data to stacked pixels
        pixels = data_to_pixel(data)

        if not upper_q:
            stdimage = np.std(data, axis=0)
            upper_q = np.quantile(stdimage, 0.8)

        # Append it all to a pixel map
        for i, p in enumerate(pixels):
            noise = per_pixel_readnoise(p, upper_q, *args)
            if not np.isnan(noise):
                readnoise_map[row_no, i] = noise
            else:
                readnoise_map[row_no, i] = np.std(p)
    return readnoise_map


def do_std(path, data_ext=0):
    """
    A function to take the standard deviation of each pixel to use as a readnoise map.
    This is a faster method than do_rts, less rigorous statistically but achieves similar answers.

    Parameters
    ----------
    path : str
        DESCRIPTION. The path to the files to be read in

    Returns
    -------
    readnoise_map : array of the same shape as the input data
        array where each element is the readnoise associated with that pixel.

    """
    ims = read_bias_frames(path, data_ext)
    im_test = ims[0].data
    dshape = np.shape(im_test)
    readnoise_map = np.zeros((dshape[0], dshape[1]))
    for row_no in range(0, dshape[0]):
        data = []
        for im in ims:
            data.append(im.data[row_no, :] + 32768)

        # convert data to stacked pixels
        stdimage = np.std(data, axis=0)
        readnoise_map[row_no, :] = stdimage
        print("row done")
    return readnoise_map


def do_rts_params(path, upper_q, data_ext=0, *args):
    """
        

    Parameters
    ----------
    path : str
        DESCRIPTION. The path to the files to be read in
    upper_q : float
        DESCRIPTION. Upper standard deviation cutoff for noisy pixels for evaluation
    *args : 
        DESCRIPTION. The arguments to be passed to get_rts

    Returns
    -------
    readnoise_map : array of the same shape as the input data
        array where each element is a list of associated parameters from modelling the pixel.
        It returns a nan for each parameter if a pixel does not exhibit RTS or is not noisy.
    
    """
    ims = read_bias_frames(path, data_ext)
    im_test = ims[0].data
    dshape = np.shape(im_test)
    param_map = []

    for row_no in range(0, dshape[0]):
        data = []
        for im in ims:
            data.append(im.data[row_no, :] + 32768)

        # convert data to stacked pixels
        pixels = data_to_pixel(data)
        if not upper_q:
            stdimage = np.std(data, axis=0)
            upper_q = np.quantile(stdimage, 0.8)

        # Append it all to a pixel map
        for i, p in enumerate(pixels):
            params = get_rts(p, upper_q, *args)
            param_map.append(params)
    return param_map
