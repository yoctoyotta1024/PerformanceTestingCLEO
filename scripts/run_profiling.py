"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: run_profiling.py
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
Script calls subprocess to run multiple runs with nsupers superdroplets
using an executable for a given build.
"""

import argparse
import os
import sys
from pathlib import Path
import subprocess

executable_paths = {
    "colls0d": Path("collisions0d") / "colls0d",
}

path2src = (
    Path(__file__).resolve().parent.parent / "src" / "profilers"
)  # for profilers module
sys.path.append(str(path2src))  # for imports for profilers
kokkos_tools_lib = Path("/work/bm1183/m300950/kokkos_tools_lib/lib64/")
from use_kp_profilers import get_profiler

bash_script = Path(__file__).resolve().parent / "bash" / "run_cleo.sh"

parser = argparse.ArgumentParser()
parser.add_argument("path2builds", type=Path, help="Absolute path to builds")
parser.add_argument(
    "buildtype", type=str, help="Type of build: serial, openmp, cuda or threads"
)
parser.add_argument("executable", type=str, help="Executable name, e.g. colls0d")
parser.add_argument("profiler", type=str, help="KP name: kerneltimer or spacetimestack")
parser.add_argument(
    "sbatch", type=str, help="=='sbatch', else execute on current terminal"
)
args = parser.parse_args()

path2builds = args.path2builds
buildtype = args.buildtype
executable = args.executable
profiler = args.profiler
sbatch = args.sbatch

executable_path = path2builds / buildtype / executable_paths[executable]
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
        binpath_run.mkdir(exist_ok=True, parents=True)
        os.chdir(binpath_run)

        config_filename = (
            path2builds
            / buildtype
            / "tmp"
            / executable
            / Path(f"config_{nsupers}_{nrun}.yaml")
        )
        cmd = [
            str(bash_script),
            str(executable_path),
            str(config_filename),
        ]
        print(Path.cwd())
        if sbatch == "sbatch":
            cmd.insert(0, "sbatch")
            subprocess.run(cmd)
        else:
            out = (
                binpath_run / "run_cleo_out.terminalpipe.out"
            )  # see similarity to SBATCH --output in run_cleo.sh
            err = (
                binpath_run / "run_cleo_err.terminalpipe.out"
            )  # see similarity to SBATCH --error in run_cleo.sh
            with open(out, "w") as outfile, open(err, "w") as errfile:
                subprocess.run(cmd, stdout=outfile, stderr=errfile)
        print(" ".join(cmd))
        print("\n")
