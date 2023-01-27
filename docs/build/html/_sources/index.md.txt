% CMOS Noise Map documentation master file, created by
% sphinx-quickstart on Tue Jan 24 16:36:45 2023.
% You can adapt this file completely to your liking, but it should at least
% contain the root `toctree` directive.

# CMOS Noise Map documentation

```{toctree}
:caption: 'Contents:'
:maxdepth: 2

algorithm
code
```
#### Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`

## About this project

This project was started in 2022, as the Las Cumbres Observatory Delta Rho upgrades were underway. We investigated the properties of random telegraph signal, which are further discussed in [The Algorithm Section](algorithm.md), 
and pondered how to deal with it in the new QHY600 cameras being installed at various LCO 0.4m telescopes. We decided to propagate noise as a 2D error map, similar to the [bad pixel map maker](https://github.com/LCOGT/pixel-mask-gen). 
This document has information about why we chose to address the problem of RTS in the way that we did, documents the code, and contains suggestions for future directions and improvements on this work.

## Usage
