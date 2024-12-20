"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: setup_colls0d.py
Project: collisions0d
Created Date: Thursday 5th December 2024
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Thursday 13th December 2024
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
Script calls src module to generate input files for CLEO 0-D box model
with volume exponential distribution as in Shima et al. 2009.
for a given build for nruns of nsupers superdroplets
"""

import argparse
import sys
import shutil
from pathlib import Path
import numpy as np
from typing import Optional

parser = argparse.ArgumentParser()
parser.add_argument("path2CLEO", type=Path, help="Absolute path to CLEO (for pySD)")
parser.add_argument("path2builds", type=Path, help="Absolute path to builds")
parser.add_argument(
    "buildtype",
    type=str,
    choices=["serial", "openmp", "cuda", "threads"],
    help="Type of build: serial, openmp, cuda or threads",
)
parser.add_argument(
    "--gen_initconds",
    type=str,
    choices=["TRUE", "FALSE"],
    default="TRUE",
    help="=='TRUE', else don't generate initial condition binary files",
)
args = parser.parse_args()

path2src = Path(__file__).resolve().parent.parent.parent / "src"
path2CLEO = args.path2CLEO
path2builds = args.path2builds
buildtype = args.buildtype
gen_initconds = args.gen_initconds

sys.path.append(str(path2CLEO))  # for imports for editing a config file
sys.path.append(str(path2src))  # for imports for input files generation
from collisions0d import initconds_colls0d
from pySD import editconfigfile

### ----- create temporary config file for simulation(s) ----- ###
src_config_filename = path2src / "collisions0d" / "config_colls0d.yaml"
ngbxs_nsupers_runs = {
    (1, 1): 2,
    (8, 1): 2,
}

if buildtype == "serial":
    ngbxs_nsupers_nthreads = {
        (ngbxs, nsupers): [1] for ngbxs, nsupers in ngbxs_nsupers_runs.keys()
    }
else:
    ngbxs_nsupers_nthreads = {
        (1, 1): [1],
        (8, 1): [8, 16],
    }

savefigpath = path2builds / "bin" / "colls0d"
sharepath = path2builds / "share" / "colls0d"
binpath = path2builds / buildtype / "bin" / "colls0d"
tmppath = path2builds / buildtype / "tmp" / "colls0d"
constants_filepath = path2builds / buildtype / "_deps" / "cleo-src" / "libs"
params = {
    "constants_filename": str(constants_filepath / "cleoconstants.hpp"),
    "sharepath": str(sharepath),
    "savefigpath": str(savefigpath),
}


def get_config_filename(
    tmppath: Path, ngbxs: int, nsupers: int, nrun: int, nthreads: Optional[int] = None
):
    if nthreads is not None:
        return tmppath / f"config_{ngbxs}_{nsupers}_{nthreads}_{nrun}.yaml"
    else:
        return tmppath / f"config_{ngbxs}_{nsupers}_{nrun}.yaml"


def get_grid_filename(sharepath: Path, ngbxs: int):
    return str(sharepath / f"dimlessGBxboundaries_{ngbxs}.dat")


def get_initsupers_filename(sharepath: Path, ngbxs: int, nsupers: int, nrun: int):
    return sharepath / f"dimlessSDsinit_{ngbxs}_{nsupers}_{nrun}.dat"


def get_binpath_onerun(
    binpath: Path, ngbxs: int, nsupers: int, nrun: int, nthreads: Optional[int] = None
):
    if nthreads is not None:
        return (
            binpath
            / f"ngbxs{ngbxs}_nsupers{nsupers}"
            / f"nthreads{nthreads}"
            / f"nrun{nrun}"
        )
    else:
        return binpath / f"ngbxs{ngbxs}_nsupers{nsupers}" / f"nrun{nrun}"


### --- ensure build, share and bin directories exist --- ###
if path2CLEO == path2builds:
    raise ValueError("build directory cannot be CLEO")
else:
    savefigpath.mkdir(exist_ok=True, parents=True)
    sharepath.mkdir(exist_ok=True, parents=True)
    binpath.mkdir(exist_ok=True, parents=True)
    tmppath.mkdir(exist_ok=True, parents=True)

for ngbxs, nsupers in ngbxs_nsupers_runs.keys():
    ### ----- Copy config to temporary file and edit specific parameters ----- ###
    for nrun in range(ngbxs_nsupers_runs[(ngbxs, nsupers)]):
        for nthreads in ngbxs_nsupers_nthreads[(ngbxs, nsupers)]:
            config_filename = get_config_filename(
                tmppath, ngbxs, nsupers, nrun, nthreads=nthreads
            )
            binpath_run = get_binpath_onerun(
                binpath, ngbxs, nsupers, nrun, nthreads=nthreads
            )

            params["num_threads"] = nthreads

            params["ngbxs"] = ngbxs
            params["grid_filename"] = str(get_grid_filename(sharepath, ngbxs))
            if np.cbrt(ngbxs) != np.round(np.cbrt(ngbxs)):
                raise ValueError("ngbxs must be a cube number for integer dimensions")
            ndim_z = ndim_x = ndim_y = int(np.cbrt(ngbxs))
            params["zgrid"] = [0, 10000, 10000 / ndim_z]
            params["xgrid"] = [0, 10000, 10000 / ndim_x]
            params["ygrid"] = [0, 10000, 10000 / ndim_y]

            params["maxnsupers"] = nsupers * ngbxs
            params["initsupers_filename"] = str(
                get_initsupers_filename(sharepath, ngbxs, nsupers, nrun)
            )

            params["setup_filename"] = str(binpath_run / "setup.txt")
            params["zarrbasedir"] = str(binpath_run / "sol.zarr")

            shutil.copy(Path(src_config_filename), config_filename)
            editconfigfile.edit_config_params(config_filename, params)

if gen_initconds == "TRUE":
    for ngbxs, nsupers in ngbxs_nsupers_runs.keys():
        isfigures = [True, True]
        nthreads_dummy = ngbxs_nsupers_nthreads[(ngbxs, nsupers)][
            0
        ]  # all nthreads use same initial conditions
        ### ----- write initial gridbox boundaries binary file ----- ###
        nrun_dummy = 0  # all runs use same init gbxs
        config_filename = get_config_filename(
            tmppath, ngbxs, nsupers, nrun=nrun_dummy, nthreads=nthreads_dummy
        )
        shutil.rmtree(get_grid_filename(sharepath, ngbxs), ignore_errors=True)
        initconds_colls0d.gridbox_boundaries(
            path2CLEO, config_filename, isfigures=isfigures
        )

        ### ----- write initial superdroplets binary files ----- ###
        for nrun in range(ngbxs_nsupers_runs[(ngbxs, nsupers)]):
            config_filename = get_config_filename(
                tmppath, ngbxs, nsupers, nrun, nthreads=nthreads_dummy
            )
            shutil.rmtree(
                get_initsupers_filename(sharepath, ngbxs, nsupers, nrun),
                ignore_errors=True,
            )
            initconds_colls0d.initial_superdroplet_conditions(
                path2CLEO, config_filename, isfigures=isfigures
            )
            isfigures = [False, False]  # only plot SD figures once
