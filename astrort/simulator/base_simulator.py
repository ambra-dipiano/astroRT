# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import argparse
from os import makedirs
from rtasci.lib.RTACtoolsSimulation import RTACtoolsSimulation
from astrort.utils.wrap import load_yaml_conf, configure_simulator_no_visibility
from astrort.configure.logging import set_logger

def base_simulator(configuration_file):
    configuration = load_yaml_conf(configuration_file)
    log = set_logger(configuration['logging']['level'])
    # create output dir
    log.info(f"Creating {configuration['simulator']['output']}")
    makedirs(configuration['simulator']['output'], exist_ok=True)
    
    # start simulations
    print(f"\n {'-'*17} \n| START SIMULATOR | \n {'-'*17} \n")
    for i in range(configuration['simulator']['samples']):
        simulator = RTACtoolsSimulation()
        configuration['simulator']['seed'] += i
        simulator = configure_simulator_no_visibility(simulator, configuration['simulator'])
        simulator.run_simulation()
        print(f"Simulation (seed = {configuration['simulator']['seed']}) complete")
        del simulator
    # end simulations
    print(f"\n {'-'*17} \n| STOP SIMULATOR | \n {'-'*17} ")


def slurm_submission(configuration_file):
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--configuration', type=str, required=True, help="Path of yaml configuration file")
    parser.add_argument('-n', '--nodes', type=int, default=0, help='Number of slurm nodes to occupy for submission, if unset it will not submit to slurm' )
    args = parser.parse_args()


    if args.nodes == 0:
        base_simulator(args.configuration)
    else:
        slurm_submission(args.configuration)



