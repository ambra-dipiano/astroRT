# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import argparse
from rtasci.utils.RTACtoolsSimulation import RTACtoolsSimulation
from rtavis.utils.visibility import Visibility
from astrort.utils.wrap import load_yaml_conf
from astrort.cfg.check_configuration import CheckConfiguration

parser = argparse.ArgumentParser(description='')
parser.add_argument('-cf', '--conf', type=str, required=True, help="Path of yaml configuration file")
args = parser.parse_args()

conf = load_yaml_conf(args.conf)



