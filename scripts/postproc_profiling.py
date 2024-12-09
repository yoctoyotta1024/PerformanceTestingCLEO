"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: postproc_profiling.py
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
Script converts output .dat and .txt files from multiple runs of an executable with
nsupers superdroplets into profilers zarr directories.
"""

import sys
from pathlib import Path

path2src = (
    Path(__file__).resolve().parent.parent / "src" / "profilers"
)  # for profilers module
sys.path.append(str(path2src))  # for imports for profilers
kokkos_tools_lib = Path("/work/bm1183/m300950/kokkos_tools_lib/lib64/")
from use_kp_profilers import get_profiler

path2builds = Path(sys.argv[1])  # must be absolute path
buildtype = sys.argv[2]  # "serial", "openmp" or "cuda"
executable = sys.argv[3]
profiler = sys.argv[4]
nsupers_runs = {
    8: 10,
    64: 10,
    1024: 5,
    8192: 5,
    16384: 2,
    131072: 2,
    524288: 2,
}

profiler = get_profiler(profiler, kokkos_tools_lib=kokkos_tools_lib)

for nsupers in nsupers_runs.keys():
    for nrun in range(nsupers_runs[nsupers]):
        binpath_run = (
            path2builds
            / buildtype
            / "bin"
            / executable
            / Path(f"nsupers{nsupers}")
            / Path(f"nrun{nrun}")
        )

        profiler.postprocess(filespath=binpath_run, to_dataset=True)
