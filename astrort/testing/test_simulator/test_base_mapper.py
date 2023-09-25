# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import pytest
from shutil import rmtree
from os import listdir
from os.path import isfile, join
from astrort.simulator.base_simulator import base_simulator
from astrort.simulator.base_mapper import base_mapper
from astrort.utils.wrap import load_yaml_conf

@pytest.mark.skip('#TODO')
@pytest.mark.test_conf_file
@pytest.mark.parametrize('seeds', [None, list([1,2])])
def test_base_mapper(test_conf_file, seeds):

    # clean output
    conf = load_yaml_conf(test_conf_file)
    rmtree(conf['mapper']['output'])

    # run simulator
    base_simulator(test_conf_file)
    base_mapper(test_conf_file, seeds)

    # check output
    expected_maps = conf['simulator']['samples']
    found_maps = len([f for f in listdir(conf['mapper']['output']) if isfile(join(conf['mapper']['output'], f)) and '.fits' in f and conf['mapper']['name'] in f])
    assert found_maps == expected_maps, f"Expected {expected_maps} maps, found {found_maps}"


    
