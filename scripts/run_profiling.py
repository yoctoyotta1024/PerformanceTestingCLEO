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
import sys
from pathlib import Path
import subprocess
import random

import shared_script_variables as ssv

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
    "buildtype",
    type=str,
    choices=["serial", "openmp", "cuda", "threads"],
    help="Type of build: serial, openmp, cuda or threads",
)
parser.add_argument(
    "executable", type=str, choices=["colls0d"], help="Executable name, e.g. colls0d"
)
parser.add_argument(
    "profilers",
    type=str,
    nargs="+",
    choices=["none", "kerneltimer", "spacetimestack", "memoryevents", "memoryusage"],
    help="KP names, e.g. kerneltimer spacetimestack",
)
parser.add_argument(
    "--sbatch",
    type=str,
    choices=["TRUE", "FALSE"],
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

ngbxs_nsupers_runs = ssv.get_ngbxs_nsupers_runs()
ngbxs_nsupers_nthreads = ssv.get_ngbxs_nsupers_nthreads(
    buildtype, ngbxs_nsupers_runs=ngbxs_nsupers_runs
)

for profiler_name in profilers:
    profiler = get_profiler(profiler_name, kokkos_tools_lib=kokkos_tools_lib)
    for ngbxs, nsupers in ngbxs_nsupers_runs.keys():
        for nrun in range(ngbxs_nsupers_runs[(ngbxs, nsupers)]):
            all_nthreads = ngbxs_nsupers_nthreads[(ngbxs, nsupers)]
            run_binpaths = ssv.get_all_nthreads_run_binpaths(
                path2build,
                executable,
                ngbxs,
                nsupers,
                nrun,
                all_nthreads=all_nthreads,
            )
            for bpath in run_binpaths:
                bpath.mkdir(exist_ok=True, parents=True)
            config_filenames = ssv.get_all_nthreads_config_filenames(
                path2build,
                executable,
                ngbxs,
                nsupers,
                nrun,
                all_nthreads=all_nthreads,
            )
            files_tag = str(random.randint(100, 999))

            outpaths_cmd = " ".join(str(b) for b in run_binpaths)
            config_filenames_cmd = " ".join(str(c) for c in config_filenames)
            cmd = [
                str(bash_script),
                buildtype,
                str(executable_path),
                outpaths_cmd,
                config_filenames_cmd,
                files_tag,
            ]
            if sbatch == "TRUE":
                cmd.insert(0, "sbatch")
                print(" ".join(cmd) + "\n")
                subprocess.run(cmd)
            else:
                out = (
                    Path.cwd()
                    / "tmp_jobs"
                    / f"run_cleo_job_out.terminal{files_tag}.out"
                )  # see similarity to SBATCH --output in run_cleo.sh
                err = (
                    Path.cwd()
                    / "tmp_jobs"
                    / f"run_cleo_job_err.terminal{files_tag}.out"
                )  # see similarity to SBATCH --error in run_cleo.sh
                print(" ".join(cmd) + "\n")
                with open(out, "w") as outfile, open(err, "w") as errfile:
                    subprocess.run(cmd, stdout=outfile, stderr=errfile)
