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
    choices=["kerneltimer", "spacetimestack", "memoryevents", "memoryusage"],
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
            datfiles = profiler.postprocess(
                filespath=binpath_run, to_dataset=True, allow_overwrite=allow_overwrite
            )
            if len(datfiles) > 0:
                print(
                    f"{profiler.name} postproccesing complete for ngbxs={ngbxs}, nsupers={nsupers}, nrun={nrun}"
                )
