#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 16:02:56 2023

@author: pkottapalli
"""
from cmos_noise_map.get_rts import per_pixel_readnoise, get_rts
from cmos_noise_map.utils.data_utils import data_to_pixel
import numpy as np


class MapMaker:
    def __init__(
        self,
        images: list,
        tolerance: float = 0.05,
        upper_quantile: float = None,
        min_peak_seperation: float = 10,
    ):
        self.images = images
        self.data_shape = np.shape(images[0].data)
        self.map = np.zeros(self.data_shape)
        self.tolerance = tolerance
        self.upper_quantile = upper_quantile
        self.min_peak_separation = min_peak_seperation


class STDMapMaker(MapMaker):
    def create_map(self):
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
        for row_no in range(0, self.data_shape[0]):
            data = []
            for im in self.images:
                data.append(im.data[row_no, :] + 32768)

            # convert data to stacked pixels
            stdimage = np.std(data, axis=0)
            self.map[row_no, :] = stdimage
        return self.map


class RTSMapMaker(MapMaker):
    def create_map(self):
        """
        A function wrapping all the methods to produce a full readnoise map

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        for row_no in range(0, self.data_shape[0]):
            data = []
            for im in self.images:
                data.append(im.data[row_no, :] + 32768)

            # convert data to stacked pixels
            pixels = data_to_pixel(data)

            if not self.upper_quantile:
                stdimage = np.std(data, axis=0)
                self.upper_quantile = np.quantile(stdimage, 0.8)

            # Append it all to a pixel map
            for i, p in enumerate(pixels):
                noise = per_pixel_readnoise(
                    p,
                    tolerance=self.tolerance,
                    upper_quantile=self.upper_quantile,
                    min_peak_separation=self.min_peak_separation,
                )
                if not np.isnan(noise):
                    self.map[row_no, i] = noise
                else:
                    self.map[row_no, i] = np.std(p)
        return self.map


class RTSParameterMapMaker(MapMaker):
    def create_map(self):
        """
        Returns the parameters calculated by get_rts, not the readnoise

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
        param_map = []
        for row_no in range(0, self.data_shape[0]):
            data = []
            for im in self.images:
                data.append(im.data[row_no, :] + 32768)

            # convert data to stacked pixels
            pixels = data_to_pixel(data)

            if not self.upper_quantile:
                stdimage = np.std(data, axis=0)
                self.upper_quantile = np.quantile(stdimage, 0.8)

            # Append it all to a pixel map
            for i, p in enumerate(pixels):
                params = get_rts(
                    p,
                    tolerance=self.tolerance,
                    upper_quantile=self.upper_quantile,
                    min_peak_separation=self.min_peak_separation,
                )
                param_map.append(params)
        return param_map


def do_rts(ims, upper_q, *args):
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


def do_std(ims, data_ext=0):
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
    return readnoise_map


def do_rts_params(ims, upper_q, *args):
    """
    Returns the parameters calculated by get_rts, not the readnoise

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
