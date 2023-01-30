# Future Directions

## Overfitting in GMM
The current way that we avoid overfitting is by taking a standard deviation cutoff so only some pixels are evaluated, 
and the peak separation and silhouette score plateauing checks were found by trial by error. There are other methods prescribed to avoid overfitting in a gaussian mixture model.
One such resource is [this article by J. Andrews et al 2018](https://www.sciencedirect.com/science/article/abs/pii/S0167947318301245?fr=RR-2&ref=pdf_download&rr=78b0d4af1ef42b89)
which dicusses using a bootstrap sampling algorithm to find the optimal number of components for the fit.

<br>

Without changing the algorithm, Python 3.10 has implemented a [match case algorithm](https://docs.python.org/3/whatsnew/3.10.html#pep-634-structural-pattern-matching) which should speed up the overfitting checks as they stand now.

## Error Propagation
There are other ways to extract the read noise from the mixture model like [in Zhang et al 2019](https://link-springer-com.proxy.library.ucsb.edu:9443/article/10.1007/s00158-019-02301-y#Sec1), which may warrant exploration if the current method is not found
rigorous enough.

## Other solutions for CMOS noise

There is another type of noise (SUTR)