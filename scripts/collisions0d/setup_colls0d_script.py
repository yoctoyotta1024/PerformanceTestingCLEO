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
path2build = Path(sys.argv[2])  # must be absolute path

sys.path.append(str(path2CLEO))  # for imports for editing a config file
sys.path.append(str(path2src))  # for imports for input files generation
from collisions0d import initconds_colls0d
from pySD import editconfigfile

### ----- create temporary config file for simulation(s) ----- ###
src_config_filename = path2src / "collisions0d" / "config_colls0d.yaml"
isfigures = [True, True]
nsupers_runs = [8, 64, 1024, 8192]
sharepath = path2build / "share" / "colls0d"
binpath = path2build / "bin" / "colls0d"
tmppath = path2build / "tmp" / "colls0d"
params = {
    "constants_filename": str(
        path2build / "_deps" / "cleo-src" / "libs" / "cleoconstants.hpp"
    ),
    "sharepath": str(sharepath),
    "binpath": str(binpath),
    "grid_filename": str(sharepath / "dimlessGBxboundaries.dat"),
}

### --- ensure build, share and bin directories exist --- ###
if path2CLEO == path2build:
    raise ValueError("build directory cannot be CLEO")
else:
    path2build.mkdir(exist_ok=True)
    sharepath.mkdir(exist_ok=True, parents=True)
    binpath.mkdir(exist_ok=True, parents=True)
    tmppath.mkdir(exist_ok=True, parents=True)

for nsupers in nsupers_runs:
    ### ----- Copy config to temporary file and edit specific parameters ----- ###
    params["maxnsupers"] = nsupers
    params["initsupers_filename"] = str(sharepath / f"dimlessSDsinit_{nsupers}.dat")
    params["setup_filename"] = str(binpath / f"setup_{nsupers}.txt")
    params["stats_filename"] = str(binpath / f"stats_{nsupers}.txt")
    params["zarrbasedir"] = str(binpath / f"sol_{nsupers}.zarr")

    config_filename = tmppath / f"config_{nsupers}.yaml"
    shutil.copy(Path(src_config_filename), config_filename)
    editconfigfile.edit_config_params(config_filename, params)

    ### ----- write initial gridbox boundaries and superdroplets binary files ----- ###
    shutil.rmtree(params["grid_filename"], ignore_errors=True)
    shutil.rmtree(params["initsupers_filename"], ignore_errors=True)
    initconds_colls0d.main(path2CLEO, config_filename, isfigures)
