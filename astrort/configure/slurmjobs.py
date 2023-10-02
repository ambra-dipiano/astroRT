# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

from yaml import dump
from os import system
from os.path import join, dirname, abspath

def make_configuration(jobname_conf, configuration, node_number):
    # simulator
    configuration['simulator']['seed'] = node_number*configuration['simulator']['samples'] + 1
    # logging
    configuration['logging']['logfile'] = join(configuration['simulator']['output'], f'job_{node_number+1}_simulator.log')
    configuration['logging']['datfile'] = join(configuration['simulator']['output'], f'job_{node_number+1}_simulator.dat')
    # write new configuration
    with open(jobname_conf, 'w+') as f:
        dump(configuration, f, default_flow_style=False)

def make_sh(jobname, slurmconf, jobname_conf, jobname_sh, jobname_log, mode='simulator'):
    # write sbatch
    with open(jobname_sh, 'w+') as f:
        f.write("#!/bin/bash")
        #f.write("\n#SBATCH --nodes=1")
        #f.write("\n#SBATCH --ntasks-per-node=1")
        #f.write("\n#SBATCH --cpus-per-task=2")
        f.write(f"\n#SBATCH --job-name={jobname}")
        #f.write(f"\n#SBATCH --mem={slurmconf['memory']}")
        f.write(f"\n#SBATCH --output={jobname_log}")
        f.write(f"\n#SBATCH --account={slurmconf['account']}")
        f.write(f"\n#SBATCH --partition={slurmconf['partition']}")
        f.write(f"\n")
        f.write(f"\nsource activate {slurmconf['environment']}")
        if mode == 'simulator':
            f.write(f"\npython {join(dirname(abspath(__file__)).replace('configure', 'simulator'), 'base_simulator.py')} -f {jobname_conf}\n")
        elif mode == 'mapper':
            f.write(f"\npython {join(dirname(abspath(__file__)).replace('configure', 'simulator'), 'base_mapper.py')} -f {jobname_conf}\n")
        else:
            raise ValueError(f"Invalid 'mode' {mode}")

def make_simulator_sbatch(jobname, configuration, node_number):
    output = configuration['simulator']['output']
    jobname_sh = join(output, f"{jobname}_simulator.sh")
    jobname_log = join(output, f"{jobname}_simulator.slurm")
    jobname_conf = join(output, f"{jobname}_simulator.yml")
    make_configuration(jobname_conf, configuration, node_number, mode='simulator')
    make_sh(jobname, configuration['slurm'], jobname_conf, jobname_sh, jobname_log)
    system(f"sbatch {jobname_sh}")
    
def make_mapper_sbatch(jobname, configuration, node_number):
    output = configuration['mapper']['output']
    jobname_sh = join(output, f"{jobname}_mapper.sh")
    jobname_log = join(output, f"{jobname}_mapper.slurm")
    jobname_conf = join(output, f"{jobname}_mapper.yml")
    make_configuration(jobname_conf, configuration, node_number, mode='mapper')
    make_sh(jobname, configuration['slurm'], jobname_conf, jobname_sh, jobname_log)
    system(f"sbatch {jobname_sh}")
    return