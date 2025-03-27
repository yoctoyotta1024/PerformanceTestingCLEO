"""
Copyright (c) 2024 MPI-M, Clara Bayley


-----  PerformanceTestingCLEO -----
File: initconds_motion2d.py
Project: motion2d
Created Date: Thursday 20th March 2025
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Thursday 20th March 2025
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
    thermodynamic_conditions(path2CLEO, config_filename, isfigures=isfigures)


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
    from pySD.initsuperdropsbinary_src import (
        rgens,
        dryrgens,
        probdists,
        attrsgen,
        crdgens,
    )
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
    mono_radius = pyconfig["supers"]["mono_radius"]
    numconc = pyconfig["supers"]["numconc"]

    # attribute generators
    radiigen = rgens.MonoAttrGen(mono_radius)
    dryradiigen = dryrgens.ScaledRadiiGen(1.0)
    xiprobdist = probdists.DiracDelta(mono_radius)
    coord3gen = crdgens.SampleCoordGen(True)
    coord1gen = crdgens.SampleCoordGen(True)
    coord2gen = None
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


def thermodynamic_conditions(path2CLEO, config_filename, isfigures=[False, False]):
    import yaml

    sys.path.append(path2CLEO)  # for imports from pySD package
    from pySD import geninitconds as gic
    from pySD.thermobinary_src import thermodyngen, thermogen, windsgen

    config = yaml.safe_load(open(config_filename))
    pyconfig = config["python_initconds"]

    ### ----------------------- INPUT PARAMETERS ----------------------- ###
    ### --- essential paths and filenames --- ###
    thermofiles = Path(pyconfig["thermo"]["thermofiles"])
    constants_filename = config["inputfiles"]["constants_filename"]
    grid_filename = config["inputfiles"]["grid_filename"]
    savefigpath = Path(pyconfig["paths"]["savefigpath"])

    ### --- number of gridboxes and uperdroplets per gridbox --- ###
    ngbxs = config["domain"]["ngbxs"]
    savelabel = f"_{ngbxs}"

    # thermodynamics generator
    VVEL = None
    thermog = thermogen.Simple2TierRelativeHumidity(
        config_filename,
        constants_filename,
        pyconfig["thermo"]["PRESS"],
        pyconfig["thermo"]["THETA"],
        pyconfig["thermo"]["qvapmethod"],
        pyconfig["thermo"]["sratios"],
        pyconfig["thermo"]["Zbase"],
        pyconfig["thermo"]["qcond_init"],
    )
    windsg = windsgen.Simple2DFlowField(
        config_filename,
        constants_filename,
        pyconfig["thermo"]["WMAX"],
        pyconfig["thermo"]["Zlength"],
        pyconfig["thermo"]["Xlength"],
        VVEL,
    )
    thermodyngen = thermodyngen.ThermodynamicsGenerator(thermog, windsg)
    ### ---------------------------------------------------------------- ###

    ### -------------------- INPUT FILES GENERATION -------------------- ###
    gic.generate_thermodynamics_conditions_fromfile(
        thermofiles,
        thermodyngen,
        config_filename,
        constants_filename,
        grid_filename,
        isfigures=isfigures,
        savefigpath=savefigpath,
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
