# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

class CheckConfiguration():

    def __init__(self, configuration):
        assert type(configuration) == dict, f'configuration type {type(configuration)} invalid, a python dictionary is required'
        self.conf = configuration
        pass

    def check(self):
        self.check_tags()
        self.check_simulator()
        self.check_visibility()

    def check_tags(self):
        tags = ['simulator', 'visibility']
        assert self.conf.keys() == tags

    def check_simulator(self):
        keys = ['name', 'irf', 'prod', 'coordinates', 'duration', 'samples', 'seed']
        assert self.conf['simulator'].keys() == keys

    def check_visibility(self):
        keys = ['start_time']
        assert self.conf['visibility'].keys() == keys
