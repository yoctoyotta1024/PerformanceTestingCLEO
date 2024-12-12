"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: performance_plots.py
Project: scripts
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
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from typing import Optional

# e.g. ipykernel_launcher.py [path2builds] [executable]
parser = argparse.ArgumentParser()
parser.add_argument(
    "--path2builds",
    type=Path,
    help="Absolute path to builds",
    default="/work/bm1183/m300950/performance_testing_cleo/builds/",
)
parser.add_argument(
    "--executable", type=str, help="Executable name, e.g. colls0d", default="colls0d"
)
args, unknown = parser.parse_known_args()
path2builds = args.path2builds
executable = args.executable

lstyles = {
    "serial": "dotted",
    "openmp": "dashdot",
    "cuda": "solid",
    "threads": "dashed",
}

markers = {"serial": "o", "openmp": "s", "cuda": "x", "threads": "d"}

savedir = Path("/home/m/m300950/performance_testing_cleo/plots/")


# %% funtion definitions for generic helper functions
def open_kerneltimer_dataset(path2builds: Path, buildtype: str, executable: str):
    path2ds = path2builds / buildtype / "bin" / executable / "kp_kerneltimer.zarr"
    return xr.open_zarr(path2ds)


def open_spacetimestack_dataset(path2builds: Path, buildtype: str, executable: str):
    path2ds = path2builds / buildtype / "bin" / executable / "kp_spacetimestack.zarr"
    return xr.open_zarr(path2ds)


def savefig(savename: Path, dpi: Optional[int] = 128):
    plt.savefig(savename, dpi=dpi, bbox_inches="tight")
    print(f"figure saved as {str(savename)}")


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


def add_shading(
    ax,
    x,
    lower,
    upper,
    c,
    ls,
    a: Optional[float] = 0.3,
    label: Optional[str] = None,
    add_y: Optional[bool] = None,
):
    if add_y is not None:
        lower = add_y - lower
        upper = add_y + upper
    ax.fill_between(
        x, lower, upper, color=c, linestyle=ls, alpha=a, label=label, zorder=0
    )


# %% funtion definitions for kernel timer plots
def plot_simple_wallclock_scaling(datasets: dict):
    fig, axs = plt.subplots(figsize=(12, 6))
    axs.spines[["right", "top"]].set_visible(False)
    c1 = "k"
    c2 = "purple"
    a = 0
    for lab, data in datasets.items():
        x, y = data.nsupers, data.summary[:, 0, 0]

        lq, uq = data.summary[:, 2, 0], data.summary[:, 3, 0]
        slab = None
        if a == 0:
            slab = "IQR"
        add_shading(axs, x, lq, uq, c1, lstyles[lab], label=slab)

        axs.plot(
            x,
            y,
            color=c1,
            marker=markers[lab],
            linestyle=lstyles[lab],
            label=lab,
        )

        xfit, yfit, m, c = line_of_best_fit(x, y, skip=2, logaxs=True)
        axs.plot(xfit, yfit, color=c2, linestyle=lstyles[lab], label=f"scaling={m:.2f}")
        a += 1
    axs.set_xscale("log")
    axs.set_yscale("log")
    axs.set_xlabel("Superdroplets per Gridbox")
    axs.set_ylabel("Total Wall Clock Time /s")
    axs.legend()
    return fig, axs


def plot_simple_wallclock_timeinkernels_scaling(datasets: dict):
    fig, axs = plt.subplots(figsize=(12, 18), nrows=3, ncols=1, sharex=True)
    for ax in axs:
        ax.spines[["right", "top"]].set_visible(False)

    c1 = "k"
    for lab, data in datasets.items():
        x, y = data.nsupers, data.summary[:, 0, 3]
        axs[0].plot(
            x,
            y,
            color=c1,
            marker=markers[lab],
            linestyle=lstyles[lab],
            label=lab,
        )
        lq, uq = data.summary[:, 2, 3], data.summary[:, 3, 3]
        add_shading(axs[0], x, lq, uq, c1, lstyles[lab])
        axs[0].set_ylabel("% of Total Wall Clock Time in Kernels")
    axs[0].legend()

    c1 = "tab:blue"
    a = 0
    for lab, data in datasets.items():
        x, y = data.nsupers, data.summary[:, 0, 1]
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
        add_shading(axs[1], x, lq, uq, c1, lstyles[lab])
        a += 1

    c2 = "tab:green"
    a = 0
    for lab, data in datasets.items():
        x, y = data.nsupers, data.summary[:, 0, 2]
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
        add_shading(axs[1], x, lq, uq, c2, lstyles[lab])
        a += 1

    axs[1].set_yscale("log")
    axs[1].set_ylabel("Total Wall Clock Time /s")
    axs[1].legend()

    c1 = "k"
    for lab, data in datasets.items():
        x, y = data.nsupers, data.summary[:, 0, 4]
        axs[2].plot(
            x,
            y,
            color=c1,
            marker=markers[lab],
            linestyle=lstyles[lab],
            label=lab,
        )
        lq, uq = data.summary[:, 2, 4], data.summary[:, 3, 4]
        add_shading(axs[2], x, lq, uq, c1, lstyles[lab])
        axs[2].set_ylabel("Total Number of Calls to Kernels")
    axs[2].legend()

    axs[0].set_xscale("log")
    axs[-1].set_xlabel("Superdroplets per Gridbox")
    return fig, axs


def plot_wallclock_decomposition_scaling(datasets: dict):
    fig, axs = plt.subplots(figsize=(12, 18), nrows=3, ncols=1, sharex=True)
    for ax in axs:
        ax.spines[["right", "top"]].set_visible(False)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_ylabel("Wall Clock Time /s")

    vars = ["runcleo", "init", "timestep"]
    colors = ["black", "darkviolet", "green"]
    v = 0
    for v, var in enumerate(vars):
        a = 0
        for lab, data in datasets.items():
            x, y = data.nsupers, data[var][:, 0, 0]
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
            add_shading(axs[0], x, lq, uq, colors[v], lstyles[lab])
            a += 1
    axs[0].set_title("total runtime")

    vars = ["init_gbxs", "init_supers"]
    colors = ["mediumorchid", "hotpink"]
    for v, var in enumerate(vars):
        a = 0
        for lab, data in datasets.items():
            x, y = data.nsupers, data[var][:, 0, 0]
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
            add_shading(axs[1], x, lq, uq, colors[v], lstyles[lab])
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
            x, y = data.nsupers, data[var][:, 0, 0]
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
            add_shading(axs[2], x, lq, uq, colors[v], lstyles[lab])
            a += 1
    axs[2].set_title("timestepping")

    for ax in axs:
        ax.legend()
    axs[-1].set_xlabel("Superdroplets per Gridbox")
    return fig, axs


# %% funtion definitions for memory consumption plots
def plot_simple_memory_scaling(datasets: xr.Dataset):
    fig, axs = plt.subplots(figsize=(12, 12), nrows=2, ncols=1, sharex=True)
    for ax in axs:
        ax.spines[["right", "top"]].set_visible(False)
        ax.set_xscale("log")

    c1 = "k"
    for lab, data in datasets.items():
        yarr = data.host_high_water_memory_consumption / 1000  # [MB]
        x, y = data.nsupers, yarr[:, 0]
        lq, uq = yarr[:, 2], yarr[:, 3]
        axs[0].plot(
            x,
            y,
            color=c1,
            marker=markers[lab],
            linestyle=lstyles[lab],
            label=lab,
        )
        add_shading(axs[0], x, lq, uq, c1, lstyles[lab])
    axs[0].legend()
    axs[0].set_ylabel("host high water memory consumption / MB")

    spaces = data.spaces.values[0:2]
    colors = ["tab:orange", "tab:green"]
    for i in range(2):
        a = 0
        for lab, data in datasets.items():
            yarr = data.max_memory_allocation / 1000  # [MB]
            x, y = data.nsupers, yarr[:, 0, i]
            lq, uq = yarr[:, 2, i], yarr[:, 3, i]
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
            add_shading(axs[1], x, lq, uq, c1, lstyles[lab])
            a += 1
    axs[1].legend()
    axs[1].set_ylabel("max memory allocation / MB")

    axs[-1].set_xlabel("Superdroplets per Gridbox")
    return fig, axs


# %% load data
serial = open_kerneltimer_dataset(path2builds, "serial", executable)
openmp = open_kerneltimer_dataset(path2builds, "openmp", executable)
cuda = open_kerneltimer_dataset(path2builds, "cuda", executable)
threads = open_kerneltimer_dataset(path2builds, "threads", executable)
datasets_time = {
    "serial": serial,
    "openmp": openmp,
    "cuda": cuda,
    "threads": threads,
}
# %%
fig, axs = plot_simple_wallclock_scaling(datasets_time)
savename = savedir / "simple_wallclock.png"
savefig(savename)
# %%
fig, axs = plot_simple_wallclock_timeinkernels_scaling(datasets_time)
savename = savedir / "wallclock_inkernels.png"
savefig(savename)
# %%
fig, axs = plot_wallclock_decomposition_scaling(datasets_time)
savename = savedir / "wallclock_decomposition.png"
savefig(savename)

# %%
serial = open_spacetimestack_dataset(path2builds, "serial", executable)
openmp = open_spacetimestack_dataset(path2builds, "openmp", executable)
cuda = open_spacetimestack_dataset(path2builds, "cuda", executable)
threads = open_spacetimestack_dataset(path2builds, "threads", executable)
datasets_mem = {
    "serial": serial,
    "openmp": openmp,
    "cuda": cuda,
    "threads": threads,
}

# %%
fig, axs = plot_simple_memory_scaling(datasets_mem)
savename = savedir / "memory_consumption.png"
savefig(savename)
