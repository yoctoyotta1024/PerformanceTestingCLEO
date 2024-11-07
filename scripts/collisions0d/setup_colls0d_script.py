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
path2CLEO = sys.argv[1]
path2build = sys.argv[2]
src_config_filename = sys.argv[3]

sys.path.append(path2CLEO)  # for imports for editing a config file
sys.path.append(str(path2src))  # for imports for input files generation
from collisions0d import initconds_colls0d
from pySD import editconfigfile

### ----- create temporary config file for simulation ----- ###
# Copy config to temporary file and edit specific parameters
params = {
    "maxnsupers": 8192,
}
nstr = str(params["maxnsupers"])
params["constants_filename"] = path2build + "/_deps/cleo-src/libs/cleoconstants.hpp"
params["sharepath"] = path2build + "/share"
params["grid_filename"] = params["sharepath"] + "/dimlessGBxboundaries_colls0d.dat"
params["binpath"] = path2build + "/bin_" + nstr
params["initsupers_filename"] = (
    params["sharepath"] + "/dimlessSDsinit_colls0d_" + nstr + ".dat"
)
params["setup_filename"] = params["binpath"] + "/setup_colls0d_" + nstr + ".txt"
params["stats_filename"] = params["binpath"] + "/stats_colls0d_" + nstr + ".txt"
params["zarrbasedir"] = params["binpath"] + "/sol_colls0d_" + nstr + ".zarr"

if path2CLEO == path2build:
    raise ValueError("build directory cannot be CLEO")
else:
    path2tmp = Path(path2build) / "tmp"
    Path(path2build).mkdir(exist_ok=True)
    path2tmp.mkdir(exist_ok=True)

config_filename = path2tmp / "config_colls0d.yaml"
shutil.copy(Path(src_config_filename), config_filename)
editconfigfile.edit_config_params(config_filename, params)

### ----- write initial gridbox boundaries and superdroplets binary files ----- ###
initconds_colls0d.main(path2CLEO, path2build, config_filename)
