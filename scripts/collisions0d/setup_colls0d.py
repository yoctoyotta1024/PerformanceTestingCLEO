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

parser = argparse.ArgumentParser()
parser.add_argument("path2CLEO", type=Path, help="Absolute path to CLEO (for pySD)")
parser.add_argument("path2builds", type=Path, help="Absolute path to builds")
parser.add_argument(
    "buildtype", type=str, help="Type of build: serial, openmp, cuda or threads"
)
parser.add_argument(
    "gen_initconds", type=str, help="General initial condition binary files"
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


def get_config_filename(tmppath: Path, ngbxs: int, nsupers: int, nrun: int):
    return tmppath / f"config_{ngbxs}_{nsupers}_{nrun}.yaml"


def get_grid_filename(sharepath: Path, ngbxs: int):
    return str(sharepath / f"dimlessGBxboundaries_{ngbxs}.dat")


def get_initsupers_filename(sharepath: Path, ngbxs: int, nsupers: int, nrun: int):
    return sharepath / f"dimlessSDsinit_{ngbxs}_{nsupers}_{nrun}.dat"


def get_binpath_onerun(binpath: Path, ngbxs: int, nsupers: int, nrun: int):
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
        config_filename = get_config_filename(tmppath, ngbxs, nsupers, nrun)
        binpath_run = get_binpath_onerun(binpath, ngbxs, nsupers, nrun)

        if np.cbrt(ngbxs) != np.round(np.cbrt(ngbxs)):
            raise ValueError("ngbxs must be a cube number for integer dimensions")
        params["ngbxs"] = ngbxs
        ndim_z = ndim_x = ndim_y = int(np.cbrt(ngbxs))
        params["zgrid"] = [0, 10000, 10000 / ndim_z]
        params["xgrid"] = [0, 10000, 10000 / ndim_x]
        params["ygrid"] = [0, 10000, 10000 / ndim_y]
        params["grid_filename"] = str(get_grid_filename(sharepath, ngbxs))

        params["maxnsupers"] = nsupers * ngbxs
        params["initsupers_filename"] = str(
            get_initsupers_filename(sharepath, ngbxs, nsupers, nrun)
        )

        params["setup_filename"] = str(binpath_run / "setup.txt")
        params["zarrbasedir"] = str(binpath_run / "sol.zarr")

        shutil.copy(Path(src_config_filename), config_filename)
        editconfigfile.edit_config_params(config_filename, params)

if gen_initconds == "true":
    for ngbxs, nsupers in ngbxs_nsupers_runs.keys():
        isfigures = [True, True]
        ### ----- write initial gridbox boundaries binary file ----- ###
        config_filename = get_config_filename(tmppath, ngbxs, nsupers, nrun=0)
        shutil.rmtree(get_grid_filename(sharepath, ngbxs), ignore_errors=True)
        initconds_colls0d.gridbox_boundaries(
            path2CLEO, config_filename, isfigures=isfigures
        )

        ### ----- write initial superdroplets binary files ----- ###
        for nrun in range(ngbxs_nsupers_runs[(ngbxs, nsupers)]):
            config_filename = get_config_filename(tmppath, ngbxs, nsupers, nrun)
            shutil.rmtree(
                get_initsupers_filename(sharepath, ngbxs, nsupers, nrun),
                ignore_errors=True,
            )
            initconds_colls0d.initial_superdroplet_conditions(
                path2CLEO, config_filename, isfigures=isfigures
            )
            isfigures = [False, False]  # only plot SD figures once
