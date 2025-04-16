"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: plot_cond0d.py
Project: validations
Created Date: Thursday 20th March 2025
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
Script plots results from condensation example
"""

import argparse
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
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

from plotssrc import as2017fig
from pySD.sdmout_src import pyzarr, pysetuptxt, pygbxsdat, sdtracing


### ---------------- plotting functions ---------------- ###
def displacement(time, w_avg, thalf):
    """displacement z given velocity, w, is sinusoidal
    profile: w = w_avg * pi/2 * np.sin(np.pi * t/thalf)
    where wmax = pi/2*w_avg and tauhalf = thalf/pi."""

    zmax = w_avg / 2 * thalf
    z = zmax * (1 - np.cos(np.pi * time / thalf))
    return z


def cond0d_validation_plot(time, gbxs, thermo, sddata, w_avg, tau_half):
    fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(5, 16))

    supersat = thermo.supersaturation()
    zprof = displacement(time, w_avg, tau_half)

    volume = (
        gbxs["gbxvols"][0, 0, 0] * 1e6
    )  # assuming all gbxs have same volume [/cm^3]
    xi0 = np.where(
        sddata["sdgbxindex"][0] == 0, sddata["xi"][0], 0
    )  # 0th gbx's initial droplet xi
    numconc = np.sum(xi0) / volume  # initial number concentation in volume

    sdid2plot = random.choice(sddata.sdId[0])  # plot one of the initial superdroplets
    attrs = ["radius", "xi", "msol"]
    sd2plot = sdtracing.attributes_for1superdroplet(sddata, sdid2plot, attrs)

    wlab = "<w> = {:.1f}".format(w_avg * 100) + "cm s$^{-1}$"
    as2017fig.condensation_validation_subplots(
        axs, time, sd2plot["radius"], supersat[:, 0, 0, 0], zprof, lwdth=2, lab=wlab
    )

    as2017fig.plot_kohlercurve_with_criticalpoints(
        axs[1],
        sd2plot["radius"],
        sd2plot["msol"][0],
        thermo.temp[0, 0, 0, 0],
        sddata.IONIC,
        sddata.MR_SOL,
    )

    textlab = (
        "N = "
        + str(numconc)
        + "cm$^{-3}$\n"
        + "r$_{dry}$ = "
        + "{:.2g}\u03BCm\n".format(sd2plot["radius"][0])
    )
    axs[0].legend(loc="lower right", fontsize=10)
    axs[1].legend(loc="upper left")
    axs[0].text(0.03, 0.85, textlab, transform=axs[0].transAxes)

    axs[0].set_xlim([-1, 1])
    for ax in axs[1:]:
        ax.set_xlim([0.125, 10])
        ax.set_xscale("log")
    axs[0].set_ylim([0, 150])
    axs[1].set_ylim([-1, 1])
    axs[2].set_ylim([5, 75])

    fig.tight_layout()

    return fig, axs


### ---------------------------------------------------- ###

### read in constants and intial setup from setup .txt file
config = pysetuptxt.get_config(setupfile, nattrs=3, isprint=True)
consts = pysetuptxt.get_consts(setupfile, isprint=True)
gbxs = pygbxsdat.get_gridboxes(gridfile, consts["COORD0"], isprint=True)

# read in output Xarray data
time = pyzarr.get_time(dataset).secs
sddata = pyzarr.get_supers(dataset, consts)
thermo = pyzarr.get_thermodata(dataset, config["ntime"], gbxs["ndims"], consts)

fig, axs = cond0d_validation_plot(
    time, gbxs, thermo, sddata, config["W_avg"], config["TAU_half"]
)
savename = savedir / Path("cond0d_validation.png")
fig.savefig(savename, dpi=400, bbox_inches="tight", facecolor="w", format="png")
print("Figure .png saved as: " + str(savename))
plt.show()
