# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import argparse
from rtasci.rtasci.lib.RTACtoolsSimulation import RTACtoolsSimulation
from astrort.utils.wrap import load_yaml_conf

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-cf', '--conf', type=str, required=True, help="Path of yaml configuration file")
    args = parser.parse_args()

    conf = load_yaml_conf(args.conf)

if __name__ == '__main__':
    main()



