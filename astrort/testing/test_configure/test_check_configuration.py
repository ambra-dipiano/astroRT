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

@pytest.mark.test_conf_file
class TestCheckConfiguration:

    def test_check(self, test_conf_file):
        configuration = load_yaml_conf(test_conf_file)
        try:
            CheckConfiguration(configuration=configuration).check()
        except AssertionError as e:
            type(e) == AssertionError

    def test_check_tags(self, test_conf_file):
        configuration = load_yaml_conf(test_conf_file)
        try:
            CheckConfiguration(configuration=configuration).check_tags()
        except AssertionError as e:
            type(e) == AssertionError

    def test_check_simulator(self, test_conf_file):
        configuration = load_yaml_conf(test_conf_file)
        try:
            CheckConfiguration(configuration=configuration).check_simulator()
        except AssertionError as e:
            type(e) == AssertionError

    def test_check_visibility(self, test_conf_file):
        configuration = load_yaml_conf(test_conf_file)
        try:
            CheckConfiguration(configuration=configuration).check_visibility()
        except AssertionError as e:
            type(e) == AssertionError

    def test_check_logging(self, test_conf_file):
        configuration = load_yaml_conf(test_conf_file)
        try:
            CheckConfiguration(configuration=configuration).check_logging()
        except AssertionError as e:
            type(e) == AssertionError

    def test_check_slurm(self, test_conf_file):
        configuration = load_yaml_conf(test_conf_file)
        try:
            CheckConfiguration(configuration=configuration).check_logging()
        except AssertionError as e:
            type(e) == AssertionError

    def test_check_mapper(self, test_conf_file):
        configuration = load_yaml_conf(test_conf_file)
        try:
            CheckConfiguration(configuration=configuration).check_mapper()
        except AssertionError as e:
            type(e) == AssertionError