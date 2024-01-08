# *****************************************************************************
# Copyright (C) 2023 Ambra Di Piano
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import pytest
import logging
from os.path import join, isfile
from astrort.configure.logging import *
from astrort.utils.wrap import load_yaml_conf

def test_set_logger():
    assert get_log_level('DEBUG') == logging.DEBUG
    assert get_log_level('INFO') == logging.INFO    
    assert get_log_level('WARNING') == logging.WARNING
    assert get_log_level('ERROR') == logging.ERROR
    assert get_log_level('CRITICAL') == logging.CRITICAL

@pytest.mark.test_tmp_folder
def test_set_logger(test_tmp_folder):
    log = set_logger(logging.CRITICAL, join(test_tmp_folder, 'test_set_logger.log'))
    log.debug('TEST')
    assert isfile(join(test_tmp_folder, 'test_set_logger.log')) is True

@pytest.mark.test_conf_file
@pytest.mark.parametrize('mode', ['simulator', 'mapper'])
def test_get_logfile(test_conf_file, mode):
    conf = load_yaml_conf(test_conf_file)

    logfile = get_logfile(conf, mode)
    assert mode in logfile


