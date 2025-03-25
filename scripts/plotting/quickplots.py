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
import matplotlib.pyplot as plt

path2src = Path(__file__).resolve().parent.parent.parent / "src"
sys.path.append(str(path2src))  # for helperfuncs module
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
    choices=["colls0d", "cond0d", "motion2d", "thermo3d"],
    help="Executable name, e.g. colls0d",
    default="colls0d",
)
args, unknown = parser.parse_known_args()
path2builds = args.path2builds
executable = args.executable

buildtypes = ["serial", "openmp", "cuda", "threads"]

ensembletype = "gbxs"
fixed_ensemb_vals = [128]

lstyles = hfuncs.buildtype_lstyles
markers = hfuncs.buildtype_markers

savedir = Path("/home/m/m300950/performance_testing_cleo/plots/")

skip = 1


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
def domain_totnsupers(data):
    try:
        x = data.attrs["nsupers"] * data.ngbxs
    except KeyError:
        x = data.attrs["ngbxs"] * data.nsupers
    return x


def plot_overall_wallclock_scaling(datasets: dict):
    fig, axs = hfuncs.subplots(figsize=(12, 8), logx=True, logy=True)

    ncolors = 4  # allows n different values for threads
    colors = plt.cm.cool(np.linspace(0, 1, ncolors))

    a = 0
    for lab, data in datasets.items():
        c = 0
        for nthreads in data.nthreads:
            x = domain_totnsupers(data)
            summary = data.summary.sel(nthreads=nthreads)
            y = summary[:, 0, 0]
            lq, uq = summary[:, 2, 0], summary[:, 3, 0]
            slab = None
            if a == 0:
                slab = "IQR"
            hfuncs.add_shading(axs, x, lq, uq, colors[c], lstyles[lab], label=slab)

            llab = None
            if nthreads == data.nthreads[0]:
                llab = lab + f", nthreads={nthreads.values}"
            print(f"colour_index={c}, threads={nthreads.values}")
            axs.plot(
                x,
                y,
                color=colors[c],
                marker=markers[lab],
                linestyle=lstyles[lab],
                label=llab,
            )
            c += 1
            # c2 = "red"
            # xfit, yfit, m, _ = line_of_best_fit(x, y, skip=skip, logaxs=True)
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
        for nthreads in data.nthreads:
            x = domain_totnsupers(data)
            summary = data.summary.sel(nthreads=nthreads)
            y = summary[:, 0, 0]
            lq, uq = summary[:, 2, 0], summary[:, 3, 0]
            slab = None
            if a == 0:
                slab = "IQR"
            hfuncs.add_shading(axs[0], x, lq, uq, c1, lstyles[lab], label=slab)

            llab = None
            if nthreads == data.nthreads[0]:
                llab = lab

            axs[0].plot(
                x,
                y,
                color=c1,
                marker=markers[lab],
                linestyle=lstyles[lab],
                label=llab,
            )

            # c2 = "purple"
            # xfit, yfit, m, c = line_of_best_fit(x, y, skip=skip, logaxs=True)
            # axs[0].plot(xfit, yfit, color=c2, linestyle=lstyles[lab], label=f"scaling={m:.2f}")

            a += 1
    axs[0].set_title("Entire Program")

    for lab, data in datasets.items():
        for nthreads in data.nthreads:
            x = domain_totnsupers(data)
            runcleo = data.runcleo.sel(nthreads=nthreads)
            y = runcleo[:, 0, 0]
            lq, uq = runcleo[:, 2, 0], runcleo[:, 3, 0]
            slab = None
            if a == 0:
                slab = "IQR"
            hfuncs.add_shading(axs[1], x, lq, uq, c1, lstyles[lab], label=slab)

            llab = None
            if nthreads == data.nthreads[0]:
                llab = lab

            axs[1].plot(
                x,
                y,
                color=c1,
                marker=markers[lab],
                linestyle=lstyles[lab],
                label=llab,
            )

            # c2 = "purple"
            # xfit, yfit, m, c = line_of_best_fit(x, y, skip=skip, logaxs=True)
            # axs[1].plot(xfit, yfit, color=c2, linestyle=lstyles[lab], label=f"scaling={m:.2f}")

            a += 1
    axs[1].set_title("RunCLEO")

    for lab, data in datasets.items():
        for nthreads in data.nthreads:
            x = domain_totnsupers(data)
            timestep = data.timestep.sel(nthreads=nthreads)
            y = timestep[:, 0, 0]
            lq, uq = timestep[:, 2, 0], timestep[:, 3, 0]
            slab = None
            if a == 0:
                slab = "IQR"
            hfuncs.add_shading(axs[2], x, lq, uq, c1, lstyles[lab], label=slab)

            llab = None
            if nthreads == data.nthreads[0]:
                llab = lab

            axs[2].plot(
                x,
                y,
                color=c1,
                marker=markers[lab],
                linestyle=lstyles[lab],
                label=llab,
            )

            # c2 = "purple"
            # xfit, yfit, m, c = line_of_best_fit(x, y, skip=skip, logaxs=True)
            # axs[2].plot(xfit, yfit, color=c2, linestyle=lstyles[lab], label=f"scaling={m:.2f}")

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
        for nthreads in data.nthreads:
            x = domain_totnsupers(data)
            summary = data.summary.sel(nthreads=nthreads)
            y = summary[:, 0, 3]
            lq, uq = summary[:, 2, 3], summary[:, 3, 3]

            llab = None
            if nthreads == data.nthreads[0]:
                llab = lab
            axs[0].plot(
                x,
                y,
                color=c1,
                marker=markers[lab],
                linestyle=lstyles[lab],
                label=llab,
            )
            hfuncs.add_shading(axs[0], x, lq, uq, c1, lstyles[lab])
    axs[0].set_ylabel("% of Total Wall Clock Time in Kernels")
    axs[0].legend()

    c1 = "tab:blue"
    a = 0
    for lab, data in datasets.items():
        for nthreads in data.nthreads:
            x = domain_totnsupers(data)
            summary = data.summary.sel(nthreads=nthreads)
            y = summary[:, 0, 1]
            lq, uq = summary[:, 2, 1], summary[:, 3, 1]

            llab = None
            if nthreads == data.nthreads[0]:
                llab = lab
                if a == 0:
                    llab += " in kernels"

            axs[1].plot(
                x,
                y,
                color=c1,
                marker=markers[lab],
                linestyle=lstyles[lab],
                label=llab,
            )
            hfuncs.add_shading(axs[1], x, lq, uq, c1, lstyles[lab])
            a += 1

    c2 = "tab:green"
    a = 0
    for lab, data in datasets.items():
        for nthreads in data.nthreads:
            x = domain_totnsupers(data)
            summary = data.summary.sel(nthreads=nthreads)
            y = summary[:, 0, 2]
            lq, uq = summary[:, 2, 2], summary[:, 3, 2]

            llab = None
            if nthreads == data.nthreads[0]:
                llab = lab
                if a == 0:
                    llab += " outside kernels"

            axs[1].plot(
                x,
                y,
                color=c2,
                marker=markers[lab],
                linestyle=lstyles[lab],
                label=llab,
            )
            hfuncs.add_shading(axs[1], x, lq, uq, c2, lstyles[lab])
            a += 1

    axs[1].set_yscale("log")
    axs[1].set_ylabel("Total Wall Clock Time /s")
    axs[1].legend()

    c1 = "k"
    for lab, data in datasets.items():
        for nthreads in data.nthreads:
            x = domain_totnsupers(data)
            summary = data.summary.sel(nthreads=nthreads)
            y = summary[:, 0, 4]
            lq, uq = summary[:, 2, 4], summary[:, 3, 4]

            llab = None
            if nthreads == data.nthreads[0]:
                llab = lab
            axs[2].plot(
                x,
                y,
                color=c1,
                marker=markers[lab],
                linestyle=lstyles[lab],
                label=llab,
            )
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
            for nthreads in data.nthreads:
                x = domain_totnsupers(data)
                datavar = data[var].sel(nthreads=nthreads)
                y = datavar[:, 0, 0]
                lq, uq = datavar[:, 2, 0], datavar[:, 3, 0]

                llab = None
                if nthreads == data.nthreads[0]:
                    llab = lab
                    if a == 0:
                        llab += f" in {var}"
                axs[0].plot(
                    x,
                    y,
                    color=colors[v],
                    marker=markers[lab],
                    linestyle=lstyles[lab],
                    label=llab,
                )
                hfuncs.add_shading(axs[0], x, lq, uq, colors[v], lstyles[lab])
                a += 1
    axs[0].set_title("total runtime")

    vars = ["init_gbxs", "init_supers"]
    colors = ["mediumorchid", "hotpink"]
    for v, var in enumerate(vars):
        a = 0
        for lab, data in datasets.items():
            for nthreads in data.nthreads:
                x = domain_totnsupers(data)
                datavar = data[var].sel(nthreads=nthreads)
                y = datavar[:, 0, 0]
                lq, uq = datavar[:, 2, 0], datavar[:, 3, 0]

                llab = None
                if nthreads == data.nthreads[0]:
                    llab = lab
                    if a == 0:
                        llab += f" in {var}"
                axs[1].plot(
                    x,
                    y,
                    color=colors[v],
                    marker=markers[lab],
                    linestyle=lstyles[lab],
                    label=llab,
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
            for nthreads in data.nthreads:
                x = domain_totnsupers(data)
                datavar = data[var].sel(nthreads=nthreads)
                y = datavar[:, 0, 0]
                lq, uq = datavar[:, 2, 0], datavar[:, 3, 0]

                llab = None
                if nthreads == data.nthreads[0]:
                    llab = lab
                    if a == 0:
                        llab += f" in {var}"
                axs[2].plot(
                    x,
                    y,
                    color=colors[v],
                    marker=markers[lab],
                    linestyle=lstyles[lab],
                    label=llab,
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
        figsize=(12, 15), nrows=2, ncols=1, sharex=True, logx=False, logy=False
    )

    c1 = "k"
    for lab, data in datasets.items():
        for nthreads in data.nthreads:
            yarr = (
                data.host_high_water_memory_consumption.sel(nthreads=nthreads) / 1000
            )  # [MB]
            x = domain_totnsupers(data)
            y = yarr[:, 0]
            lq, uq = yarr[:, 2], yarr[:, 3]

            llab = None
            if nthreads == data.nthreads[0]:
                llab = lab
            axs[0].plot(
                x,
                y,
                color=c1,
                marker=markers[lab],
                linestyle=lstyles[lab],
                label=llab,
            )
            hfuncs.add_shading(axs[0], x, lq, uq, c1, lstyles[lab])
    axs[0].legend()
    axs[0].set_ylabel("host high water memory consumption / MB")

    spaces = data.spaces.values[0:2]
    colors = ["tab:orange", "tab:green"]
    for i in range(2):
        a = 0
        for lab, data in datasets.items():
            for nthreads in data.nthreads:
                x = domain_totnsupers(data)
                yarr = data.max_memory_allocation.sel(nthreads=nthreads) / 1000  # [MB]
                y = yarr[:, 0, i]
                llab = None
                if nthreads == data.nthreads[0]:
                    llab = lab
                    if a == 0:
                        llab += f" in {spaces[i]}"
                axs[1].plot(
                    x,
                    y,
                    color=colors[i],
                    marker=markers[lab],
                    linestyle=lstyles[lab],
                    label=llab,
                )
                lq, uq = yarr[:, 2, i], yarr[:, 3, i]
                hfuncs.add_shading(axs[1], x, lq, uq, c1, lstyles[lab])
                a += 1
    axs[1].legend()
    axs[1].set_ylabel("max memory allocation / MB")

    axs[-1].set_xlabel("Total Superdroplets in Domain")
    return fig, axs


# %% make kernel timer plots for each nsupers
for n in fixed_ensemb_vals:
    # load data
    datasets_time = {}
    for buildtype in buildtypes:
        datasets_time[buildtype] = hfuncs.open_kerneltimer_dataset(
            path2builds, buildtype, executable, ensembletype, n
        )

    # %% plot data
    fig, axs = plot_overall_wallclock_scaling(datasets_time)
    savename = savedir / f"total_wallclock_{ensembletype}ensemble_n{n}.png"
    hfuncs.savefig(savename)
    # %%
    fig, axs = plot_simple_wallclock_scaling(datasets_time)
    savename = savedir / f"simple_wallclock_{ensembletype}ensemble_n{n}.png"
    hfuncs.savefig(savename)
    # %%
    fig, axs = plot_simple_wallclock_timeinkernels_scaling(datasets_time)
    savename = savedir / f"wallclock_inkernels_{ensembletype}ensemble_n{n}.png"
    hfuncs.savefig(savename)
    # %%
    fig, axs = plot_wallclock_decomposition_scaling(datasets_time)
    savename = savedir / f"wallclock_decomposition_{ensembletype}ensemble_n{n}.png"
    hfuncs.savefig(savename)

# %% make spacetimestack plots for each nsupers
for n in fixed_ensemb_vals:
    # load data
    datasets_mem = {}
    for buildtype in buildtypes:
        datasets_mem[buildtype] = hfuncs.open_spacetimestack_dataset(
            path2builds, buildtype, executable, ensembletype, n
        )

    # %% plot data
    fig, axs = plot_simple_memory_scaling(datasets_mem)
    savename = savedir / f"memory_consumption_{ensembletype}ensemble_n{n}.png"
    hfuncs.savefig(savename)

# %%
