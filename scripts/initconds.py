"""
Copyright (c) 2024 MPI-M, Clara Bayley


-----  PerformanceTestingCLEO -----
File: initconds.py
Project: scripts
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
Script generates input files for CLEO 0-D box model
with volume exponential distribution as in Shima et al. 2009.
"""

import os
import sys
import numpy as np
from pathlib import Path

path2CLEO = sys.argv[1]
path2build = sys.argv[2]
configfile = sys.argv[3]

sys.path.append(path2CLEO)  # for imports from pySD package
from pySD.initsuperdropsbinary_src import rgens, probdists, attrsgen
from pySD.initsuperdropsbinary_src import create_initsuperdrops as csupers
from pySD.initsuperdropsbinary_src import read_initsuperdrops as rsupers
from pySD.gbxboundariesbinary_src import read_gbxboundaries as rgrid
from pySD.gbxboundariesbinary_src import create_gbxboundaries as cgrid

### ---------------------------------------------------------------- ###
### ----------------------- INPUT PARAMETERS ----------------------- ###
### ---------------------------------------------------------------- ###
### --- essential paths and filenames --- ###
# path and filenames for creating initial SD conditions
constsfile = path2CLEO + "/libs/cleoconstants.hpp"
binpath = path2build + "/bin/"
sharepath = path2build + "/share/"
initSDsfile = sharepath + "breakup_dimlessSDsinit.dat"
gridfile = sharepath + "breakup_dimlessGBxboundaries.dat"

# booleans for [making, saving] initialisation figures
isfigures = [True, True]
savefigpath = path2build + "/bin/"  # directory for saving figures

### --- settings for 0-D Model gridbox boundaries --- ###
zgrid = np.asarray([0, 100])
xgrid = np.asarray([0, 100])
ygrid = np.asarray([0, 100])

### --- settings for initial superdroplets --- ###
# settings for superdroplet coordinates
nsupers = 8192

# settings for superdroplet attributes
dryradius = 1e-16  # all SDs have negligible solute [m]


# radius distirbution from exponential in droplet volume for setup 1
rspan = [1e-7, 9e-5]  # max and min range of radii to sample [m]
volexpr0 = 30.531e-6  # peak of volume exponential distribution [m]
numconc = 2 ** (23)  # total no. conc of real droplets [m^-3]

# attribute generators
radiigen = rgens.SampleLog10RadiiGen(rspan)  # radii are sampled from rspan [m]
dryradiigen = rgens.MonoAttrGen(dryradius)
xiprobdist = probdists.VolExponential(volexpr0, rspan)
coord3gen = None  # do not generate superdroplet coords
coord1gen = None
coord2gen = None
initattrsgen = attrsgen.AttrsGenerator(
    radiigen, dryradiigen, xiprobdist, coord3gen, coord1gen, coord2gen
)
### ---------------------------------------------------------------- ###
### ---------------------------------------------------------------- ###

### ---------------------------------------------------------------- ###
### -------------- INPUT FILES' GENERATION FUNCTIONS --------------- ###
### ---------------------------------------------------------------- ###
### --- ensure build, share and bin directories exist --- ###
if path2CLEO == path2build:
    raise ValueError("build directory cannot be CLEO")
else:
    Path(path2build).mkdir(exist_ok=True)
    Path(sharepath).mkdir(exist_ok=True)
    Path(binpath).mkdir(exist_ok=True)
    if isfigures[1]:
        Path(savefigpath).mkdir(exist_ok=True)

### --- delete any existing initial conditions --- ###
os.system("rm " + gridfile)
os.system("rm " + initSDsfile)


### ----- write gridbox boundaries binary ----- ###
def generate_gridbox_boundaries(
    gridfile, zgrid, xgrid, ygrid, constsfile, savefigpath, isfigures
):
    cgrid.write_gridboxboundaries_binary(gridfile, zgrid, xgrid, ygrid, constsfile)
    rgrid.print_domain_info(constsfile, gridfile)
    ### show (and save) plots of binary file data
    if isfigures[0]:
        rgrid.plot_gridboxboundaries(constsfile, gridfile, savefigpath, isfigures[1])


### ----- write initial superdroplets binary ----- ###
def generate_initial_superdroplet_conditions(
    initattrsgen,
    initSDsfile,
    configfile,
    constsfile,
    gridfile,
    nsupers,
    numconc,
    savefigpath,
    isfigures,
):
    csupers.write_initsuperdrops_binary(
        initSDsfile, initattrsgen, configfile, constsfile, gridfile, nsupers, numconc
    )
    rsupers.print_initSDs_infos(initSDsfile, configfile, constsfile, gridfile)

    ### show (and save) plots of binary file data
    if isfigures[0]:
        rsupers.plot_initGBxs_distribs(
            configfile,
            constsfile,
            initSDsfile,
            gridfile,
            savefigpath,
            isfigures[1],
            "all",
            savelabel="",
        )


### ---------------------------------------------------------------- ###
### ---------------------------------------------------------------- ###

### ---------------------------------------------------------------- ###
### -------------------- INPUT FILES GENERATION -------------------- ###
### ---------------------------------------------------------------- ###
generate_gridbox_boundaries(
    gridfile, zgrid, xgrid, ygrid, constsfile, savefigpath, isfigures
)
generate_initial_superdroplet_conditions(
    initattrsgen,
    configfile,
    constsfile,
    gridfile,
    nsupers,
    numconc,
    savefigpath,
    isfigures,
)
### ---------------------------------------------------------------- ###
### ---------------------------------------------------------------- ###
