"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: prettyplots_kerneltimer.py
Project: plotting
Created Date: Thursday 27th March 2025
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Thursday 27th March 2025
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
Standalone script for pretty plotting specific scaling plots of specific datasets.
Intented for use on output of thermo3d test kerneltimer datasets.
"""

# %%
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
from matplotlib.cm import ScalarMappable
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
        serial / f"kp_kerneltimer_ngbxsensemble_nsupers{nsupers}.zarr"
    ),
    "CUDA": xr.open_zarr(cuda / f"kp_kerneltimer_ngbxsensemble_nsupers{nsupers}.zarr"),
    "OpenMP": xr.open_zarr(
        openmp / f"kp_kerneltimer_ngbxsensemble_nsupers{nsupers}.zarr"
    ),
    "C++Threads": xr.open_zarr(
        threads / f"kp_kerneltimer_ngbxsensemble_nsupers{nsupers}.zarr"
    ),
}

### simulation parameters
simulated_time = 4800  # length of simulation [s]
### -------------------------------------- ###


# %%
### --------- plotting functions --------- ###
def save_figure(savename: Path, dpi: Optional[int] = 128, tight: Optional[bool] = True):
    plt.savefig(savename, dpi=dpi, bbox_inches="tight")
    print(f"figure saved as {str(savename)}")


def calculate_speedup(
    time: xr.DataArray,
    time_reference: xr.DataArray,
    extrapolate: Optional[bool] = False,
):
    # extrapolate gbxs dimension of time_reference to match time
    if extrapolate:
        if len(time.coords["ngbxs"]) != len(time_reference.coords["ngbxs"]) or np.any(
            time.coords["ngbxs"].values != time_reference.coords["ngbxs"].values
        ):
            print("warning: speedup calculation extrapolating reference")
            time_reference = time_reference.interp(
                ngbxs=time.coords["ngbxs"], kwargs={"fill_value": "extrapolate"}
            )

    return time_reference / time


def perfect_scaling(x1, x2, y1, m=1):
    """straight line on log-log plot with gradient 'm' from (x1,y1) to (x2,y2)
    such that y = A * x^m and goes through (x1, y1)"""
    log10_y2 = np.log10(y1) + m * (np.log10(x2) - np.log10(x1))  # straight line
    return [x1, x2], [y1, 10**log10_y2]  # [x, y]


# %%
def plot_wallclock_vs_total_num_supers(
    datasets: dict, nthreads2plot: dict, simulated_time: float
):
    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10.5, 7), sharex=True)
    axs = axs.flatten()

    # buildtype: linestyle
    linestyles = {
        "Serial": "-.",
        "CUDA": (0, (1, 1)),  # densely dotted
        "OpenMP": "-",
        "C++Threads": "--",
    }

    buildtypes = datasets.keys()
    for ax, build in zip(axs, buildtypes):
        nthreads = nthreads2plot[build]
        ds = datasets[build].sel(nthreads=nthreads)
        alpha = 0.3

        if build == "OpenMP" or build == "C++Threads":
            ax.text(
                0.5,
                0.93,
                f"{build} with {nthreads} Threads",
                ha="center",
                transform=ax.transAxes,
                fontsize=11,
            )
        elif build == "CUDA":
            ax.text(
                0.5,
                0.93,
                f"{build} with 1 GPU and {nthreads} CPU Threads",
                ha="center",
                transform=ax.transAxes,
                fontsize=11,
            )
        else:
            ax.text(0.5, 0.93, build, ha="center", transform=ax.transAxes, fontsize=11)

        # variable_name: [label, colour]
        vars = {
            "summary": ["Total", "tab:blue"],
            "timestep_sdm": ["SDM", "tab:cyan"],
            "timestep_sdm_movement": ["Motion", "tab:purple"],
            "timestep_sdm_microphysics": ["Microphysics", "tab:red"],
        }

        for var, props in vars.items():
            x = (
                ds.attrs["nsupers"] * ds.ngbxs
            )  # total number of superdroplets in domain
            data = ds[var] / simulated_time
            y = data[:, 0, 0]  # simulated time / mean wall-clock time
            lq, uq = data[:, 2, 0], data[:, 3, 0]  # lower and upper quartiles
            ax.plot(x, y, color=props[1], linestyle=linestyles[build], label=props[0])
            ax.fill_between(
                x,
                lq,
                uq,
                color=props[1],
                linestyle=linestyles[build],
                alpha=alpha,
                zorder=0,
            )

        if build == "Serial":
            linear = perfect_scaling(x[0], x[-1], y[0])
            perf = ax.plot(
                linear[0],
                linear[1],
                linewidth=0.5,
                color="dimgrey",
                label="1:1 scaling",
            )
            axb = axs[0].twinx()
            axb.set_yticks([])
            axb.spines[["left", "bottom", "right", "top"]].set_visible(False)
            axb.legend(handles=perf, loc="lower left")

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.spines[["right", "top"]].set_visible(False)

    handles, labels = axs[2].get_legend_handles_labels()  # solid lines
    axs[0].legend(handles=handles, labels=labels, loc="upper left")

    axs[0].set_ylabel("wall-clock time per simulated second /s")
    axs[2].set_ylabel("wall-clock time per simulated second /s")
    axs[2].set_xlabel("total number of superdroplets in domain")
    axs[3].set_xlabel("total number of superdroplets in domain")

    for ax in axs:
        ax.set_ylim([5e-5, 5])

    fig.tight_layout()

    return fig, axs


# %%
def plot_wallclock_strong_scaling_for_total_num_supers(
    datasets: dict, ngbxs2plot: dict, simulated_time: float, nsupers: int
):
    fig = plt.figure(figsize=(18, 6))
    gs = GridSpec(1, 4, figure=fig, width_ratios=[30, 30, 30, 1])
    cax = fig.add_subplot(gs[0, -1])
    axs = []
    for i in range(3):
        axs.append(fig.add_subplot(gs[0, i]))

    # buildtype: line/marker style
    styles = {
        "Serial": "x",  # marker
        "CUDA": "o",  # marker
        "OpenMP": "-",  # line
        "C++Threads": "--",  # line
    }

    colors = {}
    cmap = plt.get_cmap("plasma")
    norm = LogNorm(vmin=1e2, vmax=1e8)
    for ngbxs in ngbxs2plot["CUDA"]:
        colors[ngbxs] = cmap(norm(ngbxs * nsupers))

    fig.colorbar(
        ScalarMappable(cmap=cmap, norm=norm),
        boundaries=[5, 5e1, 5e2, 5e3, 5e4, 5e5, 5e6, 5e7],
        cax=cax,
        label="total number of superdroplets in domain",
        format="%2g",
    )

    # variable_name: [label, colour]
    vars = {
        "timestep_sdm": ["SDM", "tab:cyan"],
        "timestep_sdm_microphysics": ["Microphysics", "tab:red"],
        "timestep_sdm_movement": ["Motion", "tab:purple"],
    }

    for ax, var in zip(axs, vars.keys()):
        ax.set_title(vars[var][0], color=vars[var][1])
        handles = {}
        for build in datasets.keys():
            ds = datasets[build]
            alpha = 0.3

            x = ds.nthreads
            data = ds[var].sel(ngbxs=ngbxs2plot[build]) / simulated_time

            # for legend
            if build == "CUDA" or build == "Serial":
                x_ = ds.nthreads.max()
                y_ = data.sel(nthreads=x_, ngbxs=data.ngbxs.min())[0, 0]
                lines = [
                    ax.scatter(
                        x_, y_, color="k", marker=styles[build], label=build, zorder=0
                    )
                ]
            else:
                lines = ax.plot(
                    x,
                    data[0, :, 0, 0],
                    color="k",
                    linestyle=styles[build],
                    label=build,
                    zorder=0,
                )

            for ngbxs in ngbxs2plot[build]:
                y = data.sel(ngbxs=ngbxs)[:, 0, 0]
                lq = data.sel(ngbxs=ngbxs)[:, 2, 0]
                uq = data.sel(ngbxs=ngbxs)[:, 3, 0]

                if build == "CUDA" or build == "Serial":
                    x_ = ds.nthreads.max()
                    y_ = y.sel(nthreads=x_)
                    lq_ = y_ - lq.sel(nthreads=x_)
                    uq_ = uq.sel(nthreads=x_) - y_
                    ax.errorbar(
                        x_,
                        y_,
                        yerr=[[lq_], [uq_]],
                        color=colors[ngbxs],
                        marker=styles[build],
                        zorder=10,
                    )
                else:
                    ax.plot(
                        x, y, color=colors[ngbxs], linestyle=styles[build], label=build
                    )
                    ax.fill_between(
                        x,
                        lq,
                        uq,
                        color=colors[ngbxs],
                        linestyle=styles[build],
                        alpha=alpha,
                        zorder=0,
                    )
            handles[build] = lines[0]
        ax.set_yscale("log")
        ax.spines[["right", "top"]].set_visible(False)

    axs[0].legend(handles=list(handles.values()), labels=list(handles.keys()))
    axs[0].set_ylabel("wall-clock time per simulated second /s")
    for a, ax in enumerate(axs):
        ax.set_xlim([0, 130])
        ax.set_ylim([1e-4, 1e1])
        ax.set_xticks([1, 16, 64, 128])
        ax.set_xlabel("number of CPU threads")
        if a != 0:
            ax.set_yticklabels([])

    fig.tight_layout()

    return fig, axs


# %%
def plot_speedup_strong_scaling_for_total_num_supers(
    datasets: dict,
    ngbxs2plot: dict,
    nsupers: int,
    colors: Optional[dict] = None,
):
    fig = plt.figure(figsize=(13.3, 4.75))
    gs = GridSpec(1, 3, figure=fig)
    axs = []
    for i in range(3):
        axs.append(fig.add_subplot(gs[0, i]))

    # buildtype: line/marker style
    styles = {
        "CUDA": "o",  # marker
        "OpenMP": "-",  # line
        "C++Threads": "--",  # line
    }

    if colors is None:
        colors = {}
        cmap = plt.get_cmap("plasma")
        norm = LogNorm(vmin=1e2, vmax=1e8)
        for ngbxs in ngbxs2plot["CUDA"]:
            colors[ngbxs] = cmap(norm(ngbxs * nsupers))

    # variable_name: [label, colour]
    vars = {
        "timestep_sdm": ["SDM", "tab:cyan"],
        "timestep_sdm_microphysics": ["Microphysics", "tab:red"],
        "timestep_sdm_movement": ["Motion", "tab:purple"],
    }

    # total number of superdroplets in domain: formatted number
    formatted_labels = {
        256: "3x10$^2$",
        16384: "2x10$^4$",
        131072: "1x10$^5$",
        1048576: "1x10$^6$",
        8388608: "8x10$^6$",
        33554432: "3x10$^7$",
    }

    ds_ref = datasets["Serial"].sel(nthreads=1)  # refernce dataset for speedup

    for ax, var in zip(axs, vars.keys()):
        ax.set_title(vars[var][0], color=vars[var][1])
        handles = {}
        handles2 = {}
        for build in datasets.keys():
            if build == "Serial":
                continue

            ds = datasets[build]
            alpha = 0.3

            x = ds.nthreads
            ref = ds_ref[var].sel(ngbxs=ngbxs2plot["Serial"])[:, :, 0]  # [gbxs, stat]
            data = ds[var].sel(ngbxs=ngbxs2plot[build])[
                :, :, :, 0
            ]  # [gbxs, threads, stat]

            y = calculate_speedup(
                data[:, :, 0], ref[:, 0], extrapolate=True
            )  # [gbxs, threads]
            lq = calculate_speedup(data[:, :, 3], ref[:, 2], extrapolate=True)
            uq = calculate_speedup(data[:, :, 2], ref[:, 3], extrapolate=True)

            # for legend
            if build == "CUDA":
                x_ = ds.nthreads.max()
                y_ = y.sel(nthreads=x_, ngbxs=y.ngbxs.min())
                lines = [
                    ax.scatter(
                        x_, y_, color="k", marker=styles[build], label=build, zorder=0
                    )
                ]
            else:
                lines = ax.plot(
                    x,
                    y[0],
                    color="k",
                    linestyle=styles[build],
                    label=build,
                    zorder=0,
                )

            for ngbxs in ngbxs2plot[build]:
                y_n = y.sel(ngbxs=ngbxs)
                lq_n = lq.sel(ngbxs=ngbxs)
                uq_n = uq.sel(ngbxs=ngbxs)

                if build == "CUDA" or build == "Serial":
                    x_ = ds.nthreads.max()
                    y_ = y_n.sel(nthreads=x_)
                    lq_ = y_ - lq_n.sel(nthreads=x_)
                    uq_ = uq_n.sel(nthreads=x_) - y_
                    lines2 = [
                        ax.errorbar(
                            x_,
                            y_,
                            yerr=[[lq_], [uq_]],
                            color=colors[ngbxs],
                            marker=styles[build],
                            linestyle="-",
                            zorder=10,
                        )
                    ]
                    handles2[ngbxs * nsupers] = lines2[0]
                else:
                    ax.plot(
                        x,
                        y_n,
                        color=colors[ngbxs],
                        linestyle=styles[build],
                        label=build,
                    )
                    ax.fill_between(
                        x,
                        lq_n,
                        uq_n,
                        color=colors[ngbxs],
                        linestyle=styles[build],
                        alpha=alpha,
                        zorder=0,
                    )
            handles[build] = lines[0]
        ax.spines[["right", "top"]].set_visible(False)

    axs[0].legend(
        handles=list(handles.values()), labels=list(handles.keys()), loc="upper left"
    )

    ax_tmp = axs[0].twinx()
    ax_tmp.spines[["left", "top", "right", "top"]].set_visible(False)
    ax_tmp.set_xticks([])
    ax_tmp.set_yticks([])
    labels = [formatted_labels[i] for i in handles2.keys()]
    labels[0] = f"#SDs={labels[0]}"
    ax_tmp.legend(handles=list(handles2.values()), labels=labels, loc="upper right")

    axs[0].set_ylabel("speed-up")

    for a, ax in enumerate(axs):
        ax.set_xlim([0, 130])
        ax.set_ylim([1, 130])
        ax.set_xticks([1, 16, 64, 128])
        ax.set_yticks([1, 32, 64, 96, 128])
        ax.set_xlabel("number of CPU threads")
    axs[2].set_ylim([0, 36])
    axs[2].set_yticks([1, 16, 32])

    fig.tight_layout()

    return fig, axs


### -------------------------------------- ###

### -------------- plotting -------------- ###

# %%
nthreads2plot = {
    "Serial": 1,
    "CUDA": 128,
    "OpenMP": 128,
    "C++Threads": 128,
}
fig, axs = plot_wallclock_vs_total_num_supers(datasets, nthreads2plot, simulated_time)
savename = path4plots / "wallclock_vs_totnsupers.png"
save_figure(savename)
# %%
ngbxs2plot = {
    "Serial": [1, 64, 512, 4096, 32768],
    "CUDA": [1, 64, 512, 4096, 32768, 131072],
    "OpenMP": [1, 64, 512, 4096, 32768, 131072],
    "C++Threads": [1, 64, 512, 4096, 32768, 131072],
}
fig, axs = plot_wallclock_strong_scaling_for_total_num_supers(
    datasets,
    ngbxs2plot,
    simulated_time,
    nsupers,
)
savename = path4plots / "strong_scaling_wallclock.png"
save_figure(savename)

# %%
ngbxs2plot = {
    "Serial": [1, 64, 512, 4096, 32768],
    "CUDA": [64, 512, 4096, 131072],
    "OpenMP": [64, 512, 4096, 131072],
    "C++Threads": [64, 512, 4096, 131072],
}
colors = {
    64: "orange",
    512: "crimson",
    4096: "darkviolet",
    131072: "mediumblue",
}
fig, axs = plot_speedup_strong_scaling_for_total_num_supers(
    datasets, ngbxs2plot, nsupers, colors=colors
)
savename = path4plots / "strong_scaling_speedup.png"
save_figure(savename)
### -------------------------------------- ###

# %%
