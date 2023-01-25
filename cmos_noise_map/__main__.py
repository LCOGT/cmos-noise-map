# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 11:07:17 2023

@author: prera
"""

from read_write_fns import write_hdu
from methods import do_rts, do_std, do_rts_params

# Need at least 50 images


path = "/run/media/pkottapalli/Untitled/411_mod3_gain30_bin1_telegraph/*.fits"
readnoise_map = do_std(path)
write_hdu(readnoise_map)
