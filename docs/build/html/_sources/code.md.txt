# cmos-noise-map

## Code documentation

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


### Read and write functions

<br>

```{eval-rst}
.. autofunction:: cmos_noise_map.utils.read_write_utils.read_bias_frames
```

<br><br>

```{eval-rst}
.. autofunction:: cmos_noise_map.utils.read_write_utils.write_file
```

<br><br>

```{eval-rst}
.. autofunction:: cmos_noise_map.utils.read_write_utils.read_parameter_table
```

<br>

### Data utility functions

<br>

```{eval-rst}
.. autofunction:: cmos_noise_map.utils.data_utils.data_to_pixel
```

<br><br>

```{eval-rst}
.. autofunction:: cmos_noise_map.utils.data_utils.qc_input
```

<br>

## The Code Playground

<br>

```{eval-rst}
.. autofunction:: cmos_noise_map.utils.get_rts_playground.plot_get_rts
```

<br><br>

```{eval-rst}
.. autofunction:: cmos_noise_map.utils.get_rts_playground.noise_distribution
```