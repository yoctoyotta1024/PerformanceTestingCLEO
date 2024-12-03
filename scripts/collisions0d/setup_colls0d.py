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
Script calls src module to generate input files for CLEO 0-D box model
with volume exponential distribution as in Shima et al. 2009.
"""

import sys
import shutil
from pathlib import Path

path2src = Path(__file__).resolve().parent.parent.parent / "src"
path2CLEO = Path(sys.argv[1])  # must be absolute path
path2builds = Path(sys.argv[2])  # must be absolute path
buildtype = sys.argv[3]  # "serial", "openmp" or "gpu"

sys.path.append(str(path2CLEO))  # for imports for editing a config file
sys.path.append(str(path2src))  # for imports for input files generation
from collisions0d import initconds_colls0d
from pySD import editconfigfile

### ----- create temporary config file for simulation(s) ----- ###
src_config_filename = path2src / "collisions0d" / "config_colls0d.yaml"
isfigures = [True, True]
nsupers_runs = {
    8: 10,
    64: 5,
    1024: 3,
    8192: 2,
}
savefigpath = path2builds / "bin" / "colls0d"
sharepath = path2builds / "share" / "colls0d"
binpath = path2builds / buildtype / "bin" / "colls0d"
tmppath = path2builds / buildtype / "tmp" / "colls0d"
constants_filepath = path2builds / buildtype / "_deps" / "cleo-src" / "libs"
params = {
    "constants_filename": str(constants_filepath / "cleoconstants.hpp"),
    "grid_filename": str(sharepath / "dimlessGBxboundaries.dat"),
    "sharepath": str(sharepath),
    "savefigpath": str(savefigpath),
}

### --- ensure build, share and bin directories exist --- ###
if path2CLEO == path2builds:
    raise ValueError("build directory cannot be CLEO")
else:
    savefigpath.mkdir(exist_ok=True, parents=True)
    sharepath.mkdir(exist_ok=True, parents=True)
    binpath.mkdir(exist_ok=True, parents=True)
    tmppath.mkdir(exist_ok=True, parents=True)

for nsupers in nsupers_runs.keys():
    ### ----- Copy config to temporary file and edit specific parameters ----- ###
    for nrun in range(nsupers_runs[nsupers]):
        params["maxnsupers"] = nsupers
        params["initsupers_filename"] = str(
            sharepath / f"dimlessSDsinit_{nsupers}_{nrun}.dat"
        )
        params["setup_filename"] = str(binpath / f"setup_{nsupers}_{nrun}.txt")
        params["stats_filename"] = str(binpath / f"stats_{nsupers}_{nrun}.txt")
        params["zarrbasedir"] = str(binpath / f"sol_{nsupers}_{nrun}.zarr")

        config_filename = tmppath / f"config_{nsupers}_{nrun}.yaml"
        shutil.copy(Path(src_config_filename), config_filename)
        editconfigfile.edit_config_params(config_filename, params)

        ### ----- write initial gridbox boundaries and superdroplets binary files ----- ###
        shutil.rmtree(params["grid_filename"], ignore_errors=True)
        shutil.rmtree(params["initsupers_filename"], ignore_errors=True)
        initconds_colls0d.main(path2CLEO, config_filename, isfigures)
