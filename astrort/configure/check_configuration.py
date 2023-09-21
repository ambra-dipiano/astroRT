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
        return self

    def check_tags(self):
        tags = ['simulator', 'visibility', 'logging']
        assert self.conf.keys() == tags
        return self

    def check_simulator(self):
        keys = ['name', 'array', 'irf', 'prod', 'pointing', 'duration', 'samples', 'seed', 'model']
        assert self.conf['simulator'].keys() == keys
        assert type(self.conf['simulator']['name']) == str
        assert type(self.conf['simulator']['array']) in ['lst', 'mst', 'sst', 'cta', 'north', 'south']
        assert type(self.conf['simulator']['irf']) == str
        assert type(self.conf['simulator']['prod']) == str
        assert (type(self.conf['simulator']['pointing']) == str or type(self.conf['simulator']['pointing']) == dict)
        assert type(self.conf['simulator']['duration']) == int
        assert type(self.conf['simulator']['samples']) == int
        assert type(self.conf['simulator']['seed']) == int
        assert type(self.conf['simulator']['model']) == str
        return self

    def check_visibility(self):
        keys = ['start_time']
        assert self.conf['visibility'].keys() == keys
        assert type(self.conf['visibility']['start_time']) == str
        return self

    def check_logging(self):
        keys = ['level', 'logfile', 'datfile']
        assert self.conf['logging'].keys() == keys
        assert (type(self.conf['logging']['level']) == str or type(self.conf['logging']['level']) == int) 
        assert type(self.conf['logging']['logfile']) == str 
        assert type(self.conf['logging']['datfile']) == str 
        return self
    
    def check_slurm(self):
        keys = ['nodes', 'tasks', 'cpus', 'mem', 'environment', 'name', 'account', 'partition']
        assert self.conf['slurm'].keys() == keys
        assert type(self.conf['slurm']['nodes']) == int
        assert type(self.conf['slurm']['tasks']) == int
        assert type(self.conf['slurm']['cpus']) == int
        assert type(self.conf['slurm']['mem']) == str 
        assert type(self.conf['slurm']['environment']) == str 
        assert type(self.conf['slurm']['name']) == str 
        assert type(self.conf['slurm']['account']) == str 
        assert type(self.conf['slurm']['partition']) == str 
        return self