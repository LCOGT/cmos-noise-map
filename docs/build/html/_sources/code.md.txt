# cmos-noise-map
Welcome to the cmos-noise-map package! This is designed to 



## Standard Deviation Noise Map

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

### Running the command

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

## Workflow 2

## Workflow 3

### Main wrapper function

<br>

```{eval-rst}
.. autofunction:: cmos_noise_map.main.cli
```

### Main functions to produce a read noise map

<br>

```{eval-rst}
.. autofunction:: cmos_noise_map.map_maker.MapMaker.__init__
```

<br><br>

```{eval-rst}
.. autofunction:: cmos_noise_map.map_maker.MapMaker.__init__
```

<br><br>

```{eval-rst}
.. autoclass:: cmos_noise_map.map_maker.STDMapMaker
.. autofunction:: cmos_noise_map.map_maker.STDMapMaker.create_map
```

<br><br>

```{eval-rst}
.. autoclass:: cmos_noise_map.map_maker.RTSMapMaker
.. autofunction:: cmos_noise_map.map_maker.RTSMapMaker.create_map
```

<br><br>

```{eval-rst}
.. autoclass:: cmos_noise_map.map_maker.RTSParameterMapMaker
.. autofunction:: cmos_noise_map.map_maker.RTSMapMaker.create_map
```
<br>

### Base functions to calculate the read noise from standard deviation

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
