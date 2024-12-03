"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: initconds_colls0d.py
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

import sys
from pathlib import Path
import subprocess

bash_script = Path(__file__).resolve().parent.parent / "bash" / "run_cleo.sh"
path2builds = Path(sys.argv[1])  # must be absolute path
buildtype = sys.argv[2]  # "serial", "openmp" or "gpu"
executable = path2builds / buildtype / "collisions0d" / "colls0d"
nsupers_runs = {
    8: 2,
    # 64: 1,
    # 1024: 1,
    # 8192: 1,
}

for nsupers in nsupers_runs.keys():
    for nrun in range(nsupers_runs[nsupers]):
        config_filename = (
            path2builds
            / buildtype
            / "tmp"
            / "colls0d"
            / Path(f"config_{nsupers}_{nrun}.yaml")
        )
        cmd = ["sbatch", str(bash_script), str(executable), str(config_filename)]
        print(" ".join(cmd))
        subprocess.run(cmd)
        print("\n")
