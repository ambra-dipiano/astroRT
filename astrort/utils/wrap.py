# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import yaml
import numpy as np
import pandas as pd
import astropy.units as u
from os.path import dirname, abspath, join, basename, isfile
from rtasci.lib.RTAManageXml import ManageXml
from astropy.coordinates import SkyCoord 
from astrort.utils.utils import *
from astrort.configure.check_configuration import CheckConfiguration
from astrort.utils.mapping import Mapper
from astrort.utils.plotting import Plotter

def load_yaml_conf(yamlfile):
    with open(yamlfile) as f:
        configuration = yaml.load(f, Loader=yaml.FullLoader)
        CheckConfiguration(configuration=configuration)
    return configuration

def execute_mapper_no_visibility(configuration, log):
    phlist = seeds_to_string_formatter_files(configuration['simulator']['samples'], configuration['simulator']['output'], configuration['simulator']['name'], configuration['simulator']['seed'], 'fits')
    skymap = phlist.replace('.fits', '_map.fits').replace(configuration['simulator']['output'], configuration['mapper']['output'])
    maproi = get_instrument_fov(configuration['simulator']['array'])
    mapper = Mapper(log)
    mapper.get_countmap_in_fits(dl3_file=phlist, fitsname=skymap, template=map_template(), maproi=maproi, pixelsize=configuration['mapper']['pixelsize'], trange=[0, configuration['mapper']['exposure']], sigma=configuration['mapper']['smooth'])
    del mapper
    return skymap

def configure_simulator_no_visibility(simulator, configuration, log):
    if '$TEMPLATES$' in configuration['model']:
        configuration['model'] = join(dirname(abspath(__file__)).replace('utils', 'templates'), basename(configuration['model']))
    simulator.model = configuration['model']
    simulator.output = seeds_to_string_formatter_files(configuration['samples'], configuration['output'], configuration['name'], configuration['seed'], 'fits')
    simulator.caldb = configuration['prod']
    if configuration['irf'] == 'random':
        simulator.irf = select_random_irf(configuration['array'], configuration['prod'])
        log.info(f"Randomising instrument response function [{simulator.irf}]")
    else:
        simulator.irf = configuration['irf']
    simulator.fov = get_instrument_fov(configuration['array'])
    simulator.t = [0, configuration['duration']]
    simulator.e = adjust_tev_range_to_irf(get_instrument_tev_range(configuration['array']), simulator.irf)
    log.info(f"Verified energy range {simulator.e}")
    simulator.seed = configuration['seed']
    simulator.set_log = False
    return simulator

def set_pointing(simulator, configuration, log):
    if configuration['pointing'] == 'random':
        point = randomise_pointing_sim(configuration)
        log.info(f"Randomising pointing coordinates [{point['point_ra']}, {point['point_dec']}]")
    else:
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

def merge_simulation_info(configuration, log):
    folder = configuration['output']
    datfiles = [join(folder, f) for f in listdir(folder) if '.dat' in f and 'job' in f and 'simulator' in f]
    merger = join(folder, 'merged_sim_data.dat')
    # check merger file
    if isfile(merger):
        log.warning(f"Merger output already exists, overwrite {merger}")
        with open(merger, 'w+') as f:
            f.write('name seed start stop duration source_ra source_dec point_ra point_dec offset irf computation_time\n')
    # collect data
    for i, datfile in enumerate(datfiles):
        log.info(f"Collect data from {datfile}")
        data = pd.read_csv(join(datfile), sep=' ')
        if i == 0:
            table = data
        else:
            table = pd.concat([table, data], ignore_index=True)
        log.info(f"Lines in data: {len(table)}")
    # write merger file
    table.to_csv(merger, index=False, header=True, sep=' ', na_rep=np.nan)

def write_mapping_info(configuration, datfile, clock):
    name = seeds_to_string_formatter(configuration['simulator']['samples'], configuration['simulator']['name'], configuration['simulator']['seed'])
    seed = configuration['simulator']['seed']
    exposure = configuration['mapper']['exposure']
    center_type = configuration['mapper']['center']  
    pixelsize = configuration['mapper']['pixelsize']
    smooth = configuration['mapper']['smooth']
    if not isfile(datfile):
        with open(datfile, 'w+') as f:
            f.write('name seed exposure center_on pixelsize smooth computation_time\n')
    with open(datfile, 'a') as f:
        f.write(f'{name} {seed} {exposure} {center_type} {pixelsize} {smooth} {clock}\n')

def plot_map(fitsmap, log):
    plotmap = fitsmap.replace('.fits', '.png')
    plot = Plotter(log)
    plot.plot_fits_skymap(fitsmap, plotmap)
    del plot
    return plotmap
    