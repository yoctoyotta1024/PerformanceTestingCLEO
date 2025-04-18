"""
Copyright (c) 2024 MPI-M, Clara Bayley


-----  PerformanceTestingCLEO -----
File: initconds_colls0d.py
Project: collisions0d
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
Script generates input files for CLEO 0-D box model
with volume exponential distribution as in Shima et al. 2009.
"""

import argparse
import sys
from pathlib import Path


def main(path2CLEO, config_filename, isfigures=[False, False]):
    gridbox_boundaries(path2CLEO, config_filename, isfigures=isfigures)
    initial_superdroplet_conditions(path2CLEO, config_filename, isfigures=isfigures)


def gridbox_boundaries(path2CLEO, config_filename, isfigures=[False, False]):
    import yaml

    sys.path.append(path2CLEO)  # for imports from pySD package
    from pySD import geninitconds as gic

    config = yaml.safe_load(open(config_filename))
    pyconfig = config["python_initconds"]

    ### ----------------------- INPUT PARAMETERS ----------------------- ###
    ### --- essential paths and filenames --- ###
    constants_filename = config["inputfiles"]["constants_filename"]
    grid_filename = config["inputfiles"]["grid_filename"]
    savefigpath = Path(pyconfig["paths"]["savefigpath"])

    ### --- number of gridboxes and uperdroplets per gridbox --- ###
    ngbxs = config["domain"]["ngbxs"]
    savelabel = f"_{ngbxs}"

    ### --- settings for 0-D Model gridbox boundaries --- ###
    zgrid = pyconfig["grid"]["zgrid"]
    xgrid = pyconfig["grid"]["xgrid"]
    ygrid = pyconfig["grid"]["ygrid"]
    ### ---------------------------------------------------------------- ###

    ### -------------------- INPUT FILES GENERATION -------------------- ###
    gic.generate_gridbox_boundaries(
        grid_filename,
        zgrid,
        xgrid,
        ygrid,
        constants_filename,
        isfigures=isfigures,
        savefigpath=savefigpath,
        savelabel=savelabel,
    )
    ### ---------------------------------------------------------------- ###


def initial_superdroplet_conditions(
    path2CLEO, config_filename, isfigures=[False, False]
):
    import yaml

    sys.path.append(path2CLEO)  # for imports from pySD package
    from pySD.initsuperdropsbinary_src import rgens, probdists, attrsgen, crdgens
    from pySD import geninitconds as gic

    config = yaml.safe_load(open(config_filename))
    pyconfig = config["python_initconds"]

    ### ----------------------- INPUT PARAMETERS ----------------------- ###
    ### --- essential paths and filenames --- ###
    initsupers_filename = config["initsupers"]["initsupers_filename"]
    constants_filename = config["inputfiles"]["constants_filename"]
    grid_filename = config["inputfiles"]["grid_filename"]
    savefigpath = Path(pyconfig["paths"]["savefigpath"])

    ### --- number of gridboxes and uperdroplets per gridbox --- ###
    ngbxs = config["domain"]["ngbxs"]
    nsupers = int(config["domain"]["maxnsupers"] / ngbxs)
    savelabel = f"_{ngbxs}_{nsupers}"

    ### --- settings for initial superdroplets --- ###
    # settings for superdroplet attributes
    dryradius = pyconfig["supers"]["dryradius"]

    # settings for radius distribution from exponential in droplet volume for setup
    rspan = pyconfig["supers"]["rspan"]
    xi_min = pyconfig["supers"]["xi_min"]
    volexpr0 = pyconfig["supers"]["volexpr0"]
    numconc = pyconfig["supers"]["numconc"]

    # attribute generators
    radiigen = rgens.SampleLog10RadiiGen(rspan)  # radii are sampled from rspan [m]
    dryradiigen = rgens.MonoAttrGen(dryradius)
    xiprobdist = probdists.VolExponential(volexpr0, rspan)
    xiprobdist = probdists.MinXiDistrib(xiprobdist, xi_min)
    coord3gen = crdgens.SampleCoordGen(True)
    coord1gen = crdgens.SampleCoordGen(True)
    coord2gen = crdgens.SampleCoordGen(True)
    initattrsgen = attrsgen.AttrsGenerator(
        radiigen, dryradiigen, xiprobdist, coord3gen, coord1gen, coord2gen
    )
    ### ---------------------------------------------------------------- ###

    ### -------------------- INPUT FILES GENERATION -------------------- ###
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
        gbxs2plt=0,
        savelabel=savelabel,
    )
    ### ---------------------------------------------------------------- ###


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path2CLEO", type=Path, help="Absolute path to CLEO (for pySD)")
    parser.add_argument("config_filename", type=Path, help="Absolute path to config")
    parser.add_argument("is_plotfigs", type=bool, help="True then make figures")
    parser.add_argument("is_savefigs", type=bool, help="True then save figures")
    args = parser.parse_args()

    path2CLEO = args.path2CLEO
    config_filename = args.config_filename
    isfigures = [args.is_pltfigs, args.is_savefigs]

    main(path2CLEO, config_filename, isfigures=isfigures)
