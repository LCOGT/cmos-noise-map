# CMOS Noise Map
[![Python application](https://github.com/LCOGT/cmos-noise-map/actions/workflows/python-app.yml/badge.svg)](https://github.com/LCOGT/cmos-noise-map/actions/workflows/python-app.yml)

[![Documentation Status](https://readthedocs.org/projects/cmos-noise-map/badge/?version=latest)](https://cmos-noise-map.readthedocs.io/en/latest/?badge=latest)

Code to model random telegraph noise in a CMOS detector. Originally designed for the Las Cumbres Observatory BANZAI pipeline.
Authors: Prerana Kottapalli, Matt Daily, Curtis McCully

Read the docs: https://cmos-noise-map.readthedocs.io/en/latest/index.html

## Installation
### From PyPi
```
pip install cmos-noise-map
```

### From Github
To install the tool, clone this repository and run:

```
pip install poetry
cd cmos-noise-map
poetry install
```
## Tests
To run the unit tests, simply run:

`poetry run pytest`

## Usage
Once you've installed the tool, it can be run simply by:
`rts-maker <path> <options> <write filename>`

```
Usage: rts-maker [OPTIONS] PATH [METHOD] [FILEPATH]

  This script builds a noise map with the chosen method.

  path: Path to input without the .fits at the end

  filepath:OPTIONAL Path to write file

  method: Default method is std. Available methods are std, rts, and param.
  See docs for more information about each method.

Options:
  -r, --data_ext TEXT             Extension of fits file that contains the
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
  -f, --fpack                     Adding this option will fpack your output
                                  fits file
  -b, --bias_check                Adding this option will skip the check to
                                  see if files used are bias files  [default:
                                  True]
  --help                          Show this message and exit.
```
