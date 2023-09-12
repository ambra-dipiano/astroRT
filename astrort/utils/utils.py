# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

from os.path import join

def seeds_to_string_formatter(samples, output, name, seed):
    if samples <= 3:
        name = join(output, f"{name}_{seed:03d}")
    elif samples <= 5:
        name = join(output, f"{name}_{seed:05d}")
    elif samples <= 8:
        name = join(output, f"{name}_{seed:08d}")
    else:
        name = join(output, f"{name}_{seed}")
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