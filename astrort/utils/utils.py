# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import random
from os import listdir
from os.path import join, expandvars

def seeds_to_string_formatter_files(samples, output, name, seed, ext):
    if samples <= 1e3:
        name = join(output, f"{name}_{seed:03d}.{ext}")
    elif samples <= 1e5:
        name = join(output, f"{name}_{seed:05d}.{ext}")
    elif samples <= 1e8:
        name = join(output, f"{name}_{seed:08d}.{ext}")
    else:
        name = join(output, f"{name}_{seed}.{ext}")
    return name

def seeds_to_string_formatter(samples, name, seed):
    if samples <= 1e3:
        name = join(f"{name}_{seed:03d}")
    elif samples <= 1e5:
        name = join(f"{name}_{seed:05d}")
    elif samples <= 1e8:
        name = join(f"{name}_{seed:08d}")
    else:
        name = join(f"{name}_{seed}")
    return name

def get_instrument_fov(instrument):
    if instrument == 'lst':
        fov = 2.5
    elif instrument == 'mst':
        fov = 3.5
    elif instrument == 'sst':
        fov = 5
    else:
        fov = 5 
    return fov

def get_instrument_tev_range(array):
    if array == 'lst':
        erange = [0.03, 5]
    elif array == 'mst':
        erange = [1, 50]
    elif array == 'sst':
        erange = [5, 150]
    else:
        erange = [0.03, 150]
    return erange

def adjust_tev_range_to_irf(erange, irf):
    # minimum energy
    if "z60" in irf and erange[0] < 0.11:
        erange[0] = 0.11
    elif "z40" in irf and erange[0] < 0.04:
        erange[0] = 0.04
    elif "z20" in irf and erange[0] < 0.03:
        erange[0] = 0.03
    return erange

def select_random_irf(array, prod):
    path = join(expandvars('$CALDB'), f'data/cta/{prod}/bcf')
    irfs = listdir(path)
    irf = random.choice([i for i in irfs if array in i.lower()])
    return irf