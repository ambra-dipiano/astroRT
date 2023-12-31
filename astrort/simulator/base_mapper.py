# *****************************************************************************
# Copyright (C) 2023 Ambra Di Piano
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import argparse
from time import time
from os import makedirs
from astrort.utils.wrap import load_yaml_conf, write_mapping_info, execute_mapper_no_visibility, plot_map
from astrort.utils.utils import get_all_seeds
from astrort.configure.logging import set_logger, get_log_level, get_logfile
from astrort.configure.slurmjobs import slurm_submission

def base_mapper(configuration_file, seeds=None):
    clock = time()
    configuration = load_yaml_conf(configuration_file)
    logfile = get_logfile(configuration, mode='mapper')
    datfile = logfile.replace('.log', '.dat')
    # set logger
    log = set_logger(get_log_level(configuration['logging']['level']), logfile)
    # collect simulations to map
    if seeds is None:
        log.info(f"Mapping of all simulations found")
        seeds = get_all_seeds(configuration['simulator'])
    log.info(f"Mapper configured, took {time() - clock} s")
    # create output dir
    log.info(f"Output folder: {configuration['mapper']['output']}")
    makedirs(configuration['mapper']['output'], exist_ok=True)
    # start mapping
    log.info(f"\n {'-'*15} \n| START MAPPER | \n {'-'*15} \n")
    for seed in seeds:
        clock_map = time()
        # make map
        fitsmap = execute_mapper_no_visibility(configuration, log)
        log.info(f"Mapping (seed = {seed}) complete, took {time() - clock_map} s")
        # make plot
        if configuration['mapper']['plot'] and configuration['mapper']['save'] == 'fits':
            clock_plot = time()
            plotmap = plot_map(fitsmap, log)
            log.info(f"Plotting (seed = {seed}) complete, took {time() - clock_plot} s")
        # timing simulation
        clock_map = time() - clock_map
        # save simulation data
        write_mapping_info(configuration, datfile, clock_map)
        configuration['simulator']['seed'] += 1
    # end simulations
    log.info(f"\n {'-'*15} \n| STOP MAPPER | \n {'-'*15} \n")
    log.info(f"Process complete, took {time() - clock} s")

def main(configuration, nodes):
    if nodes == 0:
        base_mapper(configuration)
    else:
        slurm_submission(configuration, nodes, mode='mapper')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--configuration', type=str, required=True, help="Path of yaml configuration file")
    parser.add_argument('-n', '--nodes', type=int, default=0, help='Number of slurm nodes to occupy for submission, if unset it will not submit to slurm' )
    args = parser.parse_args()

    main(args.configuration, args.nodes)