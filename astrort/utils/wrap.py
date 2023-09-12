# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import yaml
from astrort.utils.utils import seeds_to_string_formatter, get_instrument_fov
from astrort.configure.check_configuration import CheckConfiguration

def load_yaml_conf(yamlfile):
    with open(yamlfile) as f:
        configuration = yaml.load(f, Loader=yaml.FullLoader)
        CheckConfiguration(configuration=configuration)
    return configuration

def configure_simulator(simulator, configuration):
    simulator.model = configuration['model']
    simulator.output = seeds_to_string_formatter(configuration['samples'], configuration['output'], configuration['name'], configuration['seed'])
    simulator.caldb = configuration['prod']
    simulator.irf = configuration['irf']
    simulator.fov = get_instrument_fov(configuration['array'])
