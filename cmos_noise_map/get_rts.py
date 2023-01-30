"""
Created on Fri Jan 20 15:01:53 2023

@author: Prerana Kottapalli
"""

import numpy as np
from sklearn.mixture import GaussianMixture


def readnoise(means, variances, num_peaks, amplitudes):
    """
    A function that takes model parameters for each pixel and converts it to a
    single readnoise value.

    Parameters
    ----------
    means : array of floats, shape (N, 1) where N is the number of model components
        The means of each gaussian used to create the model.
    variances : array of floats, shape (N, 1) where N is the number of model components
        The covariance matrices of each gaussian used to create the model.
    num_peaks : int
        The optimal number of peaks found by the get_rts function
    amplitudes : list of len(N) where N is the number of model components
        The amplitude of each gaussian component modelled by get_rts.

    Returns
    -------
    readnoise : float
        The standard deviation of the pixel whose parameters are passed through, which is taken to be the read noise.

    """
    if not np.isnan(num_peaks):
        if num_peaks > 1:
            var = [
                np.trace(variances[i]) / num_peaks for i in range(0, num_peaks)
            ]  # Get variance from covariance
            noise = (
                np.sum(np.dot(amplitudes, var))
                + np.sum(np.dot(amplitudes, means.flatten() ** 2))
                - np.sum(np.dot(amplitudes, means)) ** 2
            )
        else:
            var = variances
            noise = (
                np.sum(np.dot(amplitudes, var))
                + np.sum(np.dot(amplitudes, means**2))
                - np.sum(np.dot(amplitudes, means)) ** 2
            )

        readnoise = np.sqrt(noise)
    else:
        readnoise = np.nan
    return readnoise


def get_rts(p, tolerance=0.05, upper_quantile=3, min_peak_separation=10):
    """
    Uses a Gaussian Mixture model, which is essentially a series of gaussian distributions of different means,
    variances, and amplitudes added together to model the clustering of data points.
    To avoid overfitting, we go through a series of logical checks to ensure that data is being fitted properly.
    This does NOT re-evaluate the model with every logical step, all possible fit_funs (constrained by physics)
    are carried through the steps.

    Parameters
    ----------
    p : TYPE: list
        DESCRIPTION: List of pixel values across a set of bias frames
    tolerance : TYPE: float
        DESCRIPTION: The minimum difference between silhouette scores (likelihood of the model being correct)
                     between n_components=2 and 3. If there is a plateau (i.e. not much improvement between n=2 and n=3)
                     then the number of components chosen for the fit is 2. Not recommended to change unless you have
                     looked at the scores yourself.
    upper_quantile: TYPE: float
        DESCRIPTION: The upper standard deviation cutoff of pixels to be evaluated for telegraph noise.
    min_peak_separation: TYPE: float
        DESCRIPTION: The minimum separation of peaks for them to be considered separate peaks. If they are too close,
        the next lowest component is taken to be the model.


    Returns
    -------
    peak_location : TYPE: list(float), length = num_peaks
        DESCRIPTION: The means of each of the Gaussian modes calculated by GMM
    peak_widths : TYPE: list(float), length = num_peaks
        DESCRIPTION: The covariance of each Gaussian mode calculated by GMM
    num_peaks : TYPE: int
        DESCRIPTION: The number of Gaussians used to model the distribution of values of the pixel
    amp : TYPE: list(float)
        DESCRIPTION: The weights of each gaussian in the mixture. All weights sum to 1.

    """
    n_clusters = np.arange(1, 4)
    if np.std(p) > upper_quantile:
        pixel = p.reshape(-1, 1)  # Need to reshape array for gmm algorithm to evaluate
        silhouette_scores = []
        fit_funs = []  # All possible models are carried through
        for n in n_clusters:
            gmm = GaussianMixture(
                n_components=n, n_init=2, covariance_type="full", random_state=1
            ).fit(pixel)
            score = gmm.score(pixel)
            silhouette_scores.append(score)
            fit_funs.append(gmm)
        # Choose n = 2 if the scores for 2 and 3 are very close
        n_components = n_clusters[np.argmax(silhouette_scores)]
        if n_components == 3 or n_components == 2:
            if np.abs(silhouette_scores[-1] - silhouette_scores[-2]) < tolerance:
                n_components = 2

        if n_components == 2:
            peaks = fit_funs[1].means_
            variances = fit_funs[1].covariances_
            amplitudes = fit_funs[1].weights_

            # If peaks are separated enough, then the fit continues
            if (
                np.abs(peaks[1] - peaks[0]) > min_peak_separation
            ):  # This is a bad criterion, change
                peak_location = peaks
                peak_widths = variances
                num_peaks = len(peaks)
                amp = amplitudes

            # If they are not well seperated, then choose to model with n=1
            elif np.abs(peaks[1] - peaks[0]) < min_peak_separation:
                peaks = fit_funs[0].means_
                variances = fit_funs[0].covariances_
                amplitudes = fit_funs[0].weights_
                peak_location = peaks
                peak_widths = variances
                num_peaks = len(peaks)
                amp = amplitudes

        elif n_components == 3:
            peaks = fit_funs[2].means_
            variances = fit_funs[2].covariances_
            amplitudes = fit_funs[2].weights_
            # If peaks are well separated, continue to model with n=3
            if (
                np.abs(peaks[2] - peaks[1]) >= min_peak_separation
                and np.abs(peaks[1] - peaks[0]) >= min_peak_separation
            ):
                peak_location = peaks
                peak_widths = variances
                num_peaks = len(peaks)
                amp = amplitudes

            # If peaks are not well separated try to model with n=1
            else:
                peaks = fit_funs[0].means_
                variances = fit_funs[0].covariances_
                amplitudes = fit_funs[0].weights_
                peak_location = peaks
                peak_widths = variances
                num_peaks = len(peaks)
                amp = amplitudes
        # If n=2 and n=3 modesl are not appropriate, model with one component.
        elif n_components == 1:
            peaks = fit_funs[0].means_
            variances = fit_funs[0].covariances_
            amplitudes = fit_funs[0].weights_
            peak_location = peaks
            peak_widths = variances
            num_peaks = len(peaks)
            amp = amplitudes
    # If pixel is not noisy, return nans to maintain data structure
    else:
        peak_location, peak_widths, num_peaks, amp = [np.nan, np.nan, np.nan, np.nan]
    return peak_location, peak_widths, num_peaks, amp


def per_pixel_readnoise(p, **kwargs):
    """
    A function wrapping get_rts and readnoise to get to the pixel readnoise

    Parameters
    ----------
    p : list
        DESCRIPTION. List of values of one pixel across images
    **kwargs :
        Arguments to be passed to get_rts

    Returns
    -------
    pixel_readnoise : float
        Calculated readnoise for one pixel

    """
    means, variances, num_peaks, amplitudes = get_rts(p, **kwargs)
    pixel_readnoise = readnoise(means, variances, num_peaks, amplitudes)
    return pixel_readnoise
