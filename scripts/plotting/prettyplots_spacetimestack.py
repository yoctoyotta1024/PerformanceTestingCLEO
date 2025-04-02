"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: prettyplots_spacetimestack.py
Project: plotting
Created Date: Friday 28th March 2025
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Friday 28th March 2025
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
Standalone script for pretty plotting specific scaling plots of specific datasets.
Intented for use on output of thermo3d test spacetimestack datasets.
"""

# %%
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from matplotlib.colors import LogNorm
from matplotlib.gridspec import GridSpec
from pathlib import Path
from typing import Optional

# %%
### ---------- input parameters ---------- ###
### path to directory to save plots in
path4plots = Path("/home") / "m" / "m300950" / "performance_testing_cleo" / "plots"

### paths to datatsets for each build type
path2builds = (
    Path("/work") / "bm1183" / "m300950" / "performance_testing_cleo" / "builds"
)
serial = path2builds / "serial" / "bin" / "thermo3d"
openmp = path2builds / "openmp" / "bin" / "thermo3d"
threads = path2builds / "threads" / "bin" / "thermo3d"
cuda = path2builds / "cuda" / "bin" / "thermo3d"

### datatsets for average over ensemble of runs for varioud ngbxs and threads for each build type
nsupers = 256  # number of superdroplets per gridbox in datasets
datasets = {
    "Serial": xr.open_zarr(
        serial / f"kp_spacetimestack_ngbxsensemble_nsupers{nsupers}.zarr"
    ),
    "CUDA": xr.open_zarr(
        cuda / f"kp_spacetimestack_ngbxsensemble_nsupers{nsupers}.zarr"
    ),
    "OpenMP": xr.open_zarr(
        openmp / f"kp_spacetimestack_ngbxsensemble_nsupers{nsupers}.zarr"
    ),
    "C++Threads": xr.open_zarr(
        threads / f"kp_spacetimestack_ngbxsensemble_nsupers{nsupers}.zarr"
    ),
}
### -------------------------------------- ###


# %%
### --------- plotting functions --------- ###
def save_figure(savename: Path, dpi: Optional[int] = 128, tight: Optional[bool] = True):
    plt.savefig(savename, dpi=dpi, bbox_inches="tight")
    print(f"figure saved as {str(savename)}")


def extrapolate_variable(
    var: xr.DataArray,
    new_coords: xr.DataArray,
):
    # extrapolate gbxs dimension of var to match new_coords
    if len(var.coords["ngbxs"]) != len(new_coords) or np.any(
        var.coords["ngbxs"].values != new_coords.values
    ):
        print(f"warning: extrapolating ngbxs coordinate of {var.name}")
        var = var.interp(ngbxs=new_coords, kwargs={"fill_value": "extrapolate"})

    return var


def linear_scaling(x, y):
    """fit straight line with gradient 'm' from (x[0],y[0]) to (x[-1],y[-1])"""
    m = (y[-1] - y[0]) / (x[-1] - x[0])
    return (
        [x[0], x[-1]],
        [y[0], y[-1]],
        m,
    )  # x and y of 2 points and gradient of straight line


# %%
def plot_serial_space_time_stack_memory_allocations_vs_total_num_supers(
    ax0, ds_serial: xr.Dataset, linestyle: str
):
    ax0b = ax0.twinx()  # for max memory consumption
    ax0b.spines[["left", "top"]].set_visible(False)

    totnsupers_serial = (
        ds_serial.ngbxs * ds_serial.attrs["nsupers"] / 1e6
    )  # per 1e6 SDs
    highwater_serial = (
        ds_serial.host_high_water_memory_consumption.sel(nthreads=1, statistic="mean")
        / 1e6
    )  # GB
    maxalloc_host_serial = (
        ds_serial.max_memory_allocation.sel(nthreads=1, statistic="mean", spaces="HOST")
        / 1e6
    )  # GB
    ax0.plot(
        totnsupers_serial,
        highwater_serial,
        color="green",
        linestyle=linestyle,
        linewidth=2,
    )
    ax0b.plot(
        totnsupers_serial,
        maxalloc_host_serial,
        color="brown",
        linestyle=linestyle,
        linewidth=2,
    )

    x0, y0, m0 = linear_scaling(totnsupers_serial, highwater_serial)
    lines_fit0 = ax0.plot(x0, y0, color="dimgrey", linestyle="-", linewidth=0.5)
    x1, y1, m1 = linear_scaling(totnsupers_serial, maxalloc_host_serial)
    lines_fitb = ax0b.plot(x1, y1, color="dimgrey", linestyle="-", linewidth=0.5)

    ax0.set_xlabel("total number of superdroplets in domain / 10$^6$")
    ax0.set_ylabel("CPU high-water memory consumption /GB", color="green")
    ax0b.set_ylabel("maximum memory allocation /GB", color="brown")
    ax0.set_xlim(left=0)
    ax0.set_ylim(bottom=0.0)
    ax0b.set_ylim(ax0.get_ylim())

    lines0 = ax0.plot(
        totnsupers_serial,
        highwater_serial,
        color="k",
        linestyle=linestyle,
        linewidth=2,
        zorder=0,
    )
    labels = ["serial", "linear fit, m={:.3f}".format(m0.values)]
    handles = [lines0[0], lines_fit0[0]]
    leg = ax0.legend(labels=labels, handles=handles, loc="upper left")
    plt.setp(leg.get_texts()[1], color="green")
    labelb = "linear fit, m={:.3f}".format(m1.values)
    legb = ax0b.legend(labels=[labelb], handles=[lines_fitb[0]], loc="lower right")
    plt.setp(legb.get_texts()[0], color="brown")

    return ax0, ax0b, highwater_serial * 1e6, maxalloc_host_serial * 1e6  # memory in kB


def plot_space_time_stack_memory_allocations_vs_nthreads(
    datasets: dict, ngbxs2plot: dict, nsupers: int
):
    fig = plt.figure(figsize=(9, 6.5))
    gs = GridSpec(2, 2, figure=fig, height_ratios=[5, 4])
    ax0 = fig.add_subplot(gs[0, :])
    ax1 = fig.add_subplot(gs[1, 0])
    ax2 = fig.add_subplot(gs[1, 1])

    for ax in [ax0, ax1, ax2]:
        ax.spines[["right", "top"]].set_visible(False)

    # buildtype: linestyle
    linestyles = {
        "Serial": (0, (1, 1)),  # densely dotted
        "CUDA": "-.",  # CUDA_host
        "CUDA_device": (0, (3, 5, 1, 5)),  # dashdotted
        "OpenMP": "-",
        "C++Threads": "--",
    }

    colors = {}
    cmap = plt.get_cmap("plasma")
    norm = LogNorm(vmin=1e2, vmax=1e8)
    for ngbxs in list(ngbxs2plot.values())[0]:
        colors[ngbxs] = cmap(norm(ngbxs * nsupers))

    # total number of superdroplets in domain: formatted number
    formatted_labels = {
        256: "3x10$^2$",
        16384: "2x10$^4$",
        131072: "1x10$^5$",
        1048576: "1x10$^6$",
        8388608: "8x10$^6$",
        33554432: "3x10$^7$",
    }

    ds_serial = datasets["Serial"]
    (
        ax0,
        ax0b,
        highwater_serial,
        maxalloc_host_serial,
    ) = plot_serial_space_time_stack_memory_allocations_vs_total_num_supers(
        ax0, ds_serial, linestyles["Serial"]
    )

    handles1 = {}  # for totnsupers colours
    handles2 = {}  # for build types linestyles
    for build in ngbxs2plot.keys():
        ds = datasets[build]
        highwater_serial = extrapolate_variable(highwater_serial, ds.ngbxs)
        maxalloc_host_serial = extrapolate_variable(maxalloc_host_serial, ds.ngbxs)
        for ngbxs in ngbxs2plot[build]:
            highwater = ds.host_high_water_memory_consumption.sel(
                ngbxs=ngbxs, statistic="mean"
            )  # kB
            highwater = highwater / highwater_serial.sel(ngbxs=ngbxs)
            ax1.plot(
                ds.nthreads, highwater, linestyle=linestyles[build], color=colors[ngbxs]
            )

            maxalloc_host = ds.max_memory_allocation.sel(
                ngbxs=ngbxs, statistic="mean", spaces="HOST"
            )  # kB
            maxalloc_host = maxalloc_host / maxalloc_host_serial.sel(ngbxs=ngbxs)
            lines = ax2.plot(
                ds.nthreads,
                maxalloc_host,
                linestyle=linestyles[build],
                color=colors[ngbxs],
            )

            if build == "CUDA":
                maxalloc_device = ds.max_memory_allocation.sel(
                    ngbxs=ngbxs, statistic="mean", spaces="CUDA"
                )  # kB
                maxalloc_device = maxalloc_device / maxalloc_host_serial.sel(
                    ngbxs=ngbxs
                )
                ax2.plot(
                    ds.nthreads,
                    maxalloc_device,
                    linestyle=linestyles["CUDA_device"],
                    color=colors[ngbxs],
                )

            if build == list(ngbxs2plot.keys())[0]:  # best if == "OpenMP"
                totnsupers = ngbxs * ds.attrs["nsupers"]
                handles1[totnsupers] = lines[0]

        lines_lab = ax2.plot(
            ds.nthreads, maxalloc_host, linestyle=linestyles[build], color="k", zorder=0
        )
        if build == "CUDA":
            linesb_lab = ax2.plot(
                ds.nthreads,
                maxalloc_device,
                linestyle=linestyles["CUDA_device"],
                color="k",
                zorder=0,
            )
            handles2["CUDA CPU"] = lines_lab[0]
            handles2["CUDA GPU"] = linesb_lab[0]
        else:
            handles2[build] = lines_lab[0]

    ax1.set_xlim([0, 130])
    ax1.set_xlabel("number of CPU threads")
    ax1.set_ylabel(
        "CPU high-water memory consumption\nrelative to serial", color="green"
    )
    labels = [formatted_labels[i] for i in handles1.keys()]
    labels[0] = f"#SDs = {labels[0]}"
    ax1.legend(
        handles=list(handles1.values()), labels=labels, loc="upper right", fontsize=9
    )

    ax2.set_xlim([0, 130])
    ax2.set_xlabel("number of CPU threads")
    ax2.set_ylabel("maximum memory allocation\nrelative to serial", color="brown")
    ax2.legend(
        handles=list(handles2.values()),
        labels=list(handles2.keys()),
        loc="upper left",
        fontsize=9,
    )

    fig.tight_layout()

    return fig, [ax0, ax0b, ax1, ax2]


### -------------------------------------- ###

### -------------- plotting -------------- ###

# %%
ngbxs2plot = {
    "OpenMP": [64, 512, 4096, 32768, 131072],
    "C++Threads": [64, 512, 4096, 32768, 131072],
    "CUDA": [64, 512, 4096, 32768, 131072],
}
fig, axs = plot_space_time_stack_memory_allocations_vs_nthreads(
    datasets, ngbxs2plot, nsupers
)
savename = path4plots / "memory_vs_totnsupers.png"
save_figure(savename)

# %%
ngbxs2plot = {
    "OpenMP": [1, 64, 512, 4096, 32768, 131072],
    "C++Threads": [1, 64, 512, 4096, 32768, 131072],
    "CUDA": [1, 64, 512, 4096, 32768, 131072],
}
for build in ngbxs2plot.keys():
    fig, axs = plot_space_time_stack_memory_allocations_vs_nthreads(
        datasets, {build: ngbxs2plot[build]}, nsupers
    )
    savename = path4plots / f"memory_vs_totnsupers_{build}.png"
    save_figure(savename)

# %%
