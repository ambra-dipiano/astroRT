# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

import sys
from os import system

start_job_id = int(sys.argv[1])
jobs = int(sys.argv[2])

for i in range(jobs):
    system(f"scancel {start_job_id+i}")

