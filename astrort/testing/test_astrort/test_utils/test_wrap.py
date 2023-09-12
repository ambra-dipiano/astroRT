# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import pytest
from astrort.utils.wrap import load_yaml_conf

@pytest.mark.astrort_configuration
def test_load_yaml_conf(astrort_configuration):
    configuration = load_yaml_conf(astrort_configuration)
    assert type(configuration) == dict