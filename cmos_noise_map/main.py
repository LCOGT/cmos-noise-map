# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 11:07:17 2023

@author: prera
"""

from cmos_noise_map.utils.read_write_utils import read_bias_frames, write_hdu
from cmos_noise_map.algorithms import STDMapMaker, RTSMapMaker, RTSParameterMapMaker
import click


@click.command()
@click.argument("path", required=True, type=click.Path(exists=True))
@click.argument("filename", required=True, type=click.Path(exists=False))
@click.argument("method", nargs=1, default="std")
@click.pass_context
@click.option(
    "--data_ext",
    "-r",
    default=0,
    help="Extension of fits file that contains the image data",
)
@click.option(
    "--upper_quantile",
    "-uq",
    default=None,
    type=float,
    help="Standard deviation cutoff for pixel noise evaluation",
)
@click.option(
    "--tolerance",
    "-t",
    type=float,
    help="The minimum difference between silhouette scores. See docs for more information.",
)
@click.option(
    "--min_peak_separation",
    "-m",
    type=float,
    help="Minimum difference between pixel value cluster centers to be considered separate clusters",
)
def cli(ctx: click.core.Context, **kwargs):
    """
    This script builds a noise map with the chosen method.

    path: Path to input without the .fits at the end

    filename: Path to write file, including the filename ending in .fits

    method: Default method is std. Available methods are std, rts, and param. See docs for more information about each method.
    """
    args_dict = ctx.params

    path = args_dict["path"]
    data_ext = args_dict["data_ext"]
    method = args_dict["method"]
    upper_quantile = args_dict["upper_quantile"]
    tolerance = args_dict["tolerance"]
    min_peak_separation = args_dict["min_peak_separation"]

    images = read_bias_frames(path, data_ext)
    methods = {"std": STDMapMaker, "rts": RTSMapMaker, "param": RTSParameterMapMaker}

    map_maker_class = methods.get(method)
    map_maker_object = map_maker_class(
        images, upper_quantile, tolerance, min_peak_separation
    )
    readnoise_map = map_maker_object.create_map()

    filename = args_dict["filename"]
    write_hdu(readnoise_map, filename)


if __name__ == "__main__":
    cli()
