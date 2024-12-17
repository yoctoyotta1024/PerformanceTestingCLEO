"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: quickplots.py
Project: plotting
Created Date: Monday 9th December 2024
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Monday 9th December 2024
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
Script for plotting scaling results from zarr xarray datasets for kokkos profiling data.
Note: standard data format assumed.
"""

# %%
import argparse
import xarray as xr
import numpy as np
from pathlib import Path
import sys
from typing import Optional

path2src = Path(__file__).resolve().parent.parent.parent / "src"
sys.path.append(str(path2src))  # for imports for input files generation
from plotting import helperfuncs as hfuncs

# e.g. ipykernel_launcher.py [path2builds] [executable]
parser = argparse.ArgumentParser()
parser.add_argument(
    "--path2builds",
    type=Path,
    help="Absolute path to builds",
    default="/work/bm1183/m300950/performance_testing_cleo/builds/",
)
parser.add_argument(
    "--executable",
    type=str,
    choices=["colls0d"],
    help="Executable name, e.g. colls0d",
    default="colls0d",
)
args, unknown = parser.parse_known_args()
path2builds = args.path2builds
executable = args.executable

nsupers_per_gbx = [1, 16]

lstyles = hfuncs.buildtype_lstyles
markers = hfuncs.buildtype_markers

savedir = Path("/home/m/m300950/performance_testing_cleo/plots/")

skip = {
    1: 3,
    16: 1,
}


# %% funtion definitions for generic helper functions
def line_of_best_fit(
    x: np.ndarray,
    y: np.ndarray,
    skip: Optional[int] = 0,
    logaxs: Optional[bool] = False,
):
    deg = 1
    x = x[skip:]
    y = y[skip:]
    if logaxs:
        x = np.log10(x)
        y = np.log10(y)
    slope, intercept = np.polyfit(x, y, deg)
    yfit = slope * x + intercept
    if logaxs:
        yfit = 10**yfit
        x = 10**x
    return x, yfit, slope, intercept


# %% funtion definitions for kernel timer plots
def plot_overall_wallclock_scaling(datasets: dict):
    fig, axs = hfuncs.subplots(figsize=(12, 8), nrows=1, logx=True, logy=True)
    c1 = "k"
    a = 0
    for lab, data in datasets.items():
        x = data.attrs["nsupers"] * data.ngbxs
        y = data.summary[:, 0, 0]
        lq, uq = data.summary[:, 2, 0], data.summary[:, 3, 0]
        slab = None
        if a == 0:
            slab = "IQR"
        hfuncs.add_shading(axs, x, lq, uq, c1, lstyles[lab], label=slab)

        axs.plot(
            x,
            y,
            color=c1,
            marker=markers[lab],
            linestyle=lstyles[lab],
            label=lab,
        )

        # c2 = "purple"
        # xfit, yfit, m, c = line_of_best_fit(x, y, skip=skip[nsupers], logaxs=True)
        # axs.plot(xfit, yfit, color=c2, linestyle=lstyles[lab], label=f"scaling={m:.2f}")
        a += 1
    axs.legend()
    axs.set_title("Entire Program")
    axs.set_ylabel("Wall Clock Time /s")
    axs.set_xlabel("Total Superdroplets in Domain")

    return fig, axs


def plot_simple_wallclock_scaling(datasets: dict):
    fig, axs = hfuncs.subplots(
        figsize=(12, 20), nrows=3, sharex=True, logx=True, logy=True
    )
    c1 = "k"
    a = 0
    for lab, data in datasets.items():
        x = data.attrs["nsupers"] * data.ngbxs
        y = data.summary[:, 0, 0]
        lq, uq = data.summary[:, 2, 0], data.summary[:, 3, 0]
        slab = None
        if a == 0:
            slab = "IQR"
        hfuncs.add_shading(axs[0], x, lq, uq, c1, lstyles[lab], label=slab)

        axs[0].plot(
            x,
            y,
            color=c1,
            marker=markers[lab],
            linestyle=lstyles[lab],
            label=lab,
        )

        # c2 = "purple"
        # xfit, yfit, m, c = line_of_best_fit(x, y, skip=skip[nsupers], logaxs=True)
        # axs[0].plot(xfit, yfit, color=c2, linestyle=lstyles[lab], label=f"scaling={m:.2f}")
        a += 1
    axs[0].set_title("Entire Program")

    for lab, data in datasets.items():
        x = data.attrs["nsupers"] * data.ngbxs
        y = data.runcleo[:, 0, 0]
        lq, uq = data.runcleo[:, 2, 0], data.runcleo[:, 3, 0]
        slab = None
        if a == 0:
            slab = "IQR"
        hfuncs.add_shading(axs[1], x, lq, uq, c1, lstyles[lab], label=slab)

        axs[1].plot(
            x,
            y,
            color=c1,
            marker=markers[lab],
            linestyle=lstyles[lab],
            label=lab,
        )

        # c2 = "purple"
        # xfit, yfit, m, c = line_of_best_fit(x, y, skip=skip[nsupers], logaxs=True)
        # axs[1].plot(xfit, yfit, color=c2, linestyle=lstyles[lab], label=f"scaling={m:.2f}")
        a += 1
    axs[1].set_title("RunCLEO")

    for lab, data in datasets.items():
        x = data.attrs["nsupers"] * data.ngbxs
        y = data.timestep[:, 0, 0]
        lq, uq = data.timestep[:, 2, 0], data.timestep[:, 3, 0]
        slab = None
        if a == 0:
            slab = "IQR"
        hfuncs.add_shading(axs[2], x, lq, uq, c1, lstyles[lab], label=slab)

        axs[2].plot(
            x,
            y,
            color=c1,
            marker=markers[lab],
            linestyle=lstyles[lab],
            label=lab,
        )

        # c2 = "purple"
        # xfit, yfit, m, c = line_of_best_fit(x, y, skip=skip[nsupers], logaxs=True)
        # axs[1].plot(xfit, yfit, color=c2, linestyle=lstyles[lab], label=f"scaling={m:.2f}")
        a += 1
    axs[2].set_title("Timestepping")

    for ax in axs:
        ax.set_ylabel("Wall Clock Time /s")

    axs[0].legend()
    axs[-1].set_xlabel("Total Superdroplets in Domain")

    return fig, axs


def plot_simple_wallclock_timeinkernels_scaling(datasets: dict):
    fig, axs = hfuncs.subplots(figsize=(12, 20), nrows=3, ncols=1, sharex=True)
    c1 = "k"
    for lab, data in datasets.items():
        x = data.attrs["nsupers"] * data.ngbxs
        y = data.summary[:, 0, 3]
        axs[0].plot(
            x,
            y,
            color=c1,
            marker=markers[lab],
            linestyle=lstyles[lab],
            label=lab,
        )
        lq, uq = data.summary[:, 2, 3], data.summary[:, 3, 3]
        hfuncs.add_shading(axs[0], x, lq, uq, c1, lstyles[lab])
        axs[0].set_ylabel("% of Total Wall Clock Time in Kernels")
    axs[0].legend()

    c1 = "tab:blue"
    a = 0
    for lab, data in datasets.items():
        x = data.attrs["nsupers"] * data.ngbxs
        y = data.summary[:, 0, 1]
        label = lab
        if a == 0:
            label = lab + " in kernels"
        axs[1].plot(
            x,
            y,
            color=c1,
            marker=markers[lab],
            linestyle=lstyles[lab],
            label=label,
        )
        lq, uq = data.summary[:, 2, 1], data.summary[:, 3, 1]
        hfuncs.add_shading(axs[1], x, lq, uq, c1, lstyles[lab])
        a += 1

    c2 = "tab:green"
    a = 0
    for lab, data in datasets.items():
        x = data.attrs["nsupers"] * data.ngbxs
        y = data.summary[:, 0, 2]
        label = lab
        if a == 0:
            label = lab + " outside kernels"
        axs[1].plot(
            x,
            y,
            color=c2,
            marker=markers[lab],
            linestyle=lstyles[lab],
            label=label,
        )
        lq, uq = data.summary[:, 2, 2], data.summary[:, 3, 2]
        hfuncs.add_shading(axs[1], x, lq, uq, c2, lstyles[lab])
        a += 1

    axs[1].set_yscale("log")
    axs[1].set_ylabel("Total Wall Clock Time /s")
    axs[1].legend()

    c1 = "k"
    for lab, data in datasets.items():
        x = data.attrs["nsupers"] * data.ngbxs
        y = data.summary[:, 0, 4]
        axs[2].plot(
            x,
            y,
            color=c1,
            marker=markers[lab],
            linestyle=lstyles[lab],
            label=lab,
        )
        lq, uq = data.summary[:, 2, 4], data.summary[:, 3, 4]
        hfuncs.add_shading(axs[2], x, lq, uq, c1, lstyles[lab])
        axs[2].set_ylabel("Total Number of Calls to Kernels")
    axs[2].legend()

    axs[0].set_xscale("log")
    axs[-1].set_xlabel("Total Superdroplets in Domain")
    return fig, axs


def plot_wallclock_decomposition_scaling(datasets: dict):
    fig, axs = hfuncs.subplots(
        figsize=(12, 20), nrows=3, ncols=1, sharex=True, logx=True, logy=True
    )

    vars = ["runcleo", "init", "timestep"]
    colors = ["black", "darkviolet", "green"]
    v = 0
    for v, var in enumerate(vars):
        a = 0
        for lab, data in datasets.items():
            x = data.attrs["nsupers"] * data.ngbxs
            y = data[var][:, 0, 0]
            lq, uq = data[var][:, 2, 0], data[var][:, 3, 0]
            label = lab
            if a == 0:
                label = lab + f" in {var}"
            axs[0].plot(
                x,
                y,
                color=colors[v],
                marker=markers[lab],
                linestyle=lstyles[lab],
                label=label,
            )
            hfuncs.add_shading(axs[0], x, lq, uq, colors[v], lstyles[lab])
            a += 1
    axs[0].set_title("total runtime")

    vars = ["init_gbxs", "init_supers"]
    colors = ["mediumorchid", "hotpink"]
    for v, var in enumerate(vars):
        a = 0
        for lab, data in datasets.items():
            x = data.attrs["nsupers"] * data.ngbxs
            y = data[var][:, 0, 0]
            lq, uq = data[var][:, 2, 0], data[var][:, 3, 0]
            label = lab
            if a == 0:
                label = lab + f" in {var}"
            axs[1].plot(
                x,
                y,
                color=colors[v],
                marker=markers[lab],
                linestyle=lstyles[lab],
                label=label,
            )
            hfuncs.add_shading(axs[1], x, lq, uq, colors[v], lstyles[lab])
            a += 1
    axs[1].set_title("initialisation")

    vars = [
        "timestep_coupldyn",
        "timestep_sdm",
        "timestep_sdm_microphysics",
        "timestep_sdm_movement",
    ]
    colors = ["mediumseagreen", "aquamarine", "deepskyblue", "cornflowerblue"]
    for v, var in enumerate(vars):
        a = 0
        for lab, data in datasets.items():
            x = data.attrs["nsupers"] * data.ngbxs
            y = data[var][:, 0, 0]
            lq, uq = data[var][:, 2, 0], data[var][:, 3, 0]
            label = lab
            if a == 0:
                label = lab + f" in {var}"
            axs[2].plot(
                x,
                y,
                color=colors[v],
                marker=markers[lab],
                linestyle=lstyles[lab],
                label=label,
            )
            hfuncs.add_shading(axs[2], x, lq, uq, colors[v], lstyles[lab])
            a += 1
    axs[2].set_title("timestepping")

    for ax in axs:
        ax.legend()
        ax.set_ylabel("Wall Clock Time /s")
    axs[-1].set_xlabel("Total Superdroplets in Domain")

    return fig, axs


# %% funtion definitions for memory consumption plots
def plot_simple_memory_scaling(datasets: xr.Dataset):
    fig, axs = hfuncs.subplots(
        figsize=(12, 15), nrows=2, ncols=1, sharex=True, logx=True
    )

    c1 = "k"
    for lab, data in datasets.items():
        yarr = data.host_high_water_memory_consumption / 1000  # [MB]
        x = data.attrs["nsupers"] * data.ngbxs
        y = yarr[:, 0]
        axs[0].plot(
            x,
            y,
            color=c1,
            marker=markers[lab],
            linestyle=lstyles[lab],
            label=lab,
        )
        lq, uq = yarr[:, 2], yarr[:, 3]
        hfuncs.add_shading(axs[0], x, lq, uq, c1, lstyles[lab])
    axs[0].legend()
    axs[0].set_ylabel("host high water memory consumption / MB")

    spaces = data.spaces.values[0:2]
    colors = ["tab:orange", "tab:green"]
    for i in range(2):
        a = 0
        for lab, data in datasets.items():
            x = data.attrs["nsupers"] * data.ngbxs
            yarr = data.max_memory_allocation / 1000  # [MB]
            y = yarr[:, 0, i]
            label = lab
            if a == 0:
                label = lab + f" in {spaces[i]}"
            axs[1].plot(
                x,
                y,
                color=colors[i],
                marker=markers[lab],
                linestyle=lstyles[lab],
                label=label,
            )
            lq, uq = yarr[:, 2, i], yarr[:, 3, i]
            hfuncs.add_shading(axs[1], x, lq, uq, c1, lstyles[lab])
            a += 1
    axs[1].legend()
    axs[1].set_ylabel("max memory allocation / MB")

    axs[-1].set_xlabel("Total Superdroplets in Domain")
    return fig, axs


# % mkake plots for each nsupers
for nsupers in nsupers_per_gbx:
    # %% load data
    serial = hfuncs.open_kerneltimer_dataset(path2builds, "serial", executable, nsupers)
    openmp = hfuncs.open_kerneltimer_dataset(path2builds, "openmp", executable, nsupers)
    threads = hfuncs.open_kerneltimer_dataset(
        path2builds, "threads", executable, nsupers
    )
    cuda = hfuncs.open_kerneltimer_dataset(path2builds, "cuda", executable, nsupers)
    datasets_time = {
        "serial": serial,
        "openmp": openmp,
        "threads": threads,
        "cuda": cuda,
    }
    # %%
    fig, axs = plot_overall_wallclock_scaling(datasets_time)
    savename = savedir / f"total_wallclock_nsupers{nsupers}.png"
    hfuncs.savefig(savename)
    # %%
    fig, axs = plot_simple_wallclock_scaling(datasets_time)
    savename = savedir / f"simple_wallclock_nsupers{nsupers}.png"
    hfuncs.savefig(savename)
    # %%
    fig, axs = plot_simple_wallclock_timeinkernels_scaling(datasets_time)
    savename = savedir / f"wallclock_inkernels_nsupers{nsupers}.png"
    hfuncs.savefig(savename)
    # %%
    fig, axs = plot_wallclock_decomposition_scaling(datasets_time)
    savename = savedir / f"wallclock_decomposition_nsupers{nsupers}.png"
    hfuncs.savefig(savename)

    # %%
    serial = hfuncs.open_spacetimestack_dataset(
        path2builds, "serial", executable, nsupers
    )
    openmp = hfuncs.open_spacetimestack_dataset(
        path2builds, "openmp", executable, nsupers
    )
    cuda = hfuncs.open_spacetimestack_dataset(path2builds, "cuda", executable, nsupers)
    threads = hfuncs.open_spacetimestack_dataset(
        path2builds, "threads", executable, nsupers
    )
    datasets_mem = {
        "serial": serial,
        "openmp": openmp,
        "cuda": cuda,
        "threads": threads,
    }

    # %%
    fig, axs = plot_simple_memory_scaling(datasets_mem)
    savename = savedir / f"memory_consumption_nsupers{nsupers}.png"
    hfuncs.savefig(savename)

    # %%
