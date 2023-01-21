#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 16:00:36 2023

@author: pkottapalli
"""
import numpy as np
import random
import matplotlib.pyplot as plt

test_data = np.zeros((5,5), dtype=object)
# Perfect trimodal and bimodal
N=200
mu, sigma = 100, 30
mu2, sigma2 = 10, 15
X1 = np.random.normal(mu, sigma, N)
X2 = np.random.normal(mu2, sigma2, N)
X = np.concatenate([X1, X2])
random.shuffle(X)
test_data[0,0]=X
plt.hist(X, bins = 15)
plt.title('Synthetic data for a well-defined bimodal distribution')
plt.xlabel('Fake pixel value')
plt.show()

N=200
mu, sigma = 100, 15
mu2, sigma2 = 10, 30
mu3, sigma3 = 190, 30
X1 = np.random.normal(mu, sigma, N)
X2 = np.random.normal(mu2, sigma2, N)
X3 = np.random.normal(mu3, sigma3, N)
X = np.concatenate([X1, X2, X3])
random.shuffle(X)
plt.hist(X, bins = 30)
plt.title('Synthetic data for a well-defined trimodal distribution')
plt.xlabel('Fake pixel value')
plt.show()
test_data[3,4]=X

# More noisy (more overlap, filling in the gaps) trimodal and bimodal
N=200
mu, sigma = 80, 30
mu2, sigma2 = 10, 20
X1 = np.random.normal(mu, sigma, N)
X2 = np.random.normal(mu2, sigma2, 150)
X = np.concatenate([X1, X2])
random.shuffle(X)
test_data[2,3]=X
plt.hist(X, bins = 15)
plt.title('Synthetic data for a ill-defined bimodal distribution')
plt.xlabel('Fake pixel value')
plt.show()
plt.scatter(np.arange(len(X)), X)
plt.show()

N=200
mu, sigma = 100, 23
mu2, sigma2 = 10, 30
mu3, sigma3 = 190, 30
X1 = np.random.normal(mu, sigma, N)
X2 = np.random.normal(mu2, sigma2, 100)
X3 = np.random.normal(mu3, sigma3, 100)
X = np.concatenate([X1, X2, X3])
random.shuffle(X)
test_data[1,4]=X
plt.hist(X, bins = 30)
plt.title('Synthetic data for a well-defined trimodal distribution')
plt.xlabel('Fake pixel value')
plt.show()
plt.scatter(np.arange(len(X)), X)
plt.show()

N=200
mu, sigma = 100, 28
mu2, sigma2 = 10, 30
mu3, sigma3 = 190, 30
X1 = np.random.normal(mu, sigma, N)
X2 = np.random.normal(mu2, sigma2, 130)
X3 = np.random.normal(mu3, sigma3, 130)
X = np.concatenate([X1, X2, X3])
random.shuffle(X)
test_data[0,2]=X
plt.hist(X, bins = 30)
plt.title('Synthetic data for a well-defined trimodal distribution')
plt.xlabel('Fake pixel value')
plt.show()
plt.scatter(np.arange(len(X)), X)
plt.show()
# Wide unimodal
N=500
mu, sigma = 100, 60
X = np.random.normal(mu, sigma, N)
random.shuffle(X)
test_data[0,3] = X
plt.hist(X, bins = 30)
plt.title('Synthetic data for a well-defined trimodal distribution')
plt.xlabel('Fake pixel value')
plt.show()
plt.scatter(np.arange(len(X)), X)
plt.show()

# Normal pixels
sigmas = np.random.randint(5, 10, 19)
mus = np.random.randint(50, 150, 19)
N=400
for i in range(len(sigmas)):
    mu = mus[i]
    sigma = sigmas[i]
    X = np.random.normal(mu, sigma, N)
    random.shuffle(X)
    for j, k in zip(range(5), range(5)):
        try:
            if test_data[j,k] == 0:
                test_data[j, k] = X
            else:
                pass
        except ValueError:
            pass
    plt.hist(X, bins = 30)
    plt.title('Synthetic data for a normal distribution')
    plt.xlabel('Fake pixel value')
    plt.show()
    plt.scatter(np.arange(len(X)), X)
    plt.show()

test_results = []
for p in test_data.flatten():
    test_results.append(get_rts(p, tol = 0.05, upper_q = 10, min_peak_sep=10))