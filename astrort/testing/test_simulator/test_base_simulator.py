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
from astrort.utils.wrap import load_yaml_conf

@pytest.mark.test_conf_file
def test_base_simulator(test_conf_file):

    # clean output
    conf = load_yaml_conf(test_conf_file)
    rmtree(conf['simulator']['output'], ignore_errors=True)

    # run simulator
    base_simulator(test_conf_file)

    # check output
    expected_simulations = conf['simulator']['samples']
    found_simulations = len([f for f in listdir(conf['simulator']['output']) if isfile(join(conf['simulator']['output'], f)) and '.fits' in f and conf['simulator']['name'] in f])
    assert found_simulations == expected_simulations, f"Expected {expected_simulations} simulations, found {found_simulations}"


    
