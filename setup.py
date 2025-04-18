"""
Copyright (c) 2024 MPI-M, Clara Bayley

----- PerformanceTestingCLEO -----
File: setup.py
Project: performance_testing_cleo
Created Date: Thursday 5th December 2024
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Thursday 5th December 2024
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
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "sphinx",
    ],
)
