# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import pytest
import numpy as np
from astrort.utils.wrap import load_yaml_conf, randomise_pointing_sim, get_point_source_info

@pytest.mark.test_conf_file
def test_load_yaml_conf(test_conf_file):
    configuration = load_yaml_conf(test_conf_file)
    assert type(configuration) == dict

@pytest.mark.test_conf_file
def test_randomise_pointing_sim(test_conf_file):
    conf = load_yaml_conf(test_conf_file)
    pointing = randomise_pointing_sim(conf['simulator'])
    assert type(pointing) == dict
    for key in pointing.keys():
        assert key in ['point_ra', 'point_dec', 'offset', 'source_ra', 'source_dec']
    assert type(pointing['point_ra']) == type(np.float64(1))
    assert type(pointing['point_dec']) == type(np.float64(1))
    assert type(pointing['offset']) == type(np.float64(1))
    assert type(pointing['source_ra']) == type(np.float64(1))
    assert type(pointing['source_dec']) == type(np.float64(1))

@pytest.mark.test_conf_file
def test_get_point_source_info(test_conf_file):
    conf = load_yaml_conf(test_conf_file)
    conf['simulator']['pointing'] = {'ra': 1, 'dec': 1}
    pointing = get_point_source_info(conf['simulator'])
    assert type(pointing) == dict
    for key in pointing.keys():
        assert key in ['point_ra', 'point_dec', 'offset', 'source_ra', 'source_dec']
    assert type(pointing['point_ra']) == type(np.float64(1))
    assert type(pointing['point_dec']) == type(np.float64(1))
    assert type(pointing['offset']) == type(np.float64(1))
    assert type(pointing['source_ra']) == type(np.float64(1))
    assert type(pointing['source_dec']) == type(np.float64(1))