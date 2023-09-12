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

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--configuration', type=str, required=True, help="Path of yaml configuration file")
    args = parser.parse_args()

    configutation = load_yaml_conf(args.configuration)
    makedirs(configutation['simulator']['output'], exist_ok=True)
    
    simulator = RTACtoolsSimulation()
    for i in range(configutation['simulator']['samples']):
        configutation['simulator']['seed'] += i
        simulator = configure_simulator_no_visibility(simulator, configutation['simulator'])
        simulator.run_simulation()

if __name__ == '__main__':
    main()



