# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import pytest
from rtadeep.utils.wrap import load_yaml_conf
from rtadeep.cfg.check_configuration import CheckConfiguration

@pytest.mark.rtadeep_configuration
class TestCheckConfiguration:

    def test_check(self, rtadeep_configuration):
        configuration = load_yaml_conf(rtadeep_configuration)
        try:
            CheckConfiguration(configuration=configuration).check()
        except AssertionError as e:
            type(e) == AssertionError

    def test_check_tags(self, rtadeep_configuration):
        configuration = load_yaml_conf(rtadeep_configuration)
        try:
            CheckConfiguration(configuration=configuration).check_tags()
        except AssertionError as e:
            type(e) == AssertionError

    def test_check_simulator(self, rtadeep_configuration):
        configuration = load_yaml_conf(rtadeep_configuration)
        try:
            CheckConfiguration(configuration=configuration).check_simulator()
        except AssertionError as e:
            type(e) == AssertionError

    def test_check_visibility(self, rtadeep_configuration):
        configuration = load_yaml_conf(rtadeep_configuration)
        try:
            CheckConfiguration(configuration=configuration).check_visibility()
        except AssertionError as e:
            type(e) == AssertionError
