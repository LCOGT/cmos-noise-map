# CMOS Noise Map
Code to model random telegraph noise in a CMOS detector. Originally designed for the Las Cumbres Observatory BANZAI pipeline.
Authors: Prerana Kottapalli, Matt Daily, Curtis McCully

## Installation
### From PyPi
¯\_(ツ)_/¯ Not on Pypi yet

### From Github
To install the tool, clone this repository and run:

```
cd pixel-mask-gen
poetry install
```
## Tests
To run the unit tests, simply run:

`poetry run pytest`

## Usage
Once you've installed the tool, it can be run simply by:
`rts-maker <path> <options> <write filename>`

```
  path: Path to input without the .fits at the end

  filename: Path to write file, including the filename ending in .fits

  method: Default method is std. Available methods are std, rts, and param.
  See docs for more information about each method.

Options:
  -r, --data_ext INTEGER    Extension of fits file that contains the image
                            data
  -uq, --upper_q FLOAT      Standard deviation cutoff for pixel noise
                            evaluation
  -t, --tol FLOAT           The minimum difference between silhouette scores.
                            See docs for more information.
  -m, --min_peak_sep FLOAT  Minimum difference between pixel value cluster
                            centers to be considered separate clusters
  --help                    Show this message and exit.

```
