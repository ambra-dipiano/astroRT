# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import argparse
from os.path import join
from astrort.utils.wrap import load_yaml_conf, merge_data_info
from astrort.configure.logging import set_logger

def main(configuration, mode):
    configuration = load_yaml_conf(configuration)
    logfile = join(configuration[mode]['output'], f'merge_{mode}_data.log')
    log = set_logger(configuration['logging']['level'], logfile)
    log.info(f"merge {mode} data files")
    merge_data_info(configuration[mode], mode, log)
    log.info(f"{mode} merge completed")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--configuration', type=str, required=True, help="Path of yaml configuration file")
    parser.add_argument('-m', '--mode', type=str, required=True, choices=['simulator', 'mapper'], help='Data table to merge')
    args = parser.parse_args()

    main(args.configuration, args.mode)