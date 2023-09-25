# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import pytest
from shutil import rmtree
from os import listdir, makedirs
from os.path import isfile, join
from astrort.configure.slurmjobs import make_simulator_conf, make_sh, make_simulator_sbatch
from astrort.utils.wrap import load_yaml_conf

@pytest.mark.test_conf_file
def test_make_simulator_conf(test_conf_file):

    # clean output
    conf = load_yaml_conf(test_conf_file)
    rmtree(conf['simulator']['output'])
    makedirs(conf['simulator']['output'], exist_ok=True)

    # make configurations
    for node_number in range(conf['slurm']['nodes']):
        node_number += 1
        jobname = f"{conf['slurm']['name']}_{node_number}"       
        jobname_conf = join(conf['simulator']['output'], f"job_{jobname}.yml")
        make_simulator_conf(jobname_conf, conf, node_number)
    
    # check output
    expected_configurations = conf['slurm']['nodes']
    found_configurations = len([f for f in listdir(conf['simulator']['output']) if isfile(join(conf['simulator']['output'], f)) and '.yml' in f and conf['slurm']['name'] in f])
    assert found_configurations == expected_configurations, f"Expected {expected_configurations} simulations, found {found_configurations}"

@pytest.mark.test_conf_file
def test_make_sh(test_conf_file):

    # clean output
    conf = load_yaml_conf(test_conf_file)
    rmtree(conf['simulator']['output'])
    makedirs(conf['simulator']['output'], exist_ok=True)

    # make configurations
    output = conf['simulator']['output']
    for node_number in range(conf['slurm']['nodes']):
        node_number += 1
        jobname = f"{conf['slurm']['name']}_{node_number}"
        jobname_sh = join(output, f"job_{jobname}.sh")
        jobname_log = join(output, f"job_{jobname}.log")
        jobname_conf = join(output, f"job_{jobname}.yml")
        make_sh(jobname, conf['slurm'], jobname_conf, jobname_sh, jobname_log, mode='simulator')

    # check output
    expected_sh = conf['slurm']['nodes']
    found_sh = len([f for f in listdir(conf['simulator']['output']) if isfile(join(conf['simulator']['output'], f)) and '.sh' in f and conf['slurm']['name'] in f])
    assert found_sh == expected_sh, f"Expected {expected_sh} simulations, found {found_sh}"

