"""
Copyright (c) 2024 MPI-M, Clara Bayley

----- PerformanceTestingCLEO -----
File: setup.py
Project: performance_testing_cleo
Created Date: Tuesday 27th February 2024
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Friday 21st June 2024
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
setup for pre-commit tool
"""


from setuptools import setup, find_packages

setup(
    name="PerformanceTestingCLEO",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pytest",
        "sphinx",
    ],
)
