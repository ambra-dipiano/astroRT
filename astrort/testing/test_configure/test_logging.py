# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import pytest
import logging
from os.path import join, isfile
from astrort.configure.logging import get_log_level, set_logger

def test_set_logger():
    assert get_log_level('DEBUG') == logging.DEBUG
    assert get_log_level('INFO') == logging.INFO    
    assert get_log_level('WARNING') == logging.WARNING
    assert get_log_level('ERROR') == logging.ERROR
    assert get_log_level('CRITICAL') == logging.CRITICAL

@pytest.mark.test_tmp_folder
@pytest.mark.test_conf_file
def test_set_logger(test_tmp_folder):
    log = set_logger(logging.DEBUG, join(test_tmp_folder, 'test_set_logger.log'))
    log.debug('TEST')
    assert isfile(join(test_tmp_folder, 'test_set_logger.log')) is True
