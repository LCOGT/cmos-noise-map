#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 16:00:36 2023

@author: pkottapalli
"""
import numpy as np
from get_rts import get_rts

test_data = np.load('tests/test_data.npy', allow_pickle=True)

def get_rts_test(test_data):
    means = []
    num_peaks = []
    for p in test_data.flatten():
        mean, _, num, _ = get_rts(p, tol = 0.03, upper_q = 10, min_peak_sep=10)
        means.append(mean)
        num_peaks.append(num)
    
    #Check that number of peaks are the same
    true_peaks = [2, 3, 1, 3, 2, 3]
    test_peaks = np.array(num_peaks)[~np.isnan(num_peaks)]
    if len(true_peaks) == len(test_peaks):
        if np.array(test_peaks-true_peaks).all() == 0:
            num_peak_test = True
        else:
            num_peak_test=False
    
    #Check that means are close
    true_means = [[100,10], [10, 100, 190], [100], [10, 100, 190],[10, 80], [10, 100, 190]] #Taken from data in make_test_data
    test_means = []
    for i in means:
        if not np.isnan(i).all():
            test_means.append(i.flatten())
    if len(true_means) == len(test_means) and num_peak_test==True:
        for i in range(len(true_means)):
            test_bools = np.isclose(np.sort(true_means[i]), np.sort(test_means[i]), atol = 6)
            if test_bools.all() == True:
                means_test=True
            else:
                means_test=False

        
    if num_peak_test == True and means_test == True:
        print('get_rts.py test passed!')
        
get_rts_test(test_data)
             
    
    