#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 16:00:36 2023

@author: Prerana Kottapalli
"""
import numpy as np

from cmos_noise_map.get_rts import get_rts, readnoise


def test_get_rts():
    """
    Takes the test_data.npy file in the tests directory, runs the get_rts
    function on it, and matches peak locations and number of peaks.

    Parameters
    ----------
    test_data : float, array(any,N,N)
        A mock pixel array, with varying amounts of samples and modality.

    Returns
    -------
    None.

    """
    test_data = np.load("cmos_noise_map/tests/test_data.npy", allow_pickle=True)
    means = []
    num_peaks = []
    for p in test_data.flatten():
        mean, _, num, _ = get_rts(
            p, tolerance=0.03, upper_quantile=10, min_peak_separation=10
        )
        means.append(mean)
        num_peaks.append(num)

    # Check that number of peaks are the same
    true_peaks = [2, 3, 1, 3, 2, 3]
    test_peaks = np.array(num_peaks)[~np.isnan(num_peaks)]
    if len(true_peaks) == len(test_peaks):
        if np.array(test_peaks - true_peaks).all() == 0:
            num_peak_test = True
        else:
            num_peak_test = False

    # Check that means are close
    true_means = [
        [100, 10],
        [10, 100, 190],
        [100],
        [10, 100, 190],
        [10, 80],
        [10, 100, 190],
    ]  # Taken from data in make_test_data
    test_means = []
    for i in means:
        if not np.isnan(i).all():
            test_means.append(i.flatten())
    if len(true_means) == len(test_means) and num_peak_test is True:
        for i in range(len(true_means)):
            test_bools = np.isclose(
                np.sort(true_means[i]), np.sort(test_means[i]), atol=6
            )
            # 6 chosen so that fake data passes tests, and because it is less than min peak separation.
            if test_bools.all():
                means_test = True
            else:
                means_test = False

    # Both tests need to pass for overall pass
    assert num_peak_test and means_test


def test_readnoise():
    """
    Takes one UNIMODAL pixel in the test_data.npy file in the tests directory, runs the readnoise
    function on it, and compares the true and calculated standard deviations.

    Parameters
    ----------
    test_data : float, array(any,N,N)
        A mock pixel array, with varying amounts of samples and modality.

    Returns
    -------
    None.

    """
    # Test that variance of a unimodal distribution is still the same
    test_data = np.load("cmos_noise_map/tests/test_data.npy", allow_pickle=True)
    mean, variance, num_peaks, amps = get_rts(test_data[0, 3])
    noise = readnoise(mean, variance, num_peaks, amps)
    true_noise = 60
    assert np.abs(noise - true_noise) < 1
