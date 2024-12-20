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
from typing import Optional

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
ngbxs_nsupers_runs = {
    (1, 128): 5,
    (16, 128): 5,
    (64, 128): 5,
    (128, 128): 5,
    (256, 128): 2,
    (512, 128): 2,
    (1024, 128): 2,
    (2048, 128): 2,
    (4096, 128): 2,
}

if buildtype == "serial":
    ngbxs_nsupers_nthreads = {
        (ngbxs, nsupers): [1] for ngbxs, nsupers in ngbxs_nsupers_runs.keys()
    }
else:
    ngbxs_nsupers_nthreads = {
        (1, 128): [256, 128, 64, 16, 8, 1],
        (16, 128): [256, 128, 64, 16, 8, 1],
        (64, 128): [256, 128, 64, 16, 8, 1],
        (128, 128): [256, 128, 64, 16, 8, 1],
        (256, 128): [256, 128, 64, 16, 8, 1],
        (512, 128): [256, 128, 64, 16, 8],
        (1024, 128): [256, 128, 64, 16, 8],
        (2048, 128): [256, 128, 64, 16, 8],
        (4096, 128): [256, 128, 64, 16, 8],
    }


def get_config_filenames(
    path2build: Path,
    executable: str,
    ngbxs: int,
    nsupers: int,
    nrun: int,
    all_nthreads: Optional[list[int]] = None,
):
    if all_nthreads is None:
        return [
            path2build / "tmp" / executable / f"config_{ngbxs}_{nsupers}_{nrun}.yaml"
        ]
    else:
        configfiles = []
        for nthreads in all_nthreads:
            file = (
                path2build
                / "tmp"
                / executable
                / f"config_{ngbxs}_{nsupers}_{nthreads}_{nrun}.yaml"
            )
            configfiles.append(file)
        return configfiles


def get_binpaths_onerun(
    path2build: Path,
    executable: str,
    ngbxs: int,
    nsupers: int,
    nrun: int,
    all_nthreads: Optional[list[int]] = None,
):
    if all_nthreads is None:
        return [
            path2build
            / "bin"
            / executable
            / f"ngbxs{ngbxs}_nsupers{nsupers}"
            / f"nrun{nrun}"
        ]
    else:
        binpaths = []
        for nthreads in all_nthreads:
            bpath = (
                path2build
                / "bin"
                / executable
                / f"ngbxs{ngbxs}_nsupers{nsupers}"
                / f"nthreads{nthreads}"
                / f"nrun{nrun}"
            )
            binpaths.append(bpath)
        return binpaths


for profiler_name in profilers:
    profiler = get_profiler(profiler_name, kokkos_tools_lib=kokkos_tools_lib)
    for ngbxs, nsupers in ngbxs_nsupers_runs.keys():
        for nrun in range(ngbxs_nsupers_runs[(ngbxs, nsupers)]):
            all_nthreads = ngbxs_nsupers_nthreads[(ngbxs, nsupers)]
            binpaths_run = get_binpaths_onerun(
                path2build,
                executable,
                ngbxs,
                nsupers,
                nrun,
                all_nthreads=all_nthreads,
            )
            for bpath in binpaths_run:
                bpath.mkdir(exist_ok=True, parents=True)
            config_filenames = get_config_filenames(
                path2build,
                executable,
                ngbxs,
                nsupers,
                nrun,
                all_nthreads=all_nthreads,
            )
            files_tag = str(random.randint(100, 999))

            outpaths_cmd = " ".join(str(b) for b in binpaths_run)
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
                out = Path.cwd() / Path(
                    f"run_cleo_job_out.terminal{files_tag}.out"
                )  # see similarity to SBATCH --output in run_cleo.sh
                err = Path.cwd() / Path(
                    f"run_cleo_job_err.terminal{files_tag}.out"
                )  # see similarity to SBATCH --error in run_cleo.sh
                print(" ".join(cmd) + "\n")
                with open(out, "w") as outfile, open(err, "w") as errfile:
                    subprocess.run(cmd, stdout=outfile, stderr=errfile)
