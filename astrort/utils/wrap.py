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
from os.path import dirname, abspath, join, basename, isfile
from astrort.utils.utils import *
from astrort.configure.check_configuration import CheckConfiguration
from rtasci.lib.RTAManageXml import ManageXml
from rtasci.lib.RTAUtils import check_energy_thresholds
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
    simulator.output = seeds_to_string_formatter_files(configuration['samples'], configuration['output'], configuration['name'], configuration['seed'], 'fits')
    simulator.caldb = configuration['prod']
    if configuration['irf'] == 'random':
        simulator.irf = select_random_irf(configuration['array'], configuration['prod'])
    else:
        simulator.irf = configuration['irf']
    simulator.fov = get_instrument_fov(configuration['array'])
    simulator.t = [0, configuration['duration']]
    simulator.e = check_energy_thresholds(get_instrument_tev_range(configuration['array']), configuration['irf'])
    simulator.seed = configuration['seed']
    simulator.set_log = False
    return simulator

def set_pointing(simulator, configuration, log):
    if configuration['pointing'] == 'random':
        log.info(f"Randomising pointing coordinates")
        point = randomise_pointing_sim(configuration)
    else:
        log.info(f"Using fixed pointing coordinates")
        point = get_point_source_info(configuration)
    simulator.ra = point['point_ra']
    simulator.dec = point['point_dec']
    return simulator, point

def randomise_pointing_sim(simulator):
    if '$TEMPLATES$' in simulator['model']:
        simulator['model'] = join(dirname(abspath(__file__)).replace('utils', 'templates'), basename(simulator['model']))
    model_xml = ManageXml(xml=simulator['model'])
    source = model_xml.getRaDec()
    del model_xml
    # use astropy separation
    ra, dec = source[0][0] * u.deg, source[1][0] * u.deg
    source = SkyCoord(ra, dec, frame='icrs')
    position_angle = 45 * u.deg
    separation = np.random.random() * get_instrument_fov(simulator['array']) * u.deg
    pointing = source.directional_offset_by(position_angle, separation)
    return {'point_ra': pointing.ra.deg, 'point_dec': pointing.dec.deg, 'offset': separation.value, 'source_ra': source.ra.deg, 'source_dec': source.dec.deg}

def get_point_source_info(simulator):
    if '$TEMPLATES$' in simulator['model']:
        simulator['model'] = join(dirname(abspath(__file__)).replace('utils', 'templates'), basename(simulator['model']))
    model_xml = ManageXml(xml=simulator['model'])
    source = model_xml.getRaDec()
    del model_xml
    # use astropy separation
    source = SkyCoord(source[0][0] * u.deg, source[1][0] * u.deg, frame='icrs')
    pointing = SkyCoord(simulator['pointing']['ra'] * u.deg, simulator['pointing']['dec'] * u.deg, frame='icrs')
    separation = source.separation(pointing)
    return {'point_ra': pointing.ra.deg, 'point_dec': pointing.dec.deg, 'offset': separation.value, 'source_ra': source.ra.deg, 'source_dec': source.dec.deg}

def write_simulation_info(simulator, configuration, pointing, datfile, clock):
    name = seeds_to_string_formatter(configuration['samples'], configuration['name'], configuration['seed'])
    seed = simulator.seed
    tstart, tstop = simulator.t
    duration = configuration['duration']
    irf = configuration['irf']
    point_ra, point_dec, offset, source_ra, source_dec = pointing['point_ra'], pointing['point_dec'], pointing['offset'], pointing['source_ra'], pointing['source_dec']
    if not isfile(datfile):
        with open(datfile, 'w+') as f:
            f.write('name seed start stop duration source_ra source_dec point_ra point_dec offset irf computation_time\n')
    with open(datfile, 'a') as f:
        f.write(f'{name} {seed} {tstart} {tstop} {duration} {source_ra} {source_dec} {point_ra} {point_dec} {offset} {irf} {clock}\n')
    return