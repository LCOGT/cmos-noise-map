#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 16:06:54 2023

@author: Prerana Kottapalli
"""
import numpy as np
import sys


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
    data_shape = np.shape(data)
    x, y = np.meshgrid(range(data_shape[1]), range(1), indexing="ij")
    pixels = np.reshape(np.transpose(data), (1 * data_shape[1], data_shape[0]))
    return pixels


class UnequalDataShapeException(Exception):
    "Raised when the input shapes are not the same"
    pass


class NotEnoughDataException(Exception):
    "Raised when there are not enough input images"
    pass


def check_input_data(images):
    """
    Ensure that data is all the same shape, and that there are at least 50 files.
    This is used in read_bias_frames

    """

    num_files = len(images)
    if num_files <= 50:
        print("Must have at least 50 images as input.")
        raise NotEnoughDataException()
        sys.exit(1)

    shapes = [np.shape(image) for image in images]
    if len(set(shapes)) != 1:
        print("Input images must all have the same shape.")
        raise UnequalDataShapeException()
        sys.exit(1)
