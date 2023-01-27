# cmos-noise-map

## The Basic Framework

## Code documentation

### Main wrapper function

<br>

```{eval-rst}
.. autofunction:: cmos_noise_map.main.cli
```

### Main functions to produce a read noise map

<br>

```{eval-rst}
.. autofunction:: cmos_noise_map.methods.do_rts
```
<br><br>

```{eval-rst}
.. autofunction:: cmos_noise_map.methods.do_std
```
<br><br>

```{eval-rst}
.. autofunction:: cmos_noise_map.methods.do_rts_params
```
<br>

### Base functions to calculate the read noise from standard deviation

<br>

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
.. autofunction:: cmos_noise_map.read_write_fns.read_bias_frames
```

<br><br>

```{eval-rst}
.. autofunction:: cmos_noise_map.read_write_fns.write_hdu
```

<br>

### Miscellaneous utility functions

<br>

```{eval-rst}
.. autofunction:: cmos_noise_map.utils.misc_fns.data_to_pixel
```

<br><br>

```{eval-rst}
.. autofunction:: cmos_noise_map.utils.misc_fns.qc_input
```