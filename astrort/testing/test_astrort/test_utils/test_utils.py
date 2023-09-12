# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import pytest
from astrort.utils.utils import *

@pytest.mark.astrort_tmp_folder
@pytest.mark.parametrize('samples', [3, 5, 8, 10])
def test_seeds_to_string_formatter(samples, astrort_tmp_folder):
    name = seeds_to_string_formatter(samples, astrort_tmp_folder, name='test', seed=1)

    if samples <= 3:
        assert name == f"{astrort_tmp_folder}/test_001"
    elif samples <= 5:
        assert name == f"{astrort_tmp_folder}/test_00001"
    elif samples <= 8:
        assert name == f"{astrort_tmp_folder}/test_00000001"
    else:
        assert name == f"{astrort_tmp_folder}/test_1"

@pytest.mark.parametrize('array', ['lst', 'mst', 'sst', 'cta', 'north', 'south'])
def test_get_instrument_fov(array):
    fov = get_instrument_fov(array)

    if array == 'lst':
        assert fov == 2.5
    elif array == 'mst':
        assert fov == 3.5
    elif array == 'sst':
        assert fov == 5
    else:
        assert fov == 5 
    return fov

@pytest.mark.parametrize('array', ['lst', 'mst', 'sst', 'cta', 'north', 'south'])
def test_get_instrument_tev_range(array):
    erange = get_instrument_tev_range(array)
    if array == 'lst':
        assert erange == [0.03, 5]
    elif array == 'mst':
        assert erange == [1, 50]
    elif array == 'sst':
        assert erange == [5, 150]
    else:
        assert erange == [0.03, 150]
    return erange