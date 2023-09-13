# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

from os.path import join

def seeds_to_string_formatter(samples, output, name, seed):
    if samples <= 1e3:
        name = join(output, f"{name}_{seed:03d}.fits")
    elif samples <= 1e5:
        name = join(output, f"{name}_{seed:05d}.fits")
    elif samples <= 1e8:
        name = join(output, f"{name}_{seed:08d}.fits")
    else:
        name = join(output, f"{name}_{seed}.fits")
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
