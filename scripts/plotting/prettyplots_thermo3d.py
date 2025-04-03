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
import awkward as ak
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LogNorm
from matplotlib.gridspec import GridSpec
from pathlib import Path
from typing import Optional

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
### --------- plotting functions --------- ###
def save_figure(savename: Path, dpi: Optional[int] = 128):
    plt.savefig(savename, dpi=dpi, bbox_inches="tight")
    print(f"figure saved as {str(savename)}")


def plot_superdroplet_distribution(fig, ax2, gbxs, sddata):
    t = 0  # time slice to plot
    vol = gbxs["gbxvols"][0, 0, 0] * 1e6  # [cm^3]
    gbxindex = 0  # gridbox to plot

    def get_attributes(sddata, attrs, t, gbxindex):
        vars = []
        for attr in attrs:
            var = np.where(sddata.sdgbxindex[t] == gbxindex, sddata[attr][t], np.nan)
            vars.append(var[~np.isnan(var)])
        return vars

    radius, xi, dss = get_attributes(
        sddata, ["radius", "xi", "sdgbxindex"], t, gbxindex
    )

    ax2.scatter(
        radius,
        xi / vol,
        marker=".",
        color="thistle",
        label="superdroplets",
        zorder=-1,
    )

    nbins = int(len(radius))
    hedgs = np.linspace(np.log10(5e-3), np.log10(1), nbins + 1)  # edges to bins
    wghts = xi / vol  # [cm^-3]
    hist, hedgs = np.histogram(
        np.log10(radius), bins=hedgs, weights=wghts, density=None
    )
    hcens = (hedgs[1:] + hedgs[:-1]) / 2
    ax2.step(10**hcens, hist, where="mid", color="dimgrey", label="binned distribution")

    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlim([5e-3, 1])
    ax2.set_xlabel("radius /\u03BCm")
    ax2.set_ylabel("aerosol number concentration / cm$^{-3}$")
    ax2.legend()
    ax2.spines[["right", "top"]].set_visible(False)


def plot_thermodynamics_conditions(fig, ax0, ax1, ax3, cax, gbxs, thermo):
    t = 0  # time slice to plot
    y = 0  # y slice to plot
    x = 0  # x slice to plot (for 1-D profiles)
    cmap = "BuGn"  # for winds
    cmap_norm = plt.Normalize(vmin=0.0, vmax=1.0)

    def three_xticks(var):
        mid = (np.amin(var) + np.amax(var)) / 2
        return [np.amin(var), mid, np.amax(var)]

    ## plot 1-D profiles of temperature, water vapour and supersaturation
    temp = thermo.temp[t, y, x, :]  # K
    ax0.plot(temp, gbxs["zfull"], color="k")
    ax0.set_xlabel("temperature /K")
    ax0.set_xticks(three_xticks(temp))
    ax0.set_xticklabels(["{:.2f}".format(x) for x in three_xticks(temp)])

    qvap = thermo.qvap[t, y, x, :]  # g/Kg
    ax1.plot(qvap, gbxs["zfull"], color="darkblue")
    ax1.set_xlabel("q$_{v}$ /g Kg$^{-1}$", color="darkblue")
    ax1.set_xticks(three_xticks(qvap))
    ax1.set_xticklabels(["{:.2f}".format(x) for x in three_xticks(qvap)])

    ax1b = ax1.twiny()
    supersat = thermo.supersaturation()[t, y, x, :] * 100  # %
    ax1b.plot(supersat, gbxs["zfull"], color="darkorchid")
    ax1b.set_xlabel("% supersaturation", color="darkorchid")
    ax1b.set_xticks(three_xticks(supersat))
    ax1b.set_xticklabels(["{:.2f}".format(x) for x in three_xticks(supersat)])

    for ax in [ax0, ax1]:
        ax.set_ylabel("z /m")
        ax.hlines(
            750,
            ax.get_xlim()[0],
            ax.get_xlim()[-1],
            color="dimgrey",
            linewidth=0.5,
            linestyle="--",
        )
        ax.spines[["right", "left", "top"]].set_visible(False)
        ax.set_ylim([0, 1500])
    ax1b.spines[["right", "left", "bottom"]].set_visible(False)

    ### plot 2-D wind field
    wvel = winds.wvel[t, y, :, :]  # m/s
    uvel = winds.uvel[t, y, :, :]  # m/s
    magnitude = np.sqrt(wvel**2 + uvel**2)
    ax3.pcolormesh(gbxs["xxh"], gbxs["zzh"], magnitude, cmap=cmap, norm=cmap_norm)
    ax3.quiver(gbxs["xxf"], gbxs["zzf"], uvel, wvel, pivot="mid", width=0.001, scale=15)

    fig.colorbar(
        ScalarMappable(norm=cmap_norm, cmap=cmap),
        cax=cax,
        label="|wind velocity| /m s${-1}$ ",
    )

    ax3.set_xlabel("x /m")
    ax3.set_ylabel("z /m")
    ax3.set_aspect("equal")
    ax3.set_xlim([0, 6000])
    ax3.set_ylim([0, 1500])
    ax3.spines[["right", "left"]].set_visible(False)


def plot_initial_conditions(gbxs, thermo, sddata):
    fig = plt.figure(figsize=(12, 8))
    gs = GridSpec(2, 45, figure=fig, height_ratios=[3, 2])
    ax0 = fig.add_subplot(gs[0, :11])
    ax1 = fig.add_subplot(gs[0, 15:26])
    ax2 = fig.add_subplot(gs[0, 30:])
    ax3 = fig.add_subplot(gs[1, :-1])
    cax = fig.add_subplot(gs[1, -1])

    plot_thermodynamics_conditions(fig, ax0, ax1, ax3, cax, gbxs, thermo)
    plot_superdroplet_distribution(fig, ax2, gbxs, sddata)

    return fig, [ax0, ax1, ax2, ax3, cax]


def superdroplet_data_within_coordinate_ranges(
    time, sddata, attrs, times2select, coord1_range, coord2_range
):
    def define_variable_subset(var, minmax):
        booleans = np.where(var >= minmax[0], True, False)
        booleans = np.where(var < minmax[1], booleans, False)
        return booleans

    def variable_in_ranges(var, subsets):
        for subset in subsets:
            var = np.where(subset, var, np.nan)
        return var[~np.isnan(var)]

    tslice = [
        int(np.argmin(abs(t - time.mins))) for t in times2select
    ]  # turn time into time index
    set1 = define_variable_subset(sddata.coord1[tslice], coord1_range)
    set2 = define_variable_subset(sddata.coord2[tslice], coord2_range)

    selected_data = {}
    for attr in attrs:
        selected_data[attr] = variable_in_ranges(sddata[attr][tslice], [set2, set1])

    return selected_data


def random_sample_superdroplet_data(sddata, nsample, attrs, times2select):
    sdId = sddata["sdId"]
    sds2sample = np.random.choice(sdId[0], size=nsample, replace=False)

    data_sample = {}
    for attr in attrs:
        data_sample[attr] = []

    for t in range(len(times2select)):
        sdid_sample, idxs, _ = np.intersect1d(
            sdId[t], sds2sample, assume_unique=True, return_indices=True
        )
        idxs = ak.to_numpy(idxs).astype("int32")

        tsample = {}
        for attr in attrs:
            tsample[attr] = sddata[attr][t][idxs]

        if len(sdid_sample) != nsample:
            missing_sds = np.setdiff1d(sds2sample, sdid_sample, assume_unique=True)
            missing_idxs = np.searchsorted(sdid_sample, missing_sds)
            for attr in attrs:
                tsample[attr] = np.insert(tsample[attr], missing_idxs, np.nan)

        for attr in attrs:
            data_sample[attr].append(tsample[attr])

    for attr in attrs:
        data_sample[attr] = np.asarray(data_sample[attr])

    return data_sample


def plot_superdroplet_sample_tracing(time, sample, coord1_range):
    fig = plt.figure(figsize=(12, 6))
    gs = GridSpec(1, 2, figure=fig, width_ratios=[3, 2])
    ax0 = fig.add_subplot(gs[0, 0])
    ax1 = fig.add_subplot(gs[0, 1])

    cmap = "YlOrBr"  # for superdroplet radii
    cmap_norm = plt.Normalize(vmin=-1000, vmax=6000)
    c = np.repeat(time.secs, (sample["radius"].shape)[1])

    ax0.scatter(
        sample["coord1"],
        sample["coord3"],
        c=c,
        cmap=cmap,
        norm=cmap_norm,
        marker=".",
        s=np.log10(sample["radius"] * 1e9),
    )
    ax0.set_aspect("equal")
    ax0.set_xlabel("x /m")
    ax0.set_ylabel("z /m")
    ax0.set_aspect("equal")
    ax0.set_xlim([coord1_range[0], coord1_range[1]])
    ax0.set_ylim([0, 1500])
    ax0.spines[["left", "right"]].set_visible(False)

    ax1.scatter(
        sample["radius"] / 1e3,
        sample["coord3"],
        c=c,
        cmap=cmap,
        norm=cmap_norm,
        marker=".",
        s=10,
    )
    ax1.set_ylabel("z /m")
    ax1.set_xlabel("radius /mm")
    ax1.set_ylim([0, 1500])
    ax1.set_xscale("log")
    ax1.spines[["right", "top"]].set_visible(False)

    fig.tight_layout()

    return fig, [ax0, ax1]


def plot_superdroplet_sample_tracing_version2(sample, coord1_range):
    fig = plt.figure(figsize=(7, 6))
    gs = GridSpec(1, 2, figure=fig, width_ratios=[21, 1])
    ax0 = fig.add_subplot(gs[0, 0])
    cax = fig.add_subplot(gs[0, 1])

    cmap = "PuBuGn"  # for superdroplet radii
    cmap_norm = LogNorm(vmin=1e-2, vmax=1e2)

    ax0.scatter(
        sample["coord1"],
        sample["coord3"],
        c=sample["radius"],
        marker=".",
        s=np.log10(sample["radius"] * 1e9) / 10,
        cmap=cmap,
        norm=cmap_norm,
    )
    ax0.set_aspect("equal")
    ax0.set_xlabel("x /m")
    ax0.set_ylabel("z /m")
    ax0.set_aspect("equal")
    ax0.set_xlim([coord1_range[0], coord1_range[1]])
    ax0.set_ylim([0, 1500])
    ax0.spines[["left", "right"]].set_visible(False)

    fig.colorbar(
        ScalarMappable(norm=cmap_norm, cmap=cmap),
        cax=cax,
        label=" radius /\u03BCm",
    )

    fig.tight_layout()

    return fig, [ax0, cax]


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
thermo, winds = pyzarr.get_thermodata(
    dataset, config["ntime"], gbxs["ndims"], consts, getwinds=True
)
# %%
### save figure for initial conditions
fig, axs = plot_initial_conditions(gbxs, thermo, sddata)
savename = path4plots / Path(
    f"thermo3d_initial_conditions_ngbxs{ngbxs}_nsupers{nsupers}.png"
)
save_figure(savename)

# %%
times2plot = time.mins
nsample = 500
coord1_range = [1500, 3000]
coord2_range = [gbxs["yhalf"][0], gbxs["yhalf"][1]]

attrs4coordrange = ["sdId", "radius", "coord1", "coord3"]
selected_sddata = superdroplet_data_within_coordinate_ranges(
    time, sddata, attrs4coordrange, times2plot, coord1_range, coord2_range
)
attrs4sample = ["radius", "coord1", "coord3"]
sample = random_sample_superdroplet_data(
    selected_sddata, nsample, attrs4sample, times2plot
)

# %%
fig, axs = plot_superdroplet_sample_tracing(time, sample, coord1_range)
savename = path4plots / Path(
    f"thermo3d_superdroplet_tracing_ngbxs{ngbxs}_nsupers{nsupers}.png"
)
save_figure(savename)

# %%
fig, axs = plot_superdroplet_sample_tracing_version2(sample, coord1_range)
savename = path4plots / Path(
    f"thermo3d_superdroplet_tracing_version2_ngbxs{ngbxs}_nsupers{nsupers}.png"
)
save_figure(savename)
# %%
