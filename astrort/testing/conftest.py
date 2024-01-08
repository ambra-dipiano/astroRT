# *****************************************************************************
# Copyright (C) 2023 Ambra Di Piano
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import pytest
import astrort
from os.path import join, dirname, abspath
from os import makedirs

@pytest.fixture(scope='function')
def test_conf_file():
    return join(dirname(abspath(astrort.__file__)), 'configure', 'test.yml')

@pytest.fixture(scope='function')
def test_tmp_folder():
    makedirs(join(dirname(abspath(astrort.__file__)), 'testing', 'tmp'), exist_ok=True)
    return join(dirname(abspath(astrort.__file__)), 'testing', 'tmp')

@pytest.fixture(scope='function')
def test_data_folder():
    return join(dirname(abspath(astrort.__file__)), 'testing', 'data')