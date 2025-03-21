"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: plot_motion2d.py
Project: validations
Created Date: Friday 21st March 2025
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Friday 21st March 2025
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
Script plots results from 2-D superdroplet motion example
"""

import argparse
import sys
from pathlib import Path
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("path2CLEO", type=Path, help="Absolute path to CLEO (for pySD)")
parser.add_argument("path2gridfile", type=Path, help="Absolute path to .dat grid file")
parser.add_argument("path2dataset", type=Path, help="Absolute path to .zarr dataset")
parser.add_argument(
    "path2setupfile", type=Path, help="Absolute path to .txt setup file"
)
args = parser.parse_args()

path2CLEO = args.path2CLEO
gridfile = args.path2gridfile
dataset = args.path2dataset
setupfile = args.path2setupfile

savedir = Path("/home/m/m300950/performance_testing_cleo/plots/")

sys.path.append(str(path2CLEO))  # imports from pySD
sys.path.append(
    str(path2CLEO / "examples" / "exampleplotting")
)  # imports from example plots package

from plotssrc import pltsds, pltmoms
from pySD.sdmout_src import pyzarr, pysetuptxt, pygbxsdat


### ---------------- plotting functions ---------------- ###
def motion2d_validation_plot(time, sddata, maxnsupers):
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    pltmoms.plot_totnsupers(time, maxnsupers, fig=fig, ax=axs[0])

    nsample = min(500, maxnsupers[0])
    pltsds.plot_randomsample_superdrops_2dmotion(
        sddata,
        maxnsupers[0],
        nsample,
        fig=fig,
        ax=axs[1],
    )

    return fig, axs


### ---------------------------------------------------- ###

### read in constants and intial setup from setup .txt file
config = pysetuptxt.get_config(setupfile, nattrs=3, isprint=True)
consts = pysetuptxt.get_consts(setupfile, isprint=True)
gbxs = pygbxsdat.get_gridboxes(gridfile, consts["COORD0"], isprint=True)

# read in output Xarray data
time = pyzarr.get_time(dataset)
sddata = pyzarr.get_supers(dataset, consts)
maxnsupers = pyzarr.get_totnsupers(dataset)

fig, axs = motion2d_validation_plot(time, sddata, maxnsupers)
savename = savedir / Path("motion2d_validation.png")
fig.savefig(savename, dpi=400, bbox_inches="tight", facecolor="w", format="png")
print("Figure .png saved as: " + str(savename))
plt.show()
