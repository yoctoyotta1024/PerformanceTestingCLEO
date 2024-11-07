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
Script generates input files for CLEO 0-D box model
with volume exponential distribution as in Shima et al. 2009.
"""

import sys
from pathlib import Path


def main(path2CLEO, config_filename, isfigures=[False, False]):
    import yaml

    sys.path.append(path2CLEO)  # for imports from pySD package
    from pySD.initsuperdropsbinary_src import rgens, probdists, attrsgen
    from pySD import geninitconds as gic

    config = yaml.safe_load(open(config_filename))
    pyconfig = config["python_initconds"]

    ### ---------------------------------------------------------------- ###
    ### ----------------------- INPUT PARAMETERS ----------------------- ###
    ### ---------------------------------------------------------------- ###
    ### --- essential paths and filenames --- ###
    # path and filenames for creating initial SD conditions
    constants_filename = config["inputfiles"]["constants_filename"]
    initsupers_filename = config["initsupers"]["initsupers_filename"]
    grid_filename = config["inputfiles"]["grid_filename"]
    savefigpath = Path(pyconfig["paths"]["binpath"])

    ### --- settings for 0-D Model gridbox boundaries --- ###
    zgrid = pyconfig["grid"]["zgrid"]
    xgrid = pyconfig["grid"]["xgrid"]
    ygrid = pyconfig["grid"]["ygrid"]

    ### --- settings for initial superdroplets --- ###
    # settings for superdroplet coordinates
    nsupers = config["domain"]["maxnsupers"]

    # settings for superdroplet attributes
    dryradius = pyconfig["supers"]["dryradius"]

    # radius distirbution from exponential in droplet volume for setup 1
    rspan = pyconfig["supers"]["rspan"]
    volexpr0 = pyconfig["supers"]["volexpr0"]
    numconc = pyconfig["supers"]["numconc"]

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
    ### -------------------- INPUT FILES GENERATION -------------------- ###
    ### ---------------------------------------------------------------- ###
    gic.generate_gridbox_boundaries(
        grid_filename,
        zgrid,
        xgrid,
        ygrid,
        constants_filename,
        isfigures=isfigures,
        savefigpath=savefigpath,
    )
    gic.generate_initial_superdroplet_conditions(
        initattrsgen,
        initsupers_filename,
        config_filename,
        constants_filename,
        grid_filename,
        nsupers,
        numconc,
        isfigures=isfigures,
        savefigpath=savefigpath,
        gbxs2plt="all",
        savelabel=f"_{nsupers}",
    )
    ### ---------------------------------------------------------------- ###
    ### ---------------------------------------------------------------- ###


if __name__ == "__main__":
    path2CLEO = Path(sys.argv[1])  # must be absolute
    config_filename = Path(sys.argv[2])  # must be absolute
    isfigures = [sys.argv[3], sys.argv[4]]

    main(path2CLEO, config_filename, isfigures=isfigures)
