# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import pytest
from astrort.utils.wrap import load_yaml_conf
from astrort.configure.check_configuration import CheckConfiguration

@pytest.mark.skip('to-do')
@pytest.mark.rtadeep_configuration
class TestBaseSimulator:

    @pytest.mark.skip('to-do')
    def test_base_simulator(self, rtadeep_configuration):

        # get configuration
        configuration = load_yaml_conf(rtadeep_configuration)

        
