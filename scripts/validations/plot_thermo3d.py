"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: plot_thermo3d.py
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
Script plots results from 3-D superdroplet model in constant thermodynamics example
"""

import argparse
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.markers import MarkerStyle
from matplotlib.cm import ScalarMappable
import random

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

from plotssrc import pltsds
from pySD.sdmout_src import pyzarr, pysetuptxt, pygbxsdat, sdtracing


### ---------------- plotting functions ---------------- ###
def plot_coord3_radius(fig, ax, time, sddata, ids2plot, colors=None):
    attrs = ["coord3", "radius"]
    data = sdtracing.attrs_for_superdroplets_sample(sddata, attrs, ids=ids2plot)

    radius = data["radius"] * 1e-3
    coord3 = data["coord3"] / 1000
    mks = MarkerStyle("o", fillstyle="full")
    ax.plot(radius, coord3, color="grey", alpha=0.1)
    if colors:
        ax.scatter(radius, coord3, marker=mks, s=0.4, cmap=colors[0], c=colors[1])
    else:
        ax.scatter(radius, coord3, marker=mks, s=0.4)

    ax.set_ylabel("z /km")
    ax.set_xlabel("radius /mm")
    ax.set_xscale("log")

    ax.set_xlim(1e-4, 1)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    return fig, ax


def thermo3d_validation_plot(time, sddata, maxnsupers):
    fig = plt.figure(figsize=(12, 6))
    gs = GridSpec(2, 2, figure=fig, height_ratios=[1, 27])

    nsample = min(100, maxnsupers[0])
    ids2plot = random.sample(list(range(0, maxnsupers[0], 1)), nsample)

    cmap = plt.get_cmap("plasma")  # Choose your colormap
    values = np.repeat(time.mins, len(ids2plot))

    ax0 = fig.add_subplot(gs[1, 0])
    plot_coord3_radius(fig, ax0, time, sddata, ids2plot, colors=[cmap, values])

    ax1 = fig.add_subplot(gs[1, 1])
    pltsds.plot_superdrops_2dmotion(
        sddata,
        ids2plot,
        colors=[cmap, values],
        fig=fig,
        ax=ax1,
    )
    ax1.set_aspect("equal")

    cax = fig.add_subplot(gs[0, :])
    norm = plt.Normalize(vmin=np.nanmin(values), vmax=np.nanmax(values))
    fig.colorbar(
        ScalarMappable(norm=norm, cmap=cmap),
        cax=cax,
        label="time /min",
        orientation="horizontal",
    )

    fig.tight_layout()

    return fig, [ax0, ax1, cax]


### ---------------------------------------------------- ###

### read in constants and intial setup from setup .txt file
config = pysetuptxt.get_config(setupfile, nattrs=3, isprint=True)
consts = pysetuptxt.get_consts(setupfile, isprint=True)
gbxs = pygbxsdat.get_gridboxes(gridfile, consts["COORD0"], isprint=True)

# read in output Xarray data
time = pyzarr.get_time(dataset)
sddata = pyzarr.get_supers(dataset, consts)
maxnsupers = pyzarr.get_totnsupers(dataset)

fig, axs = thermo3d_validation_plot(time, sddata, maxnsupers)
savename = savedir / Path("thermo3d_validation.png")
fig.savefig(savename, dpi=400, bbox_inches="tight", facecolor="w", format="png")
print("Figure .png saved as: " + str(savename))
plt.show()
