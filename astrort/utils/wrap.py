# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import yaml
import numpy as np
import astropy.units as u
from os.path import dirname, abspath, join, basename
from astrort.utils.utils import seeds_to_string_formatter, get_instrument_fov
from astrort.configure.check_configuration import CheckConfiguration
from rtasci.lib.RTAManageXml import ManageXml
from astropy.coordinates import SkyCoord 

def load_yaml_conf(yamlfile):
    with open(yamlfile) as f:
        configuration = yaml.load(f, Loader=yaml.FullLoader)
        CheckConfiguration(configuration=configuration)
    return configuration

def configure_simulator_no_visibility(simulator, configuration):
    if '$TEMPLATES$' in configuration['model']:
        configuration['model'] = join(dirname(abspath(__file__)).replace('utils', 'templates'), basename(configuration['model']))
    simulator.model = configuration['model']
    simulator.output = seeds_to_string_formatter(configuration['samples'], configuration['output'], configuration['name'], configuration['seed'], 'fits')
    simulator.caldb = configuration['prod']
    simulator.irf = configuration['irf']
    simulator.fov = get_instrument_fov(configuration['array'])
    simulator.t = [0, configuration['duration']]
    simulator.seed = configuration['seed']
    return simulator

def randomise_pointing(simulator):
    if '$TEMPLATES$' in simulator['model']:
        simulator['model'] = join(dirname(abspath(__file__)).replace('utils', 'templates'), basename(simulator['model']))
    model_xml = ManageXml(xml=simulator['model'])
    name = model_xml.getName()
    source = model_xml.getRaDec()
    del model_xml
    # use astropy separation
    ra, dec = source[0][0] * u.deg, source[1][0] * u.deg
    source = SkyCoord(ra, dec, frame='icrs')
    position_angle = 45 * u.deg
    separation = np.random.random() * get_instrument_fov(simulator['array']) * u.deg
    pointing = source.directional_offset_by(position_angle, separation)
    return {'ra': pointing.ra.deg, 'dec': pointing.dec.deg, 'offset': separation.value}