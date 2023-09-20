# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import pytest
import numpy as np
from astrort.utils.wrap import load_yaml_conf, randomise_pointing

@pytest.mark.test_conf_file
def test_load_yaml_conf(test_conf_file):
    configuration = load_yaml_conf(test_conf_file)
    assert type(configuration) == dict

@pytest.mark.test_conf_file
def test_randomise_pointing(test_conf_file):
    conf = load_yaml_conf(test_conf_file)
    pointing = randomise_pointing(conf['simulator'])
    assert type(pointing) == dict
    for key in pointing.keys():
        assert key in ['ra', 'dec', 'offset']
    assert type(pointing['ra']) == type(np.float64(1))
    assert type(pointing['dec']) == type(np.float64(1))
    assert type(pointing['offset']) == type(np.float64(1))