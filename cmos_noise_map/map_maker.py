#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 16:02:56 2023

@author: Prerana Kottapalli
"""
import numpy as np
import click

from cmos_noise_map.get_rts import per_pixel_readnoise, get_rts
from cmos_noise_map.utils.data_utils import data_to_pixel


class MapMaker:
    def __init__(
        self,
        images: list,
        tolerance: float = 0.05,
        upper_quantile: float = None,
        min_peak_seperation: float = 10,
    ):
        """
        A class initializing the data to be passed through each map making algorithm.

        Parameters
        ----------
        images : list
            DESCRIPTION. The fits opened input images to be processed
        tolerance : float, optional
            DESCRIPTION. The minimum difference between silhouette scores (likelihood of the model being correct)
                         between n_components=2 and 3. If there is a plateau (i.e. not much improvement between n=2 and n=3)
                         then the number of components chosen for the fit is 2. Not recommended to change unless you have
                         looked at the scores yourself. The default is 0.05.
        upper_quantile : float, optional
            DESCRIPTION. The upper standard deviation cutoff of pixels to be evaluated for telegraph noise.
        min_peak_seperation : float, optional
            DESCRIPTION. The minimum separation of peaks for them to be considered separate peaks. If they are too close,
            the next lowest component is taken to be the model. The default is 10.

        Returns
        -------
        None.

        """
        self.images = images
        self.data_shape = np.shape(images[0].data)
        self.map = np.zeros(self.data_shape)
        self.tolerance = tolerance
        self.upper_quantile = upper_quantile
        self.min_peak_separation = min_peak_seperation
        self.bzero = self.images[0].header['BZERO']
        self.bscale = self.images[0].header['BSCALE']


class STDMapMaker(MapMaker):
    def create_map(self):
        """
        A function to take the standard deviation of each pixel to use as a readnoise map.
        This is a faster method than RTSMapMaker, less rigorous statistically but achieves similar answers.

        Returns
        -------
        readnoise_map : array of the same shape as the input data
            array where each element is the readnoise associated with that pixel.

        """
        with click.progressbar(range(0, self.data_shape[0])) as bar:
            for row_no in bar:
                data = []
                for im in self.images:
                    data.append((im.data[row_no, :] + self.bzero)*self.bscale)

                # convert data to stacked pixels
                stdimage = np.std(data, axis=0)
                self.map[row_no, :] = stdimage
        return self.map


class RTSMapMaker(MapMaker):
    def create_map(self):
        """
        A function wrapping all the methods to produce a full readnoise map

        Parameters
        ----------
        inherited from MapMaker class

        Returns
        -------
        readnoise_map : array of the same shape as the input data
            array where each element is the readnoise associated with that pixel.

        """
        with click.progressbar(range(0, self.data_shape[0])) as bar:
            for row_no in bar:
                data = []
                for im in self.images:
                    data.append((im.data[row_no, :] + self.bzero)*self.bscale)

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
        inherited from MapMaker class

        Returns
        -------
        param_map : array of the same shape as the input data
            array where each element is a list of associated parameters from modelling the pixel.
            It returns a nan for each parameter if a pixel does not exhibit RTS or is not noisy.

        """
        param_map = []
        with click.progressbar(range(0, self.data_shape[0])) as bar:
            for row_no in bar:
                data = []
                for im in self.images:
                    data.append((im.data[row_no, :] + self.bzero)*self.bscale)

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
