"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: create_grand_datasets.py
Project: scripts
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
Script converts multiple zarr xarray datasets for nsupers and nruns of each build
type into mean over nruns for each build in one "grand" dataset.
"""

import os
import sys
import glob
from pathlib import Path

path2builds = Path(sys.argv[1])  # must be absolute path
buildtype = sys.argv[2]
executable = sys.argv[3]
profiler = sys.argv[4]
nsupers_runs = {
    8: 2,
    64: 1,
}

grand_ds = []
for nsupers in nsupers_runs.keys():
    for nrun in range(nsupers_runs[nsupers]):
        filespath = (
            path2builds
            / buildtype
            / "bin"
            / executable
            / f"nsupers{nsupers}"
            / f"nrun{nrun}"
        )
        filenames = glob.glob(os.path.join(filespath, f"kp_{profiler}_*.zarr"))
        for filename in filenames:
            print(filename)
        # ds = xr.open_zarr(filename)
