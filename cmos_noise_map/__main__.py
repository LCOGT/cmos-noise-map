# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 11:07:17 2023

@author: prera
"""

from cmos_noise_map.read_write_fns import write_hdu
from cmos_noise_map.methods import do_rts, do_std, do_rts_params
from cmos_noise_map.utils.misc_fns import qc_input
import click

@click.command()
@click.argument("path", nargs=1, required=True, type=click.Path(exists=True))
@click.argument("filename", nargs=1, required=True, type=click.Path(exists=True))
@click.argument("method", nargs=1, default="std")
@click.option(
    '--data_ext',
    'r',
    default=0,
    help='Extension of fits file that contains the image data'
    )
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

def cli(path: str, filename: str, data_ext, method: str = "std", *args):
    """
    This script builds a noise map with the chosen method.
    
    path: Path to input requires the *.fits at the end
    
    filename: Path to write file, including the filename ending in .fits
    
    method: Default method is std. Available methods are std, rts, and param. See docs for more information about each method.
    """
    qc_input(path, data_ext)
    if method == "std":
        readnoise_map = do_std(path, data_ext, *args)
    elif method == "rts":
        readnoise_map = do_rts(path, data_ext, *args)
    elif method == "param":
        readnoise_map = do_rts_params(path, data_ext, *args)
    else:
        print("Please select a valid method from std, rts, or param")
    write_hdu(readnoise_map, filename)


if __name__ == "__main__":
    cli()
