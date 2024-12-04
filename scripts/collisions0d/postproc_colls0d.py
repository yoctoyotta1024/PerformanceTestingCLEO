"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: postproc_colls0d.py
Project: collisions0d
Created Date: Monday 24th June 2024
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Monday 24th June 2024
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
Script converts output .dat and .txt files from multiple runs with nsupers superdroplets
using the coll0d into profilers zarr directories.
"""

import sys
from pathlib import Path

path2src = (
    Path(__file__).resolve().parent.parent.parent / "src" / "profilers"
)  # for profilers module
path2builds = Path(sys.argv[1])  # must be absolute path
buildtype = sys.argv[2]  # "serial", "openmp" or "gpu"
profiler = sys.argv[3]
nsupers_runs = {
    8: 2,
    64: 1,
}

sys.path.append(str(path2src))  # for imports for profilers
if profiler == "kerneltimer":
    from use_kp_profilers import KpKernelTimer

    profiler = KpKernelTimer()

elif profiler == "spacetimestack":
    from use_kp_profilers import KpSpaceTimeStack

    profiler = KpSpaceTimeStack()

for nsupers in nsupers_runs.keys():
    for nrun in range(nsupers_runs[nsupers]):
        binpath_run = (
            path2builds
            / buildtype
            / "bin"
            / "colls0d"
            / Path(f"nsupers{nsupers}")
            / Path(f"nrun{nrun}")
        )

        profiler.postprocess(filespath=binpath_run)
