# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import pytest
import rtadeep
from os.path import join, dirname, abspath

@pytest.fixture(scope='function')
def rtadeep_configuration():
    return join(dirname(abspath(astrort.__file__)), 'cfg', 'test.yml')