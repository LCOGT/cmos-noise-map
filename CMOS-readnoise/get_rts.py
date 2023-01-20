"""
Created on Fri Jan 20 15:01:53 2023

@author: prera
"""

from astropy.io import fits
from glob import glob
import numpy as np
from sklearn.mixture import GaussianMixture

files = glob('/run/media/pkottapalli/Untitled/411_mod3_gain30_bin1_telegraph/*.fits', recursive = True)
im_test = fits.open(files[0])[0].data
data = []
shape = np.shape(im_test)
for t in glob('/run/media/pkottapalli/Untitled/Temp/*', recursive = True):
    temp = np.memmap(t, dtype = im_test.dtype , mode = 'r', shape = (1,shape[1]))
    data.append(temp)
    del temp

im_test = fits.open(files[0])[0].data
data = []
shape = np.shape(im_test)
for t in glob('/run/media/pkottapalli/Untitled/Temp/*', recursive = True):
    temp = np.memmap(t, dtype = im_test.dtype , mode = 'r', shape = (1,shape[1]))
    data.append(temp)
    del temp

dshape = np.shape(data)
x, y = np.meshgrid(range(dshape[1]),range(dshape[2]), indexing = 'ij')
indices = np.column_stack((x[-1].ravel(),y[-1].ravel())).tolist()
pixels = np.reshape(np.transpose(data), (dshape[2]*dshape[1], dshape[0])).tolist()

def get_rts(p, tol = 0.05, upper_q = 3, min_peak_sep = 10):
    """
    Uses a Gaussian Mixture model, which is essentially a series of gaussian distributions of different means, 
    variances, and amplitudes added together to model the clustering of data points.
    To avoid overfitting, we go through a series of logical checks to ensure that data is being fitted properly.
    This does NOT re-evaluate the model with every logical step, all possible fits (limited due to physics)
    are carried through the steps.

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

    """
    n_clusters=np.arange(1, 4)
    if np.std(p) > upper_q:
        pixel = np.array(p).reshape(-1,1) #Need to reshape array for gmm algorithm to evaluate
        sils=[]
        fits = [] #All possible models are carried through
        for n in n_clusters:
            gmm=GaussianMixture(n_components=n, n_init=2, covariance_type = 'full', random_state = 1).fit(pixel)
            sil=gmm.score(pixel)
            sils.append(sil)
            fits.append(gmm)
        #Choose n = 2 if the scores for 2 and 3 are very close
        n_components = n_clusters[np.argmax(sils)]
        if n_components == 3 or n_components == 2:
            if np.abs(sils[-1]-sils[-2]) < tol:
                n_components = 2
        
        if n_components == 2:
            peaks = fits[1].means_
            variances = fits[1].covariances_
            
            #If peaks are separated enough, then the fit continues
            if np.abs(peaks[1]-peaks[0]) > min_peak_sep: #This is a bad criterion, change
                peak_location=peaks
                peak_widths=variances
                num_peaks=len(peaks)
                peak_distance=np.abs(peaks[1]-peaks[0])
            
            #If they are not well seperated, then choose to model with n=1
            elif np.abs(peaks[1]-peaks[0]) < min_peak_sep:
                peaks = fits[0].means_
                variances = fits[0].covariances_
                peak_location=peaks
                peak_widths=variances
                num_peaks=len(peaks)
                peak_distance=np.nan
        
        elif n_components == 3:
            peaks = fits[2].means_
            variances = fits[2].covariances_
            #If peaks are well separated, continue to model with n=3
            if np.abs(peaks[2]-peaks[1]) >= min_peak_sep and np.abs(peaks[1]-peaks[0]) >= min_peak_sep:
                peak_location=peaks
                peak_widths=variances
                num_peaks=len(peaks)
                peak_distance=(np.abs(peaks[2]-peaks[1]), np.abs(peaks[1]-peaks[0]))
            
            #If peaks are not well separated try to model with n=1
            else:
                peaks = fits[0].means_
                variances = fits[0].covariances_
                peak_location=peaks
                peak_widths=variances
                num_peaks=len(peaks)
                peak_distance=np.nan
        #If n=2 and n=3 modesl are not appropriate, model with one component.
        elif n_components == 1:
            peaks = fits[0].means_
            variances = fits[0].covariances_
            peak_location=peaks
            peak_widths=variances
            num_peaks=len(peaks)
            peak_distance=np.nan
    #If pixel is not noisy, return nans to maintain data structure
    else:
        peak_location, peak_widths, peak_distance, num_peaks = [np.nan, np.nan, np.nan, np.nan]
    #!TODO: convert to read noise per pixel. Maybe build a separate function to do that. Or puit everything together into a class.
    return peak_location, peak_widths, peak_distance, num_peaks