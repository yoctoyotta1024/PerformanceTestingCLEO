"""
Copyright (c) 2024 MPI-M, Clara Bayley


-----  PerformanceTestingCLEO -----
File: initconds_colls0D.py
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

def main(path2CLEO, path2build, config_filename):
    import os
    from pathlib import Path
    import yaml

    sys.path.append(path2CLEO)  # for imports from pySD package
    from pySD.initsuperdropsbinary_src import rgens, probdists, attrsgen
    from pySD.initsuperdropsbinary_src import create_initsuperdrops as csupers
    from pySD.initsuperdropsbinary_src import read_initsuperdrops as rsupers
    from pySD.gbxboundariesbinary_src import read_gbxboundaries as rgrid
    from pySD.gbxboundariesbinary_src import create_gbxboundaries as cgrid

    config = yaml.safe_load(open(config_filename))
    pyconfig = config["python_initconds"]

    ### ---------------------------------------------------------------- ###
    ### -------------- INPUT FILES' GENERATION FUNCTIONS --------------- ###
    ### ---------------------------------------------------------------- ###
    ### ----- write gridbox boundaries binary ----- ###
    def generate_gridbox_boundaries(
        grid_filename, zgrid, xgrid, ygrid, constants_filename, savefigpath, isfigures
    ):
        cgrid.write_gridboxboundaries_binary(
            grid_filename, zgrid, xgrid, ygrid, constants_filename
        )
        rgrid.print_domain_info(constants_filename, grid_filename)
        ### show (and save) plots of binary file data
        if isfigures[0]:
            rgrid.plot_gridboxboundaries(
                constants_filename, grid_filename, savefigpath, isfigures[1]
            )


    ### ----- write initial superdroplets binary ----- ###
    def generate_initial_superdroplet_conditions(
        initattrsgen,
        initsupers_filename,
        config_filename,
        constants_filename,
        grid_filename,
        nsupers,
        numconc,
        savefigpath,
        isfigures,
    ):
        csupers.write_initsuperdrops_binary(
            initsupers_filename,
            initattrsgen,
            config_filename,
            constants_filename,
            grid_filename,
            nsupers,
            numconc,
        )
        rsupers.print_initSDs_infos(
            initsupers_filename, config_filename, constants_filename, grid_filename
        )

        ### show (and save) plots of binary file data
        if isfigures[0]:
            rsupers.plot_initGBxs_distribs(
                config_filename,
                constants_filename,
                initsupers_filename,
                grid_filename,
                savefigpath,
                isfigures[1],
                "all",
                savelabel="",
            )
    ### ---------------------------------------------------------------- ###
    ### ---------------------------------------------------------------- ###

    ### ---------------------------------------------------------------- ###
    ### ----------------------- INPUT PARAMETERS ----------------------- ###
    ### ---------------------------------------------------------------- ###
    ### --- essential paths and filenames --- ###
    # path and filenames for creating initial SD conditions
    constants_filename = config["inputfiles"]["constants_filename"]
    binpath = pyconfig["paths"]["binpath"]
    sharepath = pyconfig["paths"]["sharepath"]
    initsupers_filename = config["initsupers"]["initsupers_filename"]
    grid_filename = config["inputfiles"]["grid_filename"]

    # booleans for [making, saving] initialisation figures
    isfigures = [True, True]
    savefigpath = binpath  # directory for saving figures

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
    os.system("rm " + grid_filename)
    os.system("rm " + initsupers_filename)

    generate_gridbox_boundaries(
        grid_filename, zgrid, xgrid, ygrid, constants_filename, savefigpath, isfigures
    )
    generate_initial_superdroplet_conditions(
        initattrsgen,
        initsupers_filename,
        config_filename,
        constants_filename,
        grid_filename,
        nsupers,
        numconc,
        savefigpath,
        isfigures,
    )
    ### ---------------------------------------------------------------- ###
    ### ---------------------------------------------------------------- ###

if __name__ == "__main__":
    path2CLEO = sys.argv[1]
    path2build = sys.argv[2]
    config_filename = sys.argv[3]

    main(path2CLEO, path2build, config_filename)