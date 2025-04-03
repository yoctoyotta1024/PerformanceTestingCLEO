"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: prettyplots_thermo3d.py
Project: plotting
Created Date: Thursday 3rd April 2025
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Thursday 3rd April 2025
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
Standalone script for pretty plotting specific dataset of thermo3d example.
Intented for use on output dataset of thermo3d test with non-null observer compiled.
"""

# %%
import sys
from pathlib import Path

### ---------- input parameters ---------- ###
### path to CLEO for pySD module
path2CLEO = Path("/home") / "m" / "m300950" / "CLEO"
sys.path.append(str(path2CLEO))
from pySD.sdmout_src import pyzarr, pysetuptxt, pygbxsdat

### -------------------------------------- ###

# %%
### ---------- input parameters ---------- ###
### path to directory to save plots in
path4plots = Path("/home") / "m" / "m300950" / "performance_testing_cleo" / "plots"

### paths to datatsets for each build type
path2builds = (
    Path("/work") / "bm1183" / "m300950" / "performance_testing_cleo" / "builds"
)

### paths to particular dataset, setup file and grid file
buildtype = "cuda"
ngbxs = 2048
nsupers = 128
nthreads = 128
nrun = 0

gridfile = path2builds / "share" / "thermo3d" / f"dimlessGBxboundaries_{ngbxs}.dat"
path2bin = (
    path2builds
    / buildtype
    / "bin"
    / "thermo3d"
    / f"ngbxs{ngbxs}_nsupers{nsupers}"
    / f"nthreads{nthreads}"
    / f"nrun{nrun}"
)
dataset = path2bin / "sol.zarr"
setupfile = path2bin / "setup.txt"
### -------------------------------------- ###

# %%
### read in constants and intial setup from setup .txt file
config = pysetuptxt.get_config(setupfile, nattrs=3, isprint=False)
consts = pysetuptxt.get_consts(setupfile, isprint=False)
gbxs = pygbxsdat.get_gridboxes(gridfile, consts["COORD0"], isprint=False)

# read in output Xarray data
time = pyzarr.get_time(dataset)
sddata = pyzarr.get_supers(dataset, consts)
maxnsupers = pyzarr.get_totnsupers(dataset)
thermo = pyzarr.get_thermodata(
    dataset, config["ntime"], gbxs["ndims"], consts, getwinds=True
)

# %%
