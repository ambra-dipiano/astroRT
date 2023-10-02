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
from shutil import rmtree
from astrort.utils.wrap import *
from astrort.utils.utils import seeds_to_string_formatter_files
from astrort.configure.logging import set_logger
from astrort.simulator.base_simulator import base_simulator
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

@pytest.mark.test_conf_file
def test_write_mapping_info(test_conf_file):
    conf = load_yaml_conf(test_conf_file)
    conf['simulator']['pointing'] = {'ra': 1, 'dec': 1}
    datfile = join(conf['simulator']['output'], 'simulator.dat')
    clock = 1
    write_mapping_info(conf, datfile, clock)
    assert isfile(datfile)

@pytest.mark.test_conf_file
def test_configure_simulator_no_visibility(test_conf_file):
    conf = load_yaml_conf(test_conf_file)
    conf['simulator']['pointing'] = {'ra': 1, 'dec': 1}
    log = set_logger(logging.CRITICAL)
    sim = RTACtoolsSimulation()
    sim = configure_simulator_no_visibility(sim, conf['simulator'], log)
    
    assert sim.t == [0, conf['simulator']['duration']]
    assert sim.seed == conf['simulator']['seed']
    assert sim.set_log is False
    assert sim.caldb == conf['simulator']['prod']
    del sim

@pytest.mark.test_conf_file
def test_execute_mapper_no_visibility(test_conf_file):
    # clean output
    conf = load_yaml_conf(test_conf_file)
    rmtree(conf['mapper']['output'], ignore_errors=True)
    conf['simulator']['samples'] = 1
    log = set_logger(logging.CRITICAL)

    # run simulator
    base_simulator(test_conf_file)
    fitsmap = execute_mapper_no_visibility(conf, log)
    assert isfile(fitsmap)

@pytest.mark.test_conf_file
def test_plot_map(test_conf_file):
    # clean output
    conf = load_yaml_conf(test_conf_file)
    rmtree(conf['mapper']['output'], ignore_errors=True)
    conf['simulator']['samples'] = 1
    log = set_logger(logging.CRITICAL)

    # run simulator
    base_simulator(test_conf_file)
    fitsmap = execute_mapper_no_visibility(conf, log)
    plotmap = plot_map(fitsmap, log)
    assert isfile(plotmap)