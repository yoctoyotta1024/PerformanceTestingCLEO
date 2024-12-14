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
import random

executable_paths = {
    "colls0d": Path("collisions0d") / "colls0d",
}

path2src = (
    Path(__file__).resolve().parent.parent / "src" / "profilers"
)  # for profilers module
sys.path.append(str(path2src))  # for imports for profilers
kokkos_tools_lib = Path("/work/bm1183/m300950/kokkos_tools_lib/lib64/")
from use_kp_profilers import get_profiler

parser = argparse.ArgumentParser()
parser.add_argument("path2builds", type=Path, help="Absolute path to builds")
parser.add_argument(
    "buildtype", type=str, help="Type of build: serial, openmp, cuda or threads"
)
parser.add_argument("executable", type=str, help="Executable name, e.g. colls0d")
parser.add_argument(
    "profilers", type=str, nargs="+", help="KP names, e.g. kerneltimer spacetimestack"
)
parser.add_argument(
    "--sbatch",
    type=str,
    default="TRUE",
    help="=='TRUE', else execute on current terminal",
)

args = parser.parse_args()

path2build = args.path2builds / args.buildtype
buildtype = args.buildtype
executable = args.executable
profilers = args.profilers
sbatch = args.sbatch

if buildtype == "cuda":
    bash_script = Path(__file__).resolve().parent / "bash" / "run_cleo_gpu.sh"
else:
    bash_script = Path(__file__).resolve().parent / "bash" / "run_cleo.sh"

executable_path = path2build / executable_paths[executable]
ngbxs_nsupers_runs = {
    (1, 1): 2,
    (8, 1): 2,
    (64, 1): 2,
    (512, 1): 2,
    (4096, 1): 2,
    (32768, 1): 2,
    (262144, 1): 2,
    (1, 16): 2,
    (64, 16): 2,
    (4096, 16): 2,
    (262144, 16): 2,
}


def get_config_filename(
    path2build: Path, executable: str, ngbxs: int, nsupers: int, nrun: int
):
    return path2build / "tmp" / executable / f"config_{ngbxs}_{nsupers}_{nrun}.yaml"


def get_binpath_onerun(
    path2build: Path, executable: str, ngbxs: int, nsupers: int, nrun: int
):
    return (
        path2build
        / "bin"
        / executable
        / f"ngbxs{ngbxs}_nsupers{nsupers}"
        / f"nrun{nrun}"
    )


for profiler_name in profilers:
    profiler = get_profiler(profiler_name, kokkos_tools_lib=kokkos_tools_lib)
    for ngbxs, nsupers in ngbxs_nsupers_runs.keys():
        for nrun in range(ngbxs_nsupers_runs[(ngbxs, nsupers)]):
            binpath_run = get_binpath_onerun(
                path2build, executable, ngbxs, nsupers, nrun
            )
            binpath_run.mkdir(exist_ok=True, parents=True)
            os.chdir(binpath_run)

            config_filename = get_config_filename(
                path2build, executable, ngbxs, nsupers, nrun
            )
            cmd = [
                str(bash_script),
                buildtype,
                str(executable_path),
                str(config_filename),
            ]
            print(Path.cwd())
            if sbatch == "TRUE":
                cmd.insert(0, "sbatch")
                subprocess.run(cmd)
            else:
                fileid = f"terminalpipe{random.randint(10000, 99999)}"
                out = binpath_run / Path(
                    f"run_cleo_out.{fileid}.out"
                )  # see similarity to SBATCH --output in run_cleo.sh
                err = binpath_run / Path(
                    f"run_cleo_err.{fileid}.out"
                )  # see similarity to SBATCH --error in run_cleo.sh
                with open(out, "w") as outfile, open(err, "w") as errfile:
                    subprocess.run(cmd, stdout=outfile, stderr=errfile)
            print(" ".join(cmd))
            print("\n")
