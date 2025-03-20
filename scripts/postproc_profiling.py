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
import argparse
from pathlib import Path

import shared_script_variables as ssv

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
    "executable",
    type=str,
    choices=["colls0d", "cond0d", "thermo3d"],
    help="Executable name, e.g. colls0d",
)
parser.add_argument(
    "profilers",
    type=str,
    nargs="+",
    choices=["none", "kerneltimer", "spacetimestack", "memoryevents", "memoryusage"],
    help="KP names, e.g. kerneltimer spacetimestack",
)
parser.add_argument(
    "--allow_overwrite",
    type=str,
    choices=["TRUE", "FALSE"],
    default="FALSE",
    help="Allow zarr datasets to overwrite exisiting ones (!)",
)
args = parser.parse_args()

path2build = args.path2builds / args.buildtype
buildtype = args.buildtype
executable = args.executable
profilers = args.profilers
if args.allow_overwrite == "TRUE":
    allow_overwrite = True
else:
    allow_overwrite = False
binpath = path2build / "bin" / executable

ngbxs_nsupers_runs = ssv.get_ngbxs_nsupers_runs()
ngbxs_nsupers_nthreads = ssv.get_ngbxs_nsupers_nthreads(
    buildtype, ngbxs_nsupers_runs=ngbxs_nsupers_runs
)

for profiler_name in profilers:
    profiler = get_profiler(profiler_name, kokkos_tools_lib=kokkos_tools_lib)
    for ngbxs, nsupers in ngbxs_nsupers_runs.keys():
        for nthreads in ngbxs_nsupers_nthreads[(ngbxs, nsupers)]:
            for nrun in range(ngbxs_nsupers_runs[(ngbxs, nsupers)]):
                binpath_run = ssv.get_run_binpath(
                    binpath, ngbxs, nsupers, nrun, nthreads=nthreads
                )
                datfiles = profiler.postprocess(
                    filespath=binpath_run,
                    to_dataset=True,
                    allow_overwrite=allow_overwrite,
                )
                if len(datfiles) > 0:
                    print(
                        f"{profiler.name} postproccesing complete for ngbxs={ngbxs}, nsupers={nsupers}, nrun={nrun}, nthreads={nthreads}"
                    )
