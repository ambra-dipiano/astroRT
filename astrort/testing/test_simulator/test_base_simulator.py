# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import pytest
import yaml
import pandas as pd
import numpy as np
from shutil import rmtree
from os import listdir, makedirs
from os.path import isfile, join
from astrort.simulator.base_simulator import base_simulator
from astrort.utils.wrap import load_yaml_conf

@pytest.mark.test_conf_file
@pytest.mark.test_data_folder
@pytest.mark.test_tmp_folder
@pytest.mark.parametrize('replicate', [None, 'test_simulator.dat'])
def test_base_simulator(test_conf_file, replicate, test_data_folder, test_tmp_folder):

    # clean output
    conf = load_yaml_conf(test_conf_file)
    conf['simulator']['replicate'] = join(test_data_folder, replicate) if replicate is not None else replicate
    rmtree(conf['simulator']['output'], ignore_errors=True)

    # create tmp
    makedirs(test_tmp_folder, exist_ok=True)
    tmp_conf_file = join(test_tmp_folder, 'test.yml')
    with open(tmp_conf_file, 'w+') as f:
        yaml.dump(conf, f)

    # run simulator
    base_simulator(tmp_conf_file)

    # check output
    expected_simulations = conf['simulator']['samples']
    found_simulations = len([f for f in listdir(conf['simulator']['output']) if isfile(join(conf['simulator']['output'], f)) and '.fits' in f and conf['simulator']['name'] in f])
    assert found_simulations == expected_simulations, f"Expected {expected_simulations} simulations, found {found_simulations}"

    if replicate is not None:
        data_new = pd.read_csv(join(test_tmp_folder, replicate), sep=' ', header=0)
        data_old = pd.read_csv(join(test_data_folder, replicate), sep=' ', header=0)
        for i in range(conf['simulator']['samples']):
            assert data_new['irf'][i] == data_old['irf'][i]
            assert np.round(data_new['point_ra'][i], decimals=3) == np.round(data_old['point_ra'][i], decimals=3)
            assert np.round(data_new['point_dec'][i], decimals=3) == np.round(data_old['point_dec'][i], decimals=3)



    
