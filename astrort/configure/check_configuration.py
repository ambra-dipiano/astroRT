# *****************************************************************************
# Copyright (C) 2023 Ambra Di Piano
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
        assert set(self.conf.keys()) == set(tags), f"Expected keys {tags}, got {list(self.conf.keys())}"
        return self

    def check_simulator(self):
        keys = ['name', 'array', 'irf', 'prod', 'pointing', 'target', 'maxoffset', 'duration', 'samples', 'seed', 'model', 'output', 'replicate']
        assert set(self.conf['simulator'].keys()) == set(keys), f"Expected keys {keys}, got {list(self.conf['simulator'].keys())}"
        assert isinstance(self.conf['simulator']['name'], str)
        assert self.conf['simulator']['array'] in ['lst', 'mst', 'sst', 'cta', 'north', 'south']
        assert isinstance(self.conf['simulator']['irf'], str)
        assert isinstance(self.conf['simulator']['prod'], str)
        assert isinstance(self.conf['simulator']['pointing'], (str, dict))
        assert self.conf['simulator']['target'] is None or isinstance(self.conf['simulator']['target'], str)
        assert isinstance(self.conf['simulator']['maxoffset'], (int, float))
        assert isinstance(self.conf['simulator']['duration'], int)
        assert isinstance(self.conf['simulator']['samples'], int)
        assert isinstance(self.conf['simulator']['seed'], int)
        assert isinstance(self.conf['simulator']['model'], str)
        assert isinstance(self.conf['simulator']['output'], str)
        assert self.conf['simulator']['replicate'] is None or isinstance(self.conf['simulator']['replicate'], str)
        return self

    def check_visibility(self):
        keys = ['start_time']
        assert set(self.conf['visibility'].keys()) == set(keys), f"Expected keys {keys}, got {list(self.conf['visibility'].keys())}"
        assert isinstance(self.conf['visibility']['start_time'], str)
        return self

    def check_logging(self):
        keys = ['level', 'logfile', 'datfile']
        assert set(self.conf['logging'].keys()) == set(keys), f"Expected keys {keys}, got {list(self.conf['logging'].keys())}"
        assert isinstance(self.conf['logging']['level'], (str, int))
        assert isinstance(self.conf['logging']['logfile'], str)
        assert isinstance(self.conf['logging']['datfile'], str)
        return self
    
    def check_slurm(self):
        keys = ['nodes', 'tasks', 'cpus', 'mem', 'environment', 'name', 'account', 'partition']
        assert set(self.conf['slurm'].keys()) == set(keys), f"Expected keys {keys}, got {list(self.conf['slurm'].keys())}"
        assert isinstance(self.conf['slurm']['nodes'], int)
        assert isinstance(self.conf['slurm']['tasks'], int)
        assert isinstance(self.conf['slurm']['cpus'], int)
        assert isinstance(self.conf['slurm']['mem'], str)
        assert isinstance(self.conf['slurm']['environment'], str)
        assert isinstance(self.conf['slurm']['name'], str)
        assert isinstance(self.conf['slurm']['account'], str)
        assert isinstance(self.conf['slurm']['partition'], str)
        return self
    
    def check_mapper(self):
        keys = ['exposure', 'smooth', 'pixelsize', 'center', 'plot', 'region', 'output', 'replicate', 'save']
        assert set(self.conf['mapper'].keys()) == set(keys), f"Expected keys {keys}, got {list(self.conf['mapper'].keys())}"
        assert isinstance(self.conf['mapper']['exposure'], int)
        assert isinstance(self.conf['mapper']['smooth'], (float, int))
        assert isinstance(self.conf['mapper']['pixelsize'], (float, int))
        assert self.conf['mapper']['center'] in ['pointing', 'source']
        assert isinstance(self.conf['mapper']['plot'], bool)
        assert isinstance(self.conf['mapper']['region'], bool)
        assert isinstance(self.conf['mapper']['output'], str)
        assert self.conf['mapper']['replicate'] is None or isinstance(self.conf['mapper']['replicate'], str)
        assert isinstance(self.conf['mapper']['save'], str)
        return self