# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import pytest
import logging
import numpy as np
from astrort.utils.wrap import *
from astrort.configure.logging import set_logger
from rtasci.lib.RTACtoolsSimulation import RTACtoolsSimulation

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

@pytest.mark.test_conf_file
def test_write_simulation_info(test_conf_file):
    conf = load_yaml_conf(test_conf_file)
    conf['simulator']['pointing'] = {'ra': 1, 'dec': 1}
    pointing = get_point_source_info(conf['simulator'])
    datfile = join(conf['simulator']['output'], 'simulator.dat')
    sim = RTACtoolsSimulation()
    clock = 1
    write_simulation_info(sim, conf['simulator'], pointing, datfile, clock)
    assert isfile(datfile)
    del sim

@pytest.mark.test_tmp_folder
@pytest.mark.test_conf_file
def test_merge_simulation_info(test_conf_file, test_tmp_folder):
    conf = load_yaml_conf(test_conf_file)
    conf['simulator']['pointing'] = {'ra': 1, 'dec': 1}
    pointing = get_point_source_info(conf['simulator'])
    sim = RTACtoolsSimulation()
    clock = 1
    for i in range(5):
        sim.seed = i
        datfile = join(conf['simulator']['output'], f'job_{i}_simulator.dat')
        write_simulation_info(sim, conf['simulator'], pointing, datfile, clock)
        assert isfile(datfile)
    
    log = set_logger(logging.CRITICAL, join(test_tmp_folder, 'test_set_logger.log'))
    merge_simulation_info(conf['simulator'], log)
    assert isfile(join(conf['simulator']['output'], 'merged_sim_data.dat'))
    del sim

def test_write_mapping_info():
    return


    