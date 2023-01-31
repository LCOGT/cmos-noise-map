# cmos-noise-map

## Workflow 1

The default way that the RTS map maker makes a noise map is by taking the standard deviation of the input bias images. 
The standard deviation is taken along the 0th axis i.e. the resultant map has the same shape of the input images, and 
each element is the standard deviation of a single pixel, across each of the bias images.

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
