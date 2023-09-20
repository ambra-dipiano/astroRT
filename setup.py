# *****************************************************************************
# Copyright (C) 2021 INAF
# This software is distributed under the terms of the BSD-3-Clause license
#
# Authors:
# Ambra Di Piano <ambra.dipiano@inaf.it>
# *****************************************************************************

from setuptools import setup, find_packages

entry_points = {
	'console_scripts': [
		'base_simulator = astrort.simulator.base_simulator:main',
    ]
}

setup( 
    name='astrort',
    author='Ambra Di Piano <ambra.dipiano@inaf.it>',
    package_dir={'astrort': 'astrort'},
    entry_points=entry_points,
    packages=find_packages(),
    include_package_data=True,
    license='BSD-3-Clause',
    python_requires=">=3.8",
)