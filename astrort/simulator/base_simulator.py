# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import argparse
from time import time
from os import makedirs
from os.path import join
from rtasci.lib.RTACtoolsSimulation import RTACtoolsSimulation
from astrort.utils.wrap import load_yaml_conf, configure_simulator_no_visibility, write_simulation_info, set_pointing
from astrort.configure.logging import set_logger, get_log_level
from astrort.configure.slurmjobs import make_simulator_sbatch

def base_simulator(configuration_file):
    clock = time()
    configuration = load_yaml_conf(configuration_file)
    logfile = join(configuration['simulator']['output'], 'simulator_' + configuration['logging']['logfile'])
    datfile = logfile.replace('.log', '.dat')
    log = set_logger(get_log_level(configuration['logging']['level']), logfile)
    log.info(f"Simulator configured, took {time() - clock} s")
    # create output dir
    log.info(f"Output folder: {configuration['simulator']['output']}")
    makedirs(configuration['simulator']['output'], exist_ok=True)
    # start simulations
    log.info(f"\n {'-'*17} \n| START SIMULATOR | \n {'-'*17} \n")
    for i in range(configuration['simulator']['samples']):
        clock_sim = time()
        simulator = RTACtoolsSimulation()
        # check pointing option
        simulator, point = set_pointing(simulator, configuration['simulator'], log)
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


def slurm_submission(configuration_file, nodes):
    configuration = load_yaml_conf(configuration_file)
    log = set_logger(get_log_level(configuration['logging']['level']))
    # create output dir
    log.info(f"Creating {configuration['simulator']['output']}")
    makedirs(configuration['simulator']['output'], exist_ok=True)
    # sbatch jobs per each nodes
    configuration['slurm']['nodes'] = nodes
    for node_number in range(configuration['slurm']['nodes']):
        jobname = f"{configuration['slurm']['name']}_{node_number+1}"
        make_simulator_sbatch(jobname, configuration, node_number)
    return

def main(configuration, nodes):
    if nodes == 0:
        base_simulator(configuration)
    else:
        slurm_submission(configuration, nodes)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--configuration', type=str, required=True, help="Path of yaml configuration file")
    parser.add_argument('-n', '--nodes', type=int, default=0, help='Number of slurm nodes to occupy for submission, if unset it will not submit to slurm' )
    args = parser.parse_args()

    main(args.configuration, args.nodes)

