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
        keys = ['name', 'array', 'irf', 'prod', 'pointing', 'target', 'maxoffset', 'duration', 'samples', 'seed', 'model', 'output', 'replicate']
        assert self.conf['simulator'].keys() == keys
        assert type(self.conf['simulator']['name']) == str
        assert type(self.conf['simulator']['array']) in ['lst', 'mst', 'sst', 'cta', 'north', 'south']
        assert type(self.conf['simulator']['irf']) == str
        assert type(self.conf['simulator']['prod']) == str
        assert type(self.conf['simulator']['pointing']) == (str or dict)
        assert type(self.conf['simulator']['target']) == (str or None)
        assert type(self.conf['simulator']['maxoffset']) == (int or float)
        assert type(self.conf['simulator']['duration']) == int
        assert type(self.conf['simulator']['samples']) == int
        assert type(self.conf['simulator']['seed']) == int
        assert type(self.conf['simulator']['model']) == str
        assert type(self.conf['simulator']['output']) == str
        assert type(self.conf['simulator']['replicate']) == (str or None)
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
    
    def check_mapper(self):
        keys = ['exposure', 'smooth', 'pixelsize', 'center', 'plot', 'region', 'output', 'replicate', 'save']
        assert self.conf['mapper'].keys() == keys
        assert type(self.conf['mapper']['exposure']) == int
        assert type(self.conf['mapper']['smooth']) == (float or int)
        assert type(self.conf['mapper']['pixelsize']) == (float or int)
        assert type(self.conf['mapper']['center']) in ['pointing', 'source'] 
        assert type(self.conf['mapper']['plot']) == bool
        assert type(self.conf['mapper']['region']) == bool
        assert type(self.conf['mapper']['output']) == str
        assert type(self.conf['simulator']['replicate']) == (str or None)
        assert type(self.conf['simulator']['save']) == str
        return self