"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: plot_colls0d.py
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
Script plots results from 0-D box model of superdroplet collisions
"""

import argparse
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import awkward as ak

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

from plotssrc import shima2009fig
from pySD.sdmout_src import pyzarr, pysetuptxt, pygbxsdat, sdtracing


### ---------------- plotting functions ---------------- ###
def plot_mass_density_distributions(
    time,
    sddata,
    t2plts,
    gbx2plt,
    volume,
    smoothsig,
):
    xlims = [10, 5000]
    nbins = 100
    witherr = False
    non_nanradius = ak.nan_to_none(sddata["radius"])
    rspan = [ak.min(non_nanradius), ak.max(non_nanradius)]

    attrs2sel = ["sdgbxindex", "radius", "xi"]
    selsddata = sdtracing.attributes_at_times(sddata, time, t2plts, attrs2sel)

    fig, ax, _ = shima2009fig.setup_validation_figure(witherr, xlims)

    for n in range(len(t2plts)):
        ind = np.argmin(abs(time - t2plts[n]))
        tlab = "t = {:.2f}s".format(time[ind])
        c = "C" + str(n)

        sdgbxindex = selsddata["sdgbxindex"][n]
        radius = np.where(sdgbxindex == gbx2plt, selsddata["radius"][n], np.nan)
        xi = np.where(sdgbxindex == gbx2plt, selsddata["xi"][n], np.nan)

        hist, hcens = shima2009fig.calc_massdens_distrib(
            rspan, nbins, volume, xi, radius, sddata, smoothsig
        )

        if smoothsig:
            ax.plot(hcens, hist, label=tlab, color=c)
        else:
            ax.step(hcens, hist, label=tlab, where="mid", color=c)
    ax.legend()

    fig.tight_layout()

    return fig, ax


def colls0d_validation_plot(time, gbxs, sddata, volexpr0):
    smoothsig = False
    # nsupers0 = np.sum(np.where(sddata.sdgbxindex[0] == 0, 1, 0)) # initial num superdrops in 0th gbx
    # smoothsig = 0.62 * (nsupers0 ** (-1 / 5))  # = ~0.2 for guassian smoothing

    t2plts = [0, 600, 1200, 1800, 3600]
    time = time.secs

    gbx2plt = 0  # plot 0th gridbox
    volume = gbxs["gbxvols"][0, 0, 0]  # assuming all gbxs have same volume [m^3]

    fig, ax = plot_mass_density_distributions(
        time,
        sddata,
        t2plts,
        gbx2plt,
        volume,
        smoothsig,
    )

    return fig, ax


### ---------------------------------------------------- ###

### read in constants and intial setup from setup .txt file
config = pysetuptxt.get_config(setupfile, nattrs=3, isprint=True)
consts = pysetuptxt.get_consts(setupfile, isprint=True)
gbxs = pygbxsdat.get_gridboxes(gridfile, consts["COORD0"], isprint=True)

# read in output Xarray data
time = pyzarr.get_time(dataset)
sddata = pyzarr.get_supers(dataset, consts)

fig, axs = colls0d_validation_plot(time, gbxs, sddata, config["volexpr0"])
savename = savedir / Path("colls0d_validation.png")
fig.savefig(savename, dpi=400, bbox_inches="tight", facecolor="w", format="png")
print("Figure .png saved as: " + str(savename))
plt.show()
