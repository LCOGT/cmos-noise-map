# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 11:07:17 2023

@author: Prerana Kottapalli
"""

import click

from cmos_noise_map.utils.read_write_utils import read_write_utils
from cmos_noise_map.map_maker import STDMapMaker, RTSMapMaker, RTSParameterMapMaker


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
    default=0.05,
    type=float,
    help="The minimum difference between silhouette scores. See docs for more information.",
)
@click.option(
    "--min_peak_separation",
    "-m",
    default=10,
    type=float,
    help="Minimum difference between pixel value cluster centers to be considered separate clusters",
)
@click.option(
    "--out_hdu_name",
    "-o",
    default="PRIMARY",
    type=str,
    help="Name for the header in which the data will be stored",
)
@click.option(
    "--fpack",
    "-f",
    default=True,
    help="Adding this option will fpack your output fits file",
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
    filename = args_dict["filename"]
    hdu_name = args_dict["out_hdu_name"]
    fpack = args_dict["fpack"]
    
    read_write = read_write_utils(path=path, filename=filename, data_ext=data_ext, hduname=hdu_name, fpack=fpack)
    images = read_write.read_bias_frames()
    methods = {"std": STDMapMaker, "rts": RTSMapMaker, "param": RTSParameterMapMaker}

    map_maker_class = methods.get(method)
    map_maker_object = map_maker_class(
        images, tolerance, upper_quantile, min_peak_separation
    )
    readnoise_map = map_maker_object.create_map()

    data_types = {"std": "image", "rts": "image", "param": "table"}
    
    if fpack is True:
        read_write.write_file(readnoise_map, fpack, data_types[method])
    else:
        read_write.write_file(readnoise_map, fpack, data_types[method])


if __name__ == "__main__":
    cli()
