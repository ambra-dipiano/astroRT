# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import pytest
from astrort.utils.wrap import load_yaml_conf
from astrort.cfg.check_configuration import CheckConfiguration

@pytest.mark.rtadeep_configuration
class TestBaseSimulator:

    def test_base_simulator(self, rtadeep_configuration):

        # get configuration
        configuration = load_yaml_conf(rtadeep_configuration)
        CheckConfiguration(configuration=configuration).check()

        
