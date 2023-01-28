#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 10:18:42 2023

@author: Prerana Kottapalli
"""
from sklearn.mixture import GaussianMixture
import numpy as np
import matplotlib.pyplot as plt
import scipy


def plot_get_rts(p, tol=5, upper_q=3, min_peak_sep=10):
    """
    The get_rts function with plotting functions to easily visualize what the algorithm is doing.

    Parameters
    ----------
    p : TYPE: list
        DESCRIPTION: List of pixel values across a set of bias frames
    tol : TYPE: float
        DESCRIPTION: The minimum difference between silhouette scores (likelihood of the model being correct)
                     between n_components=2 and 3. If there is a plateau (i.e. not much improvement between n=2 and n=3)
                     then the number of components chosen for the fit is 2. Not recommended to change unless you have
                     looked at the scores yourself.
    upper_q: TYPE: float
        DESCRIPTION: The upper standard deviation cutoff of pixels to be evaluated for telegraph noise.
    min_peak_sep: TYPE: float
        DESCRIPTION: The minimum separation of peaks for them to be considered separate peaks. If they are too close,
        the next lowest component is taken to be the model.


    Returns
    -------
    peak_location : TYPE: list(int), length = num_peaks
        DESCRIPTION: The means of each of the Gaussian modes calculated by GMM
    peak_widths : TYPE: list(int), length = num_peaks
        DESCRIPTION: The standard deviations of each Gaussian mode calculated by GMM
    peak_distance : TYPE: list(int), length = num_peaks-1
        DESCRIPTION: The difference between the means of each sequential mode
    num_peaks : TYPE: int
        DESCRIPTION: The number of Gaussians used to model the distribution of values of the pixel
    bad_idx_gmm : TYPE: list(int), shape(1,2)
        DESCRIPTION: The python array (not ds9) coordinate of the pixel modeled on the detector

    Plots
    ------
    Slihouette scores:
        The silhouette score is an indication of how likely it is that the calculated model accurately reflects the data.
        The higher the point on the graph, the more likely it is. This is used to determine the number of components needed
        to model data. Use this tool to set the minimum value difference for the silhouette score to be considered
        plateauing.

    Pixel histograms:
        A histogram representation of pixel data being fed in. Note that this is
        not the data the model fits to, but rather the probability density function.
        This can be used to determine the minimum peak separation you might need to
        consider them two separate peaks.

    Data and model plots:
        This plot shows the resultant gaussian components means and covariances (without amplitude),
        along with the pixel histogram in the top plot. The bottom shows the actual data variation.
        This plot does not limit the range on the axes, but it is recommended to do so in order to
        see the data more clearly.
    """
    n_clusters = np.arange(1, 4)
    if np.std(p) > upper_q:
        pixel = np.array(p).reshape(
            -1, 1
        )  # Need to reshape array for gmm algorithm to evaluate
        sils = []
        fits = []  # All possible models are carried through
        for n in n_clusters:
            gmm = GaussianMixture(
                n_components=n, n_init=2, covariance_type="full", random_state=1
            ).fit(pixel)
            sil = gmm.score(pixel)
            sils.append(sil)
            fits.append(gmm)
        # Choose n = 2 if the scores for 2 and 3 are very close
        n_components = n_clusters[np.argmax(sils)]
        if n_components == 3 or n_components == 2:
            if np.abs(sils[-1] - sils[-2]) < tol:
                n_components = 2

        if n_components == 2:
            peaks = fits[1].means_
            variances = fits[1].covariances_

            # If peaks are separated enough, then the fit continues
            if (
                np.abs(peaks[1] - peaks[0]) > min_peak_sep
            ):  # This is a bad criterion, change
                peak_location = peaks
                peak_widths = variances
                num_peaks = len(peaks)
                peak_distance = np.abs(peaks[1] - peaks[0])

            # If they are not well seperated, then choose to model with n=1
            elif np.abs(peaks[1] - peaks[0]) < min_peak_sep:
                peaks = fits[0].means_
                variances = fits[0].covariances_
                peak_location = peaks
                peak_widths = variances
                num_peaks = len(peaks)
                peak_distance = np.nan

        elif n_components == 3:
            peaks = fits[2].means_
            variances = fits[2].covariances_
            # If peaks are well separated, continue to model with n=3
            if (
                np.abs(peaks[2] - peaks[1]) >= min_peak_sep
                and np.abs(peaks[1] - peaks[0]) >= min_peak_sep
            ):
                peak_location = peaks
                peak_widths = variances
                num_peaks = len(peaks)
                peak_distance = (
                    np.abs(peaks[2] - peaks[1]),
                    np.abs(peaks[1] - peaks[0]),
                )

            # If peaks are not well separated try to model with n=1
            else:
                peaks = fits[0].means_
                variances = fits[0].covariances_
                peak_location = peaks
                peak_widths = variances
                num_peaks = len(peaks)
                peak_distance = np.nan

        elif n_components == 1:
            peaks = fits[0].means_
            variances = fits[0].covariances_
            peak_location = peaks
            peak_widths = variances
            num_peaks = len(peaks)
            peak_distance = np.nan
        # -------------Plotting-------------------

        fig, ax = plt.subplots(dpi=200)
        ax.errorbar(n_clusters, sils, yerr=None)
        ax.set_xticks(n_clusters)
        ax.set_title(
            str(np.abs(sils[-1] - sils[-2])) + "    " + str(n_components),
            fontname="Libre Franklin",
        )
        ax.set_xlabel("N. of clusters", fontname="Esteban")
        ax.set_ylabel("Score")
        for label in ax.get_xticklabels():
            label.set_fontproperties("Roboto")
        for label in ax.get_yticklabels():
            label.set_fontproperties("Roboto")
        ax.grid(True, alpha=0.1)
        ax.minorticks_on()
        ax.set_facecolor("#FFF9FB")
        fig.patch.set_facecolor("#FFF9FB")
        spine_names = ("top", "right", "left", "bottom")
        for spine_name in spine_names:
            ax.spines[spine_name].set_edgecolor("#D3D4D9")
        ax.spines["top"].set_edgecolor("#D3D4D9")
        fig.show()

        import matplotlib as mpl

        mpl.rcParams["axes.prop_cycle"] = mpl.cycler(
            color=["#4B88A2", "#BB0A21", "#252627", "#F39237", "#849324"]
        )
        gmm_x = np.linspace(min(pixel) - 5, max(pixel) + 5, 199)
        gmm_y = np.exp(fits[n_components - 1].score_samples(gmm_x.reshape(-1, 1)))
        fig, ax = plt.subplots(dpi=200)
        ax.hist(pixel, bins=15, density=True)  # , range = (450,520))
        ax.plot(gmm_x, gmm_y, alpha=0.8)
        ax.set_xlabel("Pixel counts (e-)", fontname="Esteban")
        for label in ax.get_xticklabels():
            label.set_fontproperties("Roboto")
        for label in ax.get_yticklabels():
            label.set_fontproperties("Roboto")
        ax.grid(True, alpha=0.1)
        ax.minorticks_on()
        ax.set_facecolor("#FFF9FB")
        fig.patch.set_facecolor("#FFF9FB")
        spine_names = ("top", "right", "left", "bottom")
        for spine_name in spine_names:
            ax.spines[spine_name].set_edgecolor("#D3D4D9")
        ax.spines["top"].set_edgecolor("#D3D4D9")
        plt.show()

        left, width = 0.1, 0.65
        bottom, height = 0.1, 0.65
        spacing = 0.005
        rect_scatter = [left, bottom, width, height]
        rect_scatter = [left, bottom, width, height]

        fig = plt.figure(figsize=(8, 8), dpi=250)

        ax1 = fig.add_axes(rect_scatter)
        ax_plotx = fig.add_axes(
            [left, bottom + height + spacing, width, 0.2], sharex=ax1
        )
        ax_plotx.tick_params(axis="x", labelbottom=False)
        ax1.scatter(np.array(p), np.linspace(1, len(p), len(p)))
        ax_plotx.axes.get_yaxis().set_ticklabels([])
        for i in np.arange(0, n_components):
            x = np.linspace(
                peaks[i][0] - 3 * variances[i][0][0],
                peaks[i][0] + 3 * variances[i][0][0],
                100,
            )
            ax_plotx.plot(
                x,
                scipy.stats.norm.pdf(x, peaks[i][0], variances[i][0][0]),
                label=f"Mean: {peaks[i][0]: 0.2f} Var: {variances[i][0][0]: 0.2f}",
                alpha=0.8,
            )
        ax_plotx.hist(pixel, bins=15, density=True)
        ax_plotx.plot(gmm_x, gmm_y, label="Full Model", alpha=0.8)
        ax1.set_xlabel("Pixel Value (ADU)", fontname="Esteban")
        ax1.set_ylabel("Image Number", fontname="Esteban")
        for ax in (ax_plotx, ax1):
            for label in ax.get_xticklabels():
                label.set_fontproperties("Roboto")
            for label in ax.get_yticklabels():
                label.set_fontproperties("Roboto")
            ax.grid(True, alpha=0.1)
            ax.minorticks_on()
            ax.set_facecolor("#FFF9FB")
            fig.patch.set_facecolor("#FFF9FB")
            spine_names = ("top", "right", "left", "bottom")
            for spine_name in spine_names:
                ax.spines[spine_name].set_edgecolor("#D3D4D9")
            ax.spines["top"].set_edgecolor("#D3D4D9")
        plt.legend()
        plt.title("Model fitted to Data", fontname="Libre Franklin")
        plt.show()
    else:
        peak_location, peak_widths, peak_distance, num_peaks = [
            np.nan,
            np.nan,
            np.nan,
            np.nan,
        ]
    return peak_location, peak_widths, peak_distance, num_peaks


# -------------------------------------------
def noise_distribution(data, gain=None):
    """
    This function plots the noise distribution of the detector, This is obtained
    by taking the standard deviation of the values of a single pixel across images,
    for every pixel. Then these standard deviations are represented in histogram form
    with lines at the median and 90th percentile. This tool is meant to help
    determine the upper cutoff value for

    Parameters
    ----------
    data : stack of opened bias frames
        DESCRIPTION. A shape (N, X, Y) array where N is the number of images, X is the number of rows of pixels
        and Y is the number of columns of pixels.
    gain : float, optional
        DESCRIPTION. The gain setting of the detector. The default is None.

    Returns
    -------
    A plot that shows the noise distribution on the detector.

    """
    if gain:
        stdimage = np.std(data, axis=0) * gain
    else:
        stdimage = np.std(data, axis=0)

    upper_q = np.quantile(stdimage, 0.90)
    median = np.median(stdimage)
    std = scipy.stats.median_abs_deviation(stdimage, axis=None)

    plt.style.use("default")
    hist_data = stdimage.flatten()
    fig, ax = plt.subplots(1, 2, dpi=200, figsize=(15, 5))
    ax.hist(
        hist_data,
        density=True,
        bins=1000,
        range=[median - 5 * std, median + 7 * std],
        color="#252627",
    )
    ax.vlines(median, 0, 5.5, color="#BB0A21", linestyle="--", alpha=0.8)
    ax.vlines(upper_q, 0, 0.75, color="#BB0A21", linestyle="--", alpha=0.8)
    ax.text(1.25, 5.25, f"Median = {median}", fontsize=12, fontname="Roboto")
    ax.text(1.5, 0.5, f"90th pct = {upper_q}", fontsize=12, fontname="Roboto")
    ax.set_title(
        "Distribution of Per Pixel Noise", fontname="Libre Franklin", fontsize=20
    )
    ax.set_xlabel("Per pixel noise", fontname="Cantarell")
    ax.tick_params(axis="x", which="minor", length=2)

    for label in ax.get_xticklabels():
        label.set_fontproperties("Roboto")
    for label in ax.get_yticklabels():
        label.set_fontproperties("Roboto")
    ax.grid(True, alpha=0.1)
    ax.minorticks_on()
    ax.set_facecolor("#FFF9FB")
    fig.patch.set_facecolor("#FFF9FB")
    spine_names = ("top", "right", "left", "bottom")
    for spine_name in spine_names:
        ax.spines[spine_name].set_edgecolor("#D3D4D9")
    ax.spines["top"].set_edgecolor("#D3D4D9")
    fig.show()
