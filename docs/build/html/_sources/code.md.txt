# cmos-noise-map
This package was designed to create a read noise map for CMOS sensors, which often have pixels affected by [Random Telegraph Signal](algorithm.md).

**Inputs**
<br>
The expected inputs are at least **50** bias images which all have **the same shape**. This is so that the resulting outputs are statistically significant, and so that data can be properly handled.

**Methods**
<br>
There are a few utilities that cmos-noise-map provides, two of which are for creating a read noise map, and one of which is specifically for pixel noise modelling.

1. `std`: Standard Deviation Noise Map
2. `rts`: Gaussian Mixture Modeled Noise Map
3. `param`: Parameter Map

**Outputs**
If the method selected is either `std` or `rts`, the output file will be a `.fits` data file, in the `'PRIMARY'` or user specified header (by using the option `--out_hdu_name`)
If the method selected is `param`, the file will be written out as a `.csv` file

<br>

## Standard Deviation Noise Map [Default]

The default way that the RTS map maker makes a noise map is by taking the standard deviation of the input bias images. 
The standard deviation is taken along the 0th axis i.e. the resultant map has the same shape of the input images, and 
each element is the standard deviation of a single pixel, across each of the bias images.

```{eval-rst}
.. image:: images/Standard-Deviation.png
    :alt: "Three square grid blocks stacked on top of another, with a highlighted pixel in the top left corner. An arrow goes through the corner, and points to a highlighted pixel in a fourth grid block."
```
Above is an example of how to take the standard deviation of a pixel across images. The standard deviation of the three gray pixel values is the value recorded in the red pixel of the resultant map.

This is the simplest way to create a read noise map given a bias frame. This method is chosen as the default since it is significantly faster than modelling each pixel and calculating the read noise.
The results are comparable enough that this is ok.

#### Running the command

Since this method is the default, we can get away with a simple command:

```
rts-maker <input-files-directory> <output-file-name-and-path>
```

And once run, you should see a progress bar pop up, with an estimate of the time left to completion.

---
**Note:** This method does not use the `upper_quantile`, `tolerance`, or `min_peak_separation` options.

---

Whether or not your files are fpacked, the [read_bias_frames](read_write_files.md) function will take care of it. The files are read in with memory mapping,
so theoretically we can take an arbitrarily large number of images.
<br>
Once the map is created, a fits file will be created in the path specified with the name provided. The [write function](read_write_files.md) does not currently have fpacking capabilities.

<br>

```{eval-rst}
.. autoclass:: cmos_noise_map.map_maker.STDMapMaker
.. autofunction:: cmos_noise_map.map_maker.STDMapMaker.create_map
```

<br>

## Model Pixel Noise with GMM

The second way provided by cmos-noise-map to create a read noise map is by using a [Gaussian Mixture Model](algorithm.md) to determine the read noise for pixels that are not uniformly distributed.
This method is a more statistically rigorous way to determine read noise, but the algorithm is very computationally expensive. For a large CMOS sensor with a large amount of data being sampled, the process can take **days**.
This is why this method is not the default. However, the process ideally need only be run once so users may be interested in using it.

#### Running the command

The command is formatted as follows:

```
rts-maker <input-files-directory> --upper_quantile <float, optional> --tolerance <float, optional> --min_peak_separation <float, optional> <output-file-name-and-path> rts
```

Understanding the options here is important. For more information please visit the [page explaining these in detail](algorithm.md), but in brief:
- `--upper_quantile` is the noisiness cutoff for evaluating pixels. The algorithm does not evaluate every pixel, only pixels whose **standard deviation** is above this cutoff. 
By default it calculates the cutoff to be the 80th percentile of the standard deviation of all pixels. We **recommend changing the parameter** according to your data.
Please consider using the [RTS playground](playground.md) to determine this parameter for your data.
- `--tolerance: default=0.05` is an overfitting parameter. This is the minimum difference in the quality of fit between a model with 2 gaussians, and a model with 3. This parameter generally does not need to be changed.
- `--min_peak_separation: default=10` is the minimum separation between two modes in a multimodal pixel noise distribution, for them to be considered separate. Please consider using the [RTS playground](playground.md) to determine this parameter for your data.

The files are read in with memory-mapping in order to not use up memory carrying around data. 
However, the process is multiprocessed (implemented via [sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.mixture.GaussianMixture.html)), so your CPU will be working hard during this process.
Finally, the resultant file has the same shape as the input images, and each element is the calculated pixel read noise value. This is [written out](read_write_files.md) as a fits file in the path specified with the name provided.

<br>

```{eval-rst}
.. autofunction:: cmos_noise_map.map_maker.MapMaker.__init__
```

<br><br>

```{eval-rst}
.. autoclass:: cmos_noise_map.map_maker.RTSMapMaker
.. autofunction:: cmos_noise_map.map_maker.RTSMapMaker.create_map
```

<br><br>

```{eval-rst}
.. autofunction:: cmos_noise_map.get_rts.get_rts
```

<br><br>

```{eval-rst}
.. autofunction:: cmos_noise_map.get_rts.readnoise
```
<br><br>

```{eval-rst}
.. autofunction:: cmos_noise_map.get_rts.per_pixel_readnoise
```

<br>

## Getting pixel model params from GMM

This is a utility provided by the package for those who might want the parameters from our [GMM modelling scheme](algorithm.md), to do things like get more accurate estimates of photometry errors.
The method is unchanged from above, we just stop short of calculating read noise, and the file [written out](read_write_files.md) is written as a `csv` file. We provide a utility function to read this csv files in, in a way that can be read by the functions
in `cmos-noise-map`.

#### Running the Command

```
rts-maker <input-files-directory> --upper_quantile <float, optional> --tolerance <float, optional> --min_peak_separation <float, optional> <output-file-name-and-path> param
```

All the parameters use are the same as the `rts` method, and parameters should be adjusted in the same way.

Below is an example of using this parameter map to get the read noise of each pixel again.

```
from cmos_noise_map.utils.read_write_utils import read_parameter_table
from cmos_noise_map.get_rts import readnoise

means, var, num_peaks, amps = read_parameter_table(test.csv)

readnoise_map = []
for i in range(len(means)):
    pixel_readnoise = readnoise(means[i], var[i], num_peaks[i], amps[i])
    readnoise_map.append(pixel_readnoise)
```

<br>

```{eval-rst}
.. autofunction:: cmos_noise_map.map_maker.MapMaker.__init__
```

<br><br>

```{eval-rst}
.. autoclass:: cmos_noise_map.map_maker.RTSParameterMapMaker
.. autofunction:: cmos_noise_map.map_maker.RTSMapMaker.create_map
```

<br><br>

```{eval-rst}
.. autofunction:: cmos_noise_map.utils.read_write_utils.read_parameter_table
```

<br>

## Main wrapper function

<br>

```{eval-rst}
.. autofunction:: cmos_noise_map.main.cli
```

## Base functions to calculate the read noise from standard deviation

<br>

```{eval-rst}
.. autofunction:: cmos_noise_map.get_rts.get_rts
```

<br><br>

```{eval-rst}
.. autofunction:: cmos_noise_map.get_rts.readnoise
```
<br><br>

```{eval-rst}
.. autofunction:: cmos_noise_map.get_rts.per_pixel_readnoise
```

<br>
