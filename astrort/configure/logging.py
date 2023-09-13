# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import logging
from os import makedirs
from os.path import isdir, dirname

def set_logger(level, filename=None):
    log = logging.getLogger()
    log.setLevel(level)
    # console logger
    formatter = logging.Formatter('[%(asctime)s] %(name)s %(levelname)s: %(message)s')
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    log.addHandler(consoleHandler)
    # file logger
    if filename is not None:
        if not isdir(dirname(filename)):
            makedirs(dirname(filename))
        fileHandler = logging.FileHandler(filename)
        fileHandler.setFormatter(formatter)
        log.addHandler(fileHandler)
    return log