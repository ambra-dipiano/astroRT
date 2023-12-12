# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import argparse
import pandas as pd
from time import time
from rtasci.lib.RTACtoolsSimulation import RTACtoolsSimulation
from astrort.utils.wrap import load_yaml_conf, configure_simulator_no_visibility, write_simulation_info, set_pointing, set_irf, randomise_target, replicate_target
from astrort.configure.logging import set_logger, get_log_level, get_logfile
from astrort.configure.slurmjobs import slurm_submission

def base_simulator(configuration_file):
    clock = time()
    configuration = load_yaml_conf(configuration_file)
    logfile = get_logfile(configuration, mode='simulator')
    datfile = logfile.replace('.log', '.dat')
    log = set_logger(get_log_level(configuration['logging']['level']), logfile)
    log.info(f"Simulator configured, took {time() - clock} s")
    # create output dir
    log.info(f"Output folder: {configuration['simulator']['output']}")
    # start simulations
    log.info(f"\n {'-'*17} \n| START SIMULATOR | \n {'-'*17} \n")
    if configuration['simulator']['replicate'] is not None:
        replica = pd.read_csv(configuration['simulator']['replicate'], sep=' ', header=0)
        log.info(f"Replicate pointing and IRF from {configuration['simulator']['replicate']}")
    else:
        replica = None
    # loop seeds
    for i in range(configuration['simulator']['samples']):
        clock_sim = time()
        # randomise source position in model
        if configuration['simulator']['target'] == 'random' and replica is None:
            configuration['simulator']['model'] = randomise_target(model=configuration['simulator']['model'], output=configuration['simulator']['output'], name=configuration['simulator']['name'], samples=configuration['simulator']['samples'], seed=configuration['simulator']['seed'])
        simulator = RTACtoolsSimulation()
        # check pointing option
        if replica is not None:
            configuration['simulator']['pointing'] = {'ra': replica[replica['seed']==configuration['simulator']['seed']]['point_ra'].values[0],  
                                                      'dec': replica[replica['seed']==configuration['simulator']['seed']]['point_dec'].values[0]}
            configuration['simulator']['irf'] = replica[replica['seed']==configuration['simulator']['seed']]['irf'].values[0]   
            configuration['simulator']['model'] = replicate_target(model=configuration['simulator']['model'], output=configuration['simulator']['output'], name=configuration['simulator']['name'], samples=configuration['simulator']['samples'], seed=configuration['simulator']['seed'], ra=replica[replica['seed']==configuration['simulator']['seed']]['source_ra'].values[0], dec=replica[replica['seed']==configuration['simulator']['seed']]['source_dec'].values[0])

        simulator, point = set_pointing(simulator, configuration['simulator'], log)
        simulator.irf = set_irf(configuration['simulator'], log)
        # complete configuration
        simulator = configure_simulator_no_visibility(simulator, configuration['simulator'], log)
        simulator.run_simulation()
        log.info(f"Simulation (seed = {configuration['simulator']['seed']}) complete, took {time() - clock_sim} s")
        # timing simulation
        clock_sim = time() - clock_sim
        # save simulation data
        write_simulation_info(simulator, configuration['simulator'], point, datfile, clock_sim)
        configuration['simulator']['seed'] += 1
        del simulator
    # end simulations
    log.info(f"\n {'-'*17} \n| STOP SIMULATOR | \n {'-'*17} \n")
    log.info(f"Process complete, took {time() - clock} s")

def main(configuration, nodes):
    if nodes == 0:
        base_simulator(configuration)
    else:
        slurm_submission(configuration, nodes, mode='simulator')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--configuration', type=str, required=True, help="Path of yaml configuration file")
    parser.add_argument('-n', '--nodes', type=int, default=0, help='Number of slurm nodes to occupy for submission, if unset it will not submit to slurm' )
    parser.add_argument('-mp', '--mpthreads', type=int, default=0, choices=range(0,7), help='Number of threads to use for parallel simulation, if unset it will not use multi-threading' )
    args = parser.parse_args()

    main(args.configuration, args.nodes)

