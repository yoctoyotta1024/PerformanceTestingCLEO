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
import matplotlib.pyplot as plt
import xarray as xr
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


# %%
def plot_space_time_stack_memory_allocations_vs_total_num_supers(datasets: dict):
    fig = plt.figure(figsize=(12, 8))
    gs = GridSpec(2, 2, figure=fig)
    ax0 = fig.add_subplot(gs[0, :])
    ax0b = ax0.twinx()  # for max memory consumption
    ax1 = fig.add_subplot(gs[1, 0])
    ax2 = fig.add_subplot(gs[1, 1])

    for ax in [ax0, ax1, ax2]:
        ax.spines[["right", "top"]].set_visible(False)
    ax0b.spines[["left", "top"]].set_visible(False)

    # buildtype: linestyle
    linestyles = {
        "Serial": (0, (1, 1)),  # densely dotted
        "CUDA": "-.",
        "OpenMP": "-",
        "C++Threads": "--",
    }

    ds_serial = datasets["Serial"]

    totnsupers_serial = ds_serial.ngbxs * ds_serial.attrs["nsupers"]
    highwater_serial = ds_serial.host_high_water_memory_consumption.sel(
        nthreads=1, statistic="mean"
    )  # kB
    maxalloc_host_serial = ds_serial.max_memory_allocation.sel(
        nthreads=1, statistic="mean", spaces="HOST"
    )  # kB
    ax0.plot(
        totnsupers_serial / 1e6,
        highwater_serial / 1e6,
        color="darkblue",
        linestyle=linestyles["Serial"],
    )
    ax0b.plot(
        totnsupers_serial / 1e6,
        maxalloc_host_serial / 1e6,
        color="brown",
        linestyle=linestyles["Serial"],
    )
    ax0b.set_ylim(ax0.get_ylim())
    ax0.set_xlabel("total number of superdroplets in domain / 10$^6$")
    ax0.set_ylabel("host high water memory consumption /GB", color="darkblue")
    ax0b.set_ylabel("maximum memory allocation / GB", color="brown")

    build = "CUDA"
    ds = datasets[build]
    for ngbxs in ds.ngbxs:
        highwater = ds.host_high_water_memory_consumption.sel(
            ngbxs=ngbxs, statistic="mean"
        )  # kB
        highwater = highwater / highwater_serial.sel(ngbxs=ngbxs)
        ax1.plot(ds.nthreads, highwater, label=f"{build}, ngbxs={ngbxs}")

        maxalloc_host = ds.max_memory_allocation.sel(
            ngbxs=ngbxs, statistic="mean", spaces="HOST"
        )  # kB
        maxalloc_host = maxalloc_host / maxalloc_host_serial.sel(ngbxs=ngbxs)
        ax2.plot(ds.nthreads, maxalloc_host)
        if build == "CUDA":
            maxalloc_device = ds_serial.max_memory_allocation.sel(
                ngbxs=ngbxs, statistic="mean", spaces="CUDA"
            )  # kB
            maxalloc_device = maxalloc_device / maxalloc_host_serial.sel(ngbxs=ngbxs)
            ax2.plot(ds.nthreads, maxalloc_device, label=f"{build}, ngbxs={ngbxs}")

    ax1.legend()
    ax2.legend()

    ax1.set_xlabel("number of CPU threads")
    ax1.set_ylabel(
        "host high water memory consumption relative to serial", color="darkblue"
    )

    ax2.set_xlabel("number of CPU threads")
    ax2.set_ylabel("maximum memory allocation relative to serial", color="brown")

    fig.tight_layout()

    return fig, [ax0, ax0b, ax1, ax2]


### -------------------------------------- ###

### -------------- plotting -------------- ###

# %%
fig, axs = plot_space_time_stack_memory_allocations_vs_total_num_supers(datasets)
savename = path4plots / "memory_vs_totnsupers.png"
save_figure(savename)
