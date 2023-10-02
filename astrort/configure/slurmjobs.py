# *****************************************************************************
# Copyright (C) 2023 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

from yaml import dump
from os import system, makedirs
from os.path import join, dirname, abspath
from astrort.utils.wrap import load_yaml_conf
from astrort.configure.logging import set_logger, get_log_level

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

def make_sbatch(jobname, configuration, node_number, mode):
    output = configuration[mode]['output']
    jobname_sh = join(output, f"{jobname}_{mode}.sh")
    jobname_log = join(output, f"{jobname}_{mode}.slurm")
    jobname_conf = join(output, f"{jobname}_{mode}.yml")
    make_configuration(jobname_conf, configuration, node_number, mode=mode)
    make_sh(jobname, configuration['slurm'], jobname_conf, jobname_sh, jobname_log)
    system(f"sbatch {jobname_sh}")

def slurm_submission(configuration_file, nodes, mode):
    configuration = load_yaml_conf(configuration_file)
    log = set_logger(get_log_level(configuration['logging']['level']))
    # create output dir
    log.info(f"Creating {configuration['simulator']['output']}")
    makedirs(configuration['simulator']['output'], exist_ok=True)
    # sbatch jobs per each nodes
    configuration['slurm']['nodes'] = nodes
    for node_number in range(configuration['slurm']['nodes']):
        jobname = f"{configuration['slurm']['name']}_{node_number+1}"
        make_sbatch(jobname, configuration, node_number, mode=mode)
