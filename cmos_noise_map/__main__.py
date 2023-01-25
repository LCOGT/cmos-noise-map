# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 11:07:17 2023

@author: prera
"""

from cmos_noise_map.read_write_fns import write_hdu
from cmos_noise_map.methods import do_rts, do_std, do_rts_params
import click

# Need at least 50 images


@click.command()
@click.argument("path", required=True)
@click.argument("filename", required=True)
@click.argument("method", default="std")
@click.option(
    "--upper_q",
    "-uq",
    default=None,
    type=float,
    help="Standard deviation cutoff for pixel noise evaluation",
)
@click.option(
    "--tol",
    "-t",
    type=float,
    help="The minimum difference between silhouette scores. See docs for more information.",
)
@click.option(
    "--min_peak_sep",
    "-m",
    type=float,
    help="Minimum difference between pixel value cluster centers to be considered separate clusters",
)

# path = "/run/media/pkottapalli/Untitled/411_mod3_gain30_bin1_telegraph/*.fits"
def cli(path: str, filename: str, method: str = "std", *args) -> None:
    """
    This script builds a noise map with the chosen method.
    
    path: path to input requires the *.fits at the end
    
    filename: path to write file, including the filename ending in .fits
    """
    if method == "std":
        readnoise_map = do_std(path, *args)
    elif method == "rts":
        readnoise_map = do_rts(path, *args)
    elif method == "param":
        readnoise_map = do_rts_params(path, *args)
    else:
        print("Please select a valid method from std, rts, or param")
    write_hdu(readnoise_map, filename)


if __name__ == "__main__":
    cli()
