% CMOS Noise Map documentation master file, created by
% sphinx-quickstart on Tue Jan 24 16:36:45 2023.
% You can adapt this file completely to your liking, but it should at least
% contain the root `toctree` directive.

# CMOS Noise Map documentation

```{toctree}
:caption: 'Contents:'
:maxdepth: 2

code
algorithm
future-directions
playground_demo

```

## About this project

This project was started in 2022, as the Las Cumbres Observatory Delta Rho upgrades were underway. We investigated the properties of random telegraph signal, which are further discussed in [The Algorithm Section](algorithm.md), 
and pondered how to deal with it in the new QHY600 cameras being installed at various LCO 0.4m telescopes. We decided to propagate noise as a 2D error map, similar to the [bad pixel map maker](https://github.com/LCOGT/pixel-mask-gen). 
This document has information about why we chose to address the problem of RTS in the way that we did, documents the code, and contains suggestions for future directions and improvements on this work.

## Installation

### From PyPi

¯\_(ツ)_/¯ Not on Pypi yet

### From GitHub

```
cd cmos-noise-map
poetry install
```

## Usage

```
Usage: rts-maker [OPTIONS] PATH FILENAME [METHOD]

  This script builds a noise map with the chosen method.

  path: Path to input without the .fits at the end

  filename: Path to write file, including the filename ending in .fits

  method: Default method is std. Available methods are std, rts, and param.
  See docs for more information about each method.

Options:
  -r, --data_ext INTEGER          Extension of fits file that contains the
                                  image data
  -uq, --upper_quantile FLOAT     Standard deviation cutoff for pixel noise
                                  evaluation
  -t, --tolerance FLOAT           The minimum difference between silhouette
                                  scores. See docs for more information.
  -m, --min_peak_separation FLOAT
                                  Minimum difference between pixel value
                                  cluster centers to be considered separate
                                  clusters
  -o, --out_hdu_name TEXT         Name for the header in which the data will
                                  be stored
  --help                          Show this message and exit.

```
## Tests
To run the unit tests, simply run:
```
poetry run pytest
```

#### Indices and tables

- {ref}`genindex`
- {ref}`search`