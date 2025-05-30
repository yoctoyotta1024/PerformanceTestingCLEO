"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: weak_scaling.py
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
Script for plotting weak scaling results (increasing resources for increasing problem size)
from zarr xarray datasets for kokkos profiling data. Note: standard data format assumed.
"""

# %%
import argparse
from pathlib import Path
import sys
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LogNorm
from matplotlib.gridspec import GridSpec

path2src = Path(__file__).resolve().parent.parent.parent / "src"
sys.path.append(str(path2src))  # for helperfuncs module
from plotting import helperfuncs as hfuncs

sys.path.append(str(Path(__file__).parent.parent))  # scripts directory
import shared_script_variables as ssv

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
    default="thermo3d",
)
args, unknown = parser.parse_known_args()
path2builds = args.path2builds
executable = args.executable

all_buildtypes = ["serial", "openmp", "threads", "cuda"]
buildtypes = ["openmp", "threads", "cuda"]
buildtype_reference = "serial"
nthreads_reference = 1

ngbxs_nsupers_runs = ssv.get_ngbxs_nsupers_runs()

nsupers_per_gbx = [256]

lstyles = hfuncs.buildtype_lstyles
markers = hfuncs.buildtype_markers

savedir = Path("/home/m/m300950/performance_testing_cleo/plots/")

cmap = plt.get_cmap("plasma")
norm = LogNorm(vmin=1, vmax=1e8)
ngbxs_max = 1048576
nthreads_max = 128


# %% funtion definitions for weak scaling plots
def plot_weak_scaling_wallclock(
    path2builds: Path,
    buildtypes: list[str],
    executable: str,
    nsupers: int,
    ngbxs_max: int,
    nthreads_max: int,
    cmap,
    norm,
):
    fig = plt.figure(figsize=(16, 20))
    gs = GridSpec(4, 2, figure=fig, height_ratios=[0.25, 7, 7, 7])
    cax = fig.add_subplot(gs[0, :])
    axs = []
    for j in range(2):
        for i in range(1, 4):
            axs.append(fig.add_subplot(gs[i, j]))
    for ax in axs:
        ax.spines[["right", "top"]].set_visible(False)
        ax.set_xscale("log")
        ax.set_yscale("log")

    fig.suptitle("Weak Scaling: Wall Clock Time")
    fig.colorbar(
        ScalarMappable(cmap=cmap, norm=norm),
        cax=cax,
        location="top",
        label="total nsupers",
    )

    variables = [
        "summary",
        "init",
        "timestep",
        "timestep_sdm",
        "timestep_sdm_movement",
        "timestep_sdm_microphysics",
    ]

    for ax, var in zip(axs, variables):
        for buildtype in buildtypes:
            a = 0
            try:
                ds = hfuncs.open_kerneltimer_dataset(
                    path2builds,
                    buildtype,
                    executable,
                    "gbxs",
                    nsupers,
                )
            except FileNotFoundError:
                msg = f"warning: skipping buildtype={buildtype} nsupers={nsupers}"
                print(msg)
                continue

            ngbxs_start = ngbxs_max
            nthreads_start = 1
            while ngbxs_start >= 1:
                while nthreads_start <= nthreads_max:
                    ngbxs = ngbxs_start
                    nthreads = nthreads_start
                    c, x, y, lq, uq = [], [], [], [], []
                    while nthreads >= 1 and ngbxs >= 1:
                        try:
                            total_time = ds[var].sel(nthreads=nthreads, ngbxs=ngbxs)[
                                :, 0
                            ]
                            c.append(ngbxs * nsupers)
                            x.append(nthreads)
                            y.append(total_time[0].values)
                            lq.append(total_time[2].values)
                            uq.append(total_time[3].values)
                        except KeyError:
                            msg = f"warning: skipping buildtype={buildtype} nsupers={nsupers} ngbxs={ngbxs} nthreads={nthreads}"
                            print(msg)
                        nthreads = nthreads / 2
                        ngbxs = ngbxs / 2
                    llab = None
                    if a == 0:
                        llab = f"{buildtype}"
                    if len(x) == 1:
                        c = c[0]
                    ax.plot(
                        x, y, linestyle=lstyles[buildtype], label=llab, c="lightgrey"
                    )
                    ax.scatter(
                        x,
                        y,
                        marker=markers[buildtype],
                        c=c,
                        cmap=cmap,
                        norm=norm,
                    )
                    hfuncs.add_shading(ax, x, lq, uq, "lightgrey", lstyles[buildtype])

                    a += 1
                    nthreads_start = nthreads_start * 2
                ngbxs_start = ngbxs_start / 2
                nthreads_start = nthreads_max
        ax.set_title(var)
        ax.set_ylabel("wall clock time /s")
    axs[0].legend()
    for ax in axs[:-1]:
        ax.set_xticklabels([])
    axs[-1].set_xlabel("number of CPU threads")

    fig.tight_layout()
    fig.subplots_adjust(top=0.94)

    return fig, axs


# %% funtion definitions for weak scaling plots
def plot_weak_scaling_speedup(
    path2builds: Path,
    buildtypes: list[str],
    buildtype_reference: str,
    nthreads_reference: int,
    executable: str,
    nsupers: int,
    ngbxs_max: int,
    nthreads_max: int,
    cmap,
    norm,
):
    fig = plt.figure(figsize=(16, 20))
    gs = GridSpec(4, 2, figure=fig, height_ratios=[0.25, 7, 7, 7])
    cax = fig.add_subplot(gs[0, :])
    axs = []
    for j in range(2):
        for i in range(1, 4):
            axs.append(fig.add_subplot(gs[i, j]))
    for ax in axs:
        ax.spines[["right", "top"]].set_visible(False)
        # ax.set_aspect("equal")

    fig.suptitle("Weak Scaling: Speedup")
    fig.colorbar(
        ScalarMappable(cmap=cmap, norm=norm),
        cax=cax,
        location="top",
        label="total nsupers",
    )

    variables = [
        "summary",
        "init",
        "timestep",
        "timestep_sdm",
        "timestep_sdm_movement",
        "timestep_sdm_microphysics",
    ]

    ref = hfuncs.open_kerneltimer_dataset(
        path2builds,
        buildtype_reference,
        executable,
        "gbxs",
        nsupers,
    )

    for ax, var in zip(axs, variables):
        for buildtype in buildtypes:
            a = 0
            try:
                ds = hfuncs.open_kerneltimer_dataset(
                    path2builds,
                    buildtype,
                    executable,
                    "gbxs",
                    nsupers,
                )
            except FileNotFoundError:
                msg = f"warning: skipping buildtype={buildtype} nsupers={nsupers}"
                print(msg)
                continue

            ngbxs_start = ngbxs_max
            nthreads_start = 1
            while ngbxs_start >= 1:
                while nthreads_start <= nthreads_max:
                    ngbxs = ngbxs_start
                    nthreads = nthreads_start
                    c, x, y, lq, uq = [], [], [], [], []
                    while nthreads >= 1 and ngbxs >= 1:
                        try:
                            total_time = ds[var].sel(nthreads=nthreads, ngbxs=ngbxs)[
                                :, 0
                            ]
                        except KeyError:
                            total_time = None
                            msg = f"warning: skipping buildtype={buildtype} nsupers={nsupers} ngbxs={ngbxs} nthreads={nthreads}"
                            print(msg)
                        if total_time is not None:
                            if ngbxs in ref.ngbxs:
                                total_time_ref = ref[var].sel(
                                    nthreads=nthreads_reference, ngbxs=ngbxs
                                )[:, 0]
                            else:
                                total_time_ref = ref[var].sel(
                                    nthreads=nthreads_reference
                                )[:, :, 0]
                                total_time_ref = hfuncs.extrapolate_ngbxs_coord(
                                    total_time_ref, ds.ngbxs
                                )
                                total_time_ref = total_time_ref.sel(ngbxs=ngbxs)
                            c.append(ngbxs * nsupers)
                            x.append(nthreads)
                            y.append(
                                hfuncs.calculate_speedup(
                                    total_time[0].values, total_time_ref[0]
                                )
                            )
                            lq.append(
                                hfuncs.calculate_speedup(
                                    total_time[3].values, total_time_ref[2]
                                )
                            )
                            uq.append(
                                hfuncs.calculate_speedup(
                                    total_time[2].values, total_time_ref[3]
                                )
                            )
                        nthreads = nthreads / 2
                        ngbxs = ngbxs / 2
                    llab = None
                    if a == 0:
                        llab = f"{buildtype}"
                    if len(x) == 1:
                        c = c[0]
                    ax.plot(
                        x, y, linestyle=lstyles[buildtype], label=llab, c="lightgrey"
                    )
                    ax.scatter(
                        x,
                        y,
                        marker=markers[buildtype],
                        c=c,
                        cmap=cmap,
                        norm=norm,
                    )
                    hfuncs.add_shading(ax, x, lq, uq, "lightgrey", lstyles[buildtype])

                    a += 1
                    nthreads_start = nthreads_start * 2
                ngbxs_start = ngbxs_start / 2
                nthreads_start = nthreads_max
        ax.set_title(var)
        ax.set_ylabel("speedup")
    axs[0].legend()
    for ax in axs[:-1]:
        ax.set_xticklabels([])
    axs[-1].set_xlabel("number of CPU threads")

    fig.tight_layout()
    fig.subplots_adjust(top=0.94)

    return fig, axs


# %% funtion definitions for weak scaling plots
def plot_weak_scaling_efficiency(
    path2builds: Path,
    buildtypes: list[str],
    buildtype_reference: str,
    nthreads_reference: int,
    executable: str,
    nsupers: int,
    ngbxs_max: int,
    nthreads_max: int,
    cmap,
    norm,
):
    fig = plt.figure(figsize=(16, 20))
    gs = GridSpec(4, 2, figure=fig, height_ratios=[0.25, 7, 7, 7])
    cax = fig.add_subplot(gs[0, :])
    axs = []
    for j in range(2):
        for i in range(1, 4):
            axs.append(fig.add_subplot(gs[i, j]))
    for ax in axs:
        ax.spines[["right", "top"]].set_visible(False)

    fig.suptitle("Weak Scaling: Efficiency")
    fig.colorbar(
        ScalarMappable(cmap=cmap, norm=norm),
        cax=cax,
        location="top",
        label="total nsupers",
    )

    variables = [
        "summary",
        "init",
        "timestep",
        "timestep_sdm",
        "timestep_sdm_movement",
        "timestep_sdm_microphysics",
    ]

    ref = hfuncs.open_kerneltimer_dataset(
        path2builds,
        buildtype_reference,
        executable,
        "gbxs",
        nsupers,
    )

    for ax, var in zip(axs, variables):
        for buildtype in buildtypes:
            a = 0
            try:
                ds = hfuncs.open_kerneltimer_dataset(
                    path2builds,
                    buildtype,
                    executable,
                    "gbxs",
                    nsupers,
                )
            except FileNotFoundError:
                msg = f"warning: skipping buildtype={buildtype} nsupers={nsupers}"
                print(msg)
                continue

            ngbxs_start = ngbxs_max
            nthreads_start = 1
            while ngbxs_start >= 1:
                while nthreads_start <= nthreads_max:
                    ngbxs = ngbxs_start
                    nthreads = nthreads_start
                    c, x, y, lq, uq = [], [], [], [], []
                    while nthreads >= 1 and ngbxs >= 1:
                        try:
                            total_time = ds[var].sel(nthreads=nthreads, ngbxs=ngbxs)[
                                :, 0
                            ]
                        except KeyError:
                            total_time = None
                            msg = f"warning: skipping buildtype={buildtype} nsupers={nsupers} ngbxs={ngbxs} nthreads={nthreads}"
                            print(msg)
                        if total_time is not None:
                            if ngbxs in ref.ngbxs:
                                total_time_ref = ref[var].sel(
                                    nthreads=nthreads_reference, ngbxs=ngbxs
                                )[:, 0]
                            else:
                                total_time_ref = ref[var].sel(
                                    nthreads=nthreads_reference
                                )[:, :, 0]
                                total_time_ref = hfuncs.extrapolate_ngbxs_coord(
                                    total_time_ref, ds.ngbxs
                                )
                                total_time_ref = total_time_ref.sel(ngbxs=ngbxs)
                            c.append(ngbxs * nsupers)
                            x.append(nthreads)
                            y.append(
                                hfuncs.calculate_efficiency(
                                    total_time[0], total_time_ref[0], nthreads
                                )
                            )
                            lq.append(
                                hfuncs.calculate_efficiency(
                                    total_time[3], total_time_ref[2], nthreads
                                )
                            )
                            uq.append(
                                hfuncs.calculate_efficiency(
                                    total_time[2], total_time_ref[3], nthreads
                                )
                            )
                        nthreads = nthreads / 2
                        ngbxs = ngbxs / 2
                    llab = None
                    if a == 0:
                        llab = f"{buildtype}"
                    if len(x) == 1:
                        c = c[0]
                    ax.plot(
                        x, y, linestyle=lstyles[buildtype], label=llab, c="lightgrey"
                    )
                    ax.scatter(
                        x,
                        y,
                        marker=markers[buildtype],
                        c=c,
                        cmap=cmap,
                        norm=norm,
                    )
                    hfuncs.add_shading(ax, x, lq, uq, "lightgrey", lstyles[buildtype])

                    a += 1
                    nthreads_start = nthreads_start * 2
                ngbxs_start = ngbxs_start / 2
                nthreads_start = nthreads_max
        ax.set_title(var)
        ax.set_ylabel("efficiency")
    for ax in axs:
        ax.set_xlim([0, None])
        ax.hlines(
            1.0,
            ax.get_xlim()[0],
            ax.get_xlim()[1],
            color="grey",
            linewidth=0.8,
            label="benchmark",
        )
        ax.set_ylim([0.0, 1.0])

    axs[0].legend()
    for ax in axs[:-1]:
        ax.set_xticklabels([])
    axs[-1].set_xlabel("number of CPU threads")

    fig.tight_layout()
    fig.subplots_adjust(top=0.94)

    return fig, axs


# %%
for nsupers in nsupers_per_gbx:
    fig, axs = plot_weak_scaling_wallclock(
        path2builds,
        all_buildtypes,
        executable,
        nsupers,
        ngbxs_max,
        nthreads_max,
        cmap,
        norm,
    )
    savename = savedir / f"weak_scaling_wallclock_nsupers{nsupers}_gbxsensemble.png"
    hfuncs.savefig(savename, tight=False)

# %%
for nsupers in nsupers_per_gbx:
    fig, axs = plot_weak_scaling_speedup(
        path2builds,
        buildtypes,
        buildtype_reference,
        nthreads_reference,
        executable,
        nsupers,
        ngbxs_max,
        nthreads_max,
        cmap,
        norm,
    )
    savename = savedir / f"weak_scaling_speedup_nsupers{nsupers}_gbxsensemble.png"
    hfuncs.savefig(savename, tight=False)

# %%
for nsupers in nsupers_per_gbx:
    fig, axs = plot_weak_scaling_efficiency(
        path2builds,
        buildtypes,
        buildtype_reference,
        nthreads_reference,
        executable,
        nsupers,
        ngbxs_max,
        nthreads_max,
        cmap,
        norm,
    )
    savename = savedir / f"weak_scaling_efficiency_nsupers{nsupers}_gbxsensemble.png"
    hfuncs.savefig(savename, tight=False)

# %%
for nsupers in nsupers_per_gbx:
    for b in buildtypes:
        fig, axs = plot_weak_scaling_wallclock(
            path2builds,
            [b],
            executable,
            nsupers,
            ngbxs_max,
            nthreads_max,
            cmap,
            norm,
        )
        savename = (
            savedir / f"weak_scaling_wallclock_nsupers{nsupers}_{b}_gbxsensemble.png"
        )
        hfuncs.savefig(savename, tight=False)

        fig, axs = plot_weak_scaling_speedup(
            path2builds,
            [b],
            buildtype_reference,
            nthreads_reference,
            executable,
            nsupers,
            ngbxs_max,
            nthreads_max,
            cmap,
            norm,
        )
        savename = (
            savedir / f"weak_scaling_speedup_nsupers{nsupers}_{b}_gbxsensemble.png"
        )
        hfuncs.savefig(savename, tight=False)

        fig, axs = plot_weak_scaling_efficiency(
            path2builds,
            [b],
            buildtype_reference,
            nthreads_reference,
            executable,
            nsupers,
            ngbxs_max,
            nthreads_max,
            cmap,
            norm,
        )
        savename = (
            savedir / f"weak_scaling_efficiency_nsupers{nsupers}_{b}_gbxsensemble.png"
        )
        hfuncs.savefig(savename, tight=False)
# %%
