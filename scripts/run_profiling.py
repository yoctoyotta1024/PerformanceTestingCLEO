"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: run_colls0d.py
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
Script calls subprocess to run multiple runs with nsupers superdroplets
using the coll0d executable for a given build.
"""

import os
import sys
from pathlib import Path
import subprocess

path2src = (
    Path(__file__).resolve().parent.parent.parent / "src" / "profilers"
)  # for profilers module
bash_script = Path(__file__).resolve().parent.parent / "bash" / "run_cleo.sh"
path2builds = Path(sys.argv[1])  # must be absolute path
buildtype = sys.argv[2]  # "serial", "openmp" or "gpu"
profiler = sys.argv[3]
executable = path2builds / buildtype / "collisions0d" / "colls0d"
nsupers_runs = {
    8: 2,
    64: 1,
}

sys.path.append(str(path2src))  # for imports for profilers
if profiler == "kerneltimer":
    from use_kp_profilers import KpKernelTimer

    profiler = KpKernelTimer()  # TODO(CB): update with spacetiemstack too
elif profiler == "spacetimestack":
    from use_kp_profilers import KpSpaceTimeStack

    profiler = KpSpaceTimeStack()  # TODO(CB): update with spacetiemstack too

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
        os.chdir(binpath_run)

        config_filename = (
            path2builds
            / buildtype
            / "tmp"
            / "colls0d"
            / Path(f"config_{nsupers}_{nrun}.yaml")
        )
        cmd = ["sbatch", str(bash_script), str(executable), str(config_filename)]

        print(Path.cwd())
        print(" ".join(cmd))
        subprocess.run(cmd)
        print("\n")
