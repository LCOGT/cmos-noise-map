#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 13:42:45 2023

@author: Prerana Kottapalli
"""
from astropy.io import fits
from collections.abc import Iterable
from glob import glob
import numpy as np
import pandas as pd
import os
import tempfile

from cmos_noise_map.utils.data_utils import check_input_data

class read_write_utils():
    def __init__(self, path: str, filename: str, data_ext=0, hduname: str = 'PRIMARY', fpack=True):
        self.path = path
        self.data_ext = 0
        self.filename = filename
        self.hduname = hduname
        self.fpack = fpack
        
    def read_bias_frames(self):
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
        files = glob(os.path.join(self.path + "*.fits"), recursive=True)
        if len(files) == 0:
            self.images = []
            with tempfile.TemporaryDirectory() as tmpdirname:
                filenames = glob(os.path.join(self.path + "*.fz"), recursive=True)
                for filename in filenames:
                    base_filename, file_extension = os.path.splitext(
                        os.path.basename(filename)
                    )
                    output_filename = os.path.join(tmpdirname, base_filename)
                    os.system("funpack -O {0} {1}".format(output_filename, filename))
                    self.images.append(
                        fits.open(
                            output_filename, memmap=True, do_not_scale_image_data=True
                        )[self.data_ext]
                    )
        else:
            self.images = [
                fits.open(f, memmap=True, do_not_scale_image_data=True)[self.data_ext] for f in files
            ]  # Doesn't work unless not scaled
        check_input_data(self.images)
        self.images = np.array(self.images)
        return self.images


    def pack(self,
        uncompressed_hdulist: fits.HDUList, lossless_extensions: Iterable
    ) -> fits.HDUList:
        """
        See:
        https://github.com/LCOGT/banzai/blob/master/banzai/utils/fits_utils.py#L217
    
        """
        if uncompressed_hdulist.data is None:
            primary_hdu = fits.PrimaryHDU(header=uncompressed_hdulist[0].header)
            hdulist = [primary_hdu]
        else:
            primary_hdu = fits.PrimaryHDU()
            if uncompressed_hdulist.header["EXTNAME"] in lossless_extensions:
                quantize_level = 1e9
            else:
                quantize_level = 64
            compressed_hdu = fits.CompImageHDU(
                data=np.ascontiguousarray(uncompressed_hdulist.data),
                header=uncompressed_hdulist.header,
                quantize_level=quantize_level,
                quantize_method=1,
            )
            hdulist = [primary_hdu, compressed_hdu]
        return fits.HDUList(hdulist)


    def write_file(self, data, fpack=True, data_type='image'):
        """
        A function to write an output file depending on which method was used to
        generate it.
    
        Parameters
        ----------
        data : (NxN array of floats)
            DESCRIPTION. he data to be written out into the fits file. This is
            where the readnoise map or the parameter map goes.
        filename : str
            DESCRIPTION. Name of the file to be written out. This is without the
            file ending.
        hduname : str, optional
            DESCRIPTION. The name of the hdu in case of writing out a fits file.
            The default is None.
        data_type : TYPE, optional
            DESCRIPTION. Type of data to be written out. This is determined by the
            program depending on what method was used. The default is "image". If
            the method used was "param" then the type is "table"
    
        Returns
        -------
        None.
    
        """
        if data_type == "image":
            hdr = self.images[0].header
            hdr["EXTNAME"] = self.hduname
            hdr['OBSTYPE'] = 'READNOISE'
            hdu = fits.PrimaryHDU(data, header=hdr)
            if fpack is True:
                filename = (
                    os.path.join(
                        os.path.dirname("~/test"),
                        os.path.splitext(os.path.basename(self.filename))[0],
                    )
                    + ".fits.fz"
                )
                hdu = self.pack(hdu, [f"{self.hduname}"])
            else:
                filename = (
                    os.path.join(
                        os.path.dirname("~/test"),
                        os.path.splitext(os.path.basename(filename))[0],
                    )
                    + ".fits"
                )
            hdu.writeto(filename, overwrite=True)
        elif data_type == "table":
            filename = os.path.join(filename, ".csv")
            means = []
            covariances = []
            num_peaks = []
            gmm_weights = []
            for i in data:
                means.append(i[0])
                covariances.append(i[1])
                num_peaks.append(i[2])
                gmm_weights.append(i[3])
    
            df = pd.DataFrame(
                {
                    "Means": means,
                    "Covariances": covariances,
                    "Number of Peaks": num_peaks,
                    "Mixture Weights": gmm_weights,
                }
            )
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
    df = pd.read_csv(csv_file, header=0)
    means = df["Means"]
    var = df["Covariances"]
    num_peaks = []
    for elem in df["Number of Peaks"]:
        if not np.isnan(elem):
            num_peaks.append(int(elem))
        else:
            num_peaks.append(np.nan)
    amps = df["Mixture Weights"]
    return means, var, num_peaks, amps
