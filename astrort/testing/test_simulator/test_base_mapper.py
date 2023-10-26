# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import pytest
import numpy as np
from yaml import dump
from shutil import rmtree
from os import listdir
from os.path import isfile, join
from astrort.simulator.base_simulator import base_simulator
from astrort.simulator.base_mapper import base_mapper
from astrort.utils.wrap import load_yaml_conf

@pytest.mark.test_conf_file
@pytest.mark.parametrize('seeds', [None, list()])
@pytest.mark.parametrize('save', ['fits', 'npy'])
def test_base_mapper(test_conf_file, seeds, save):

    # clean output
    conf = load_yaml_conf(test_conf_file)
    conf['mapper']['save'] = save
    rmtree(conf['mapper']['output'], ignore_errors=True)

    # run simulator
    base_simulator(test_conf_file)
    if type(seeds) == list:
        seeds = np.arange(conf['simulator']['samples'])

    # write new mapper configuration
    update_conf_file = join(conf['mapper']['output'], 'tmp.yml')
    with open(update_conf_file, 'w+') as f:
        dump(conf, f, default_flow_style=False)
    base_mapper(update_conf_file, seeds)

    # check output
    expected_maps = conf['simulator']['samples']
    found_maps = len([f for f in listdir(conf['mapper']['output']) if isfile(join(conf['mapper']['output'], f)) and conf['mapper']['save'] in f and conf['simulator']['name'] in f and 'map' in f])
    assert found_maps == expected_maps, f"Expected {expected_maps} maps, found {found_maps}"


