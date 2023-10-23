# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import pytest
import numpy as np
from os.path import isdir
from astrort.utils.utils import *
from astrort.utils.wrap import *

@pytest.mark.test_tmp_folder
@pytest.mark.parametrize('samples', [3, 5, 8, 10])
def test_seeds_to_string_formatter_files(samples, test_tmp_folder):
    name = seeds_to_string_formatter_files(samples, test_tmp_folder, name='test', seed=1, ext='fits')

    if samples <= 1e3:
        assert name == f"{test_tmp_folder}/test_001.fits"
    elif samples <= 1e5:
        assert name == f"{test_tmp_folder}/test_00001.fits"
    elif samples <= 1e8:
        assert name == f"{test_tmp_folder}/test_00000001.fits"
    else:
        assert name == f"{test_tmp_folder}/test_1.fits"

@pytest.mark.parametrize('samples', [3, 5, 8, 10])
def test_seeds_to_string_formatter(samples):
    name = seeds_to_string_formatter(samples, name='test', seed=1)

    if samples <= 1e3:
        assert name == f"test_001"
    elif samples <= 1e5:
        assert name == f"test_00001"
    elif samples <= 1e8:
        assert name == f"test_00000001"
    else:
        assert name == f"test_1"

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

@pytest.mark.parametrize('zenith', ['irf_z60', 'irf_z40', 'irf_z20'])
def test_adjust_tev_range_to_irf(zenith):
    erange = adjust_tev_range_to_irf([0.03, 150], zenith)
    
    if 'z60' in zenith:
        assert erange[0] == 0.11
    elif 'z60' in zenith:
        assert erange[0] == 0.04
    elif 'z20' in zenith:
        assert erange[0] == 0.03

@pytest.mark.parametrize('array', ['lst', 'mst', 'sst', 'north', 'south'])
def test_select_irf(array):
    prod = 'prod5-v0.1'
    path = join(expandvars('$CALDB'), f'data/cta/{prod}/bcf')
    irf = select_random_irf(array, prod)

    assert array in irf.lower()
    assert 'share/caldb/data/cta' in join(path, irf).lower()
    assert isdir(join(path, irf)) is True

@pytest.mark.test_conf_file
def test_get_all_seeds(test_conf_file):
    conf = load_yaml_conf(test_conf_file)
    seeds = get_all_seeds(conf['simulator'])
    assert seeds.all() == np.array([1, 2]).all()

def test_map_template():
    assert map_template() == join(dirname(abspath(__file__)).replace('testing/test_utils', 'templates'), 'base_empty_map.fits')