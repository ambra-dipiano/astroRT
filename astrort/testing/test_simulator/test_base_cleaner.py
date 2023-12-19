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
from astrort.simulator.base_cleaner import base_cleaner
from astrort.utils.wrap import load_yaml_conf

@pytest.mark.test_conf_file
@pytest.mark.test_data_folder
def test_base_cleaner(test_conf_file, test_data_folder):

    # clean output
    conf = load_yaml_conf(test_conf_file)
    conf['mapper']['save'] = 'fits'
    conf['mapper']['replicate'] = join(test_data_folder, 'test_simulator.dat')
    rmtree(conf['mapper']['output'], ignore_errors=True)

    # run simulator
    base_simulator(test_conf_file)

    # write new mapper configuration
    update_conf_file = join(conf['mapper']['output'], 'tmp.yml')
    with open(update_conf_file, 'w+') as f:
        dump(conf, f, default_flow_style=False)
    base_cleaner(update_conf_file)

    # check output
    expected_maps = conf['simulator']['samples']
    # noisy map
    found_maps = len([f for f in listdir(join(conf['mapper']['output'], 'noisy')) if isfile(join(conf['mapper']['output'], 'noisy', f)) and conf['mapper']['save'] in f and conf['simulator']['name'] in f and 'map' in f])
    assert found_maps == expected_maps, f"Expected {expected_maps} maps, found {found_maps}"
    # clean map
    found_maps = len([f for f in listdir(join(conf['mapper']['output'], 'clean')) if isfile(join(conf['mapper']['output'], 'clean', f)) and conf['mapper']['save'] in f and conf['simulator']['name'] in f and 'map' in f])
    assert found_maps == expected_maps, f"Expected {expected_maps} maps, found {found_maps}"

