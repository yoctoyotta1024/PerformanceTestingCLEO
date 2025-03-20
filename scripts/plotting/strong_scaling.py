"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: strong_scaling.py
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
Script for plotting strong scaling results (increasing reesources for fixed problem size)
from zarr xarray datasets for kokkos profiling data. Note: standard data format assumed.
"""

# %%
import argparse
from pathlib import Path
import sys
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LogNorm

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
    choices=["colls0d", "thermo3d"],
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

lstyles = hfuncs.buildtype_lstyles
markers = hfuncs.buildtype_markers

cmap = plt.get_cmap("plasma")
norm = LogNorm(vmin=1, vmax=1e9)
ngbxs_nsupers_colors = {}
for ngbxs, nsupers in ngbxs_nsupers_runs.keys():
    color = cmap(norm(ngbxs * nsupers))
    ngbxs_nsupers_colors[(ngbxs, nsupers)] = color

savedir = Path("/home/m/m300950/performance_testing_cleo/plots/")


# %% funtion definitions for strong scaling plots
def plot_strong_scaling_wallclock(
    path2builds: Path,
    buildtypes: list[str],
    executable: str,
    ngbxs_nsupers_runs: dict,
):
    fig, axes = hfuncs.subplots(
        figsize=(12, 20), nrows=4, ncols=1, hratios=[0.25] + [7] * 3
    )
    cax = axes[0]
    axs = axes[1:]
    for ax in axs:
        ax.set_xscale("log")
        ax.set_yscale("log")

    fig.suptitle("Strong Scaling: Wall Clock Time")
    fig.colorbar(
        ScalarMappable(cmap=cmap, norm=norm),
        cax=cax,
        location="top",
        label="total nsupers",
    )

    variables = ["summary", "init", "timestep"]

    for ax, var in zip(axs, variables):
        for buildtype in buildtypes:
            a = 0
            for ngbxs, nsupers in ngbxs_nsupers_runs.keys():
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
                try:
                    total_time = ds[var].sel(ngbxs=ngbxs)[:, :, 0]
                except KeyError:
                    msg = f"warning: skipping buildtype={buildtype} ngbxs={ngbxs}, nsupers={nsupers}"
                    print(msg)
                    continue

                x = ds.nthreads
                y = total_time[:, 0]
                lq = total_time[:, 2]
                uq = total_time[:, 3]

                llab = None
                if a == 0:
                    llab = f"{buildtype}, nsupers={nsupers}"
                c = ngbxs_nsupers_colors[(ngbxs, nsupers)]
                ax.plot(
                    x,
                    y,
                    color=c,
                    marker=markers[buildtype],
                    linestyle=lstyles[buildtype],
                    label=llab,
                )
                hfuncs.add_shading(ax, x, lq, uq, c, lstyles[buildtype])
                a += 1
        ax.set_title(var)
        ax.set_ylabel("wall clock time /s")
    axs[0].legend()
    for ax in axs[:-1]:
        ax.set_xticklabels([])
    axs[-1].set_xlabel("number of CPU threads")

    fig.tight_layout()
    fig.subplots_adjust(top=0.94)

    return fig, axs


# %% funtion definitions for strong scaling plots
def plot_strong_scaling_speedup(
    path2builds: Path,
    buildtypes: list[str],
    buildtype_reference: str,
    nthreads_reference: int,
    executable: str,
    ngbxs_nsupers_runs: dict,
):
    fig, axes = hfuncs.subplots(
        figsize=(10, 20), nrows=4, ncols=1, hratios=[0.25] + [7] * 3
    )
    cax = axes[0]
    axs = axes[1:]
    for ax in axs:
        ax.set_aspect("equal")

    fig.suptitle("Strong Scaling: Speedup")
    fig.colorbar(
        ScalarMappable(cmap=cmap, norm=norm),
        cax=cax,
        location="top",
        label="total nsupers",
    )

    variables = ["summary", "init", "timestep"]

    for ax, var in zip(axs, variables):
        for buildtype in buildtypes:
            a = 0
            for ngbxs, nsupers in ngbxs_nsupers_runs.keys():
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
                try:
                    total_time = ds[var].sel(ngbxs=ngbxs)[:, :, 0]
                except KeyError:
                    msg = f"warning: skipping buildtype={buildtype} ngbxs={ngbxs}, nsupers={nsupers}"
                    print(msg)
                    continue

                ref = hfuncs.open_kerneltimer_dataset(
                    path2builds,
                    buildtype_reference,
                    executable,
                    "gbxs",
                    nsupers,
                )
                if ngbxs in ref.ngbxs:
                    total_time_ref = ref[var].sel(
                        ngbxs=ngbxs, nthreads=nthreads_reference
                    )[:, 0]
                else:
                    total_time_ref = ref[var].sel(nthreads=nthreads_reference)[:, :, 0]
                    total_time_ref = hfuncs.extrapolate_ngbxs_coord(
                        total_time_ref, ds.ngbxs
                    )
                    total_time_ref = total_time_ref.sel(ngbxs=ngbxs)

                x = ds.nthreads
                y = hfuncs.calculate_speedup(total_time[:, 0], total_time_ref[0])
                lq = hfuncs.calculate_speedup(total_time[:, 3], total_time_ref[2])
                uq = hfuncs.calculate_speedup(total_time[:, 2], total_time_ref[3])

                llab = None
                if a == 0:
                    llab = f"{buildtype}, nsupers={nsupers}"
                c = ngbxs_nsupers_colors[(ngbxs, nsupers)]
                ax.plot(
                    x,
                    y,
                    color=c,
                    marker=markers[buildtype],
                    linestyle=lstyles[buildtype],
                    label=llab,
                )
                hfuncs.add_shading(ax, x, lq, uq, c, lstyles[buildtype])
                a += 1
        ax.set_title(var)
        ax.set_ylabel("speedup")
    axs[0].legend()
    for ax in axs[:-1]:
        ax.set_xticklabels([])
    axs[-1].set_xlabel("number of CPU threads")

    fig.tight_layout()
    fig.subplots_adjust(top=0.94)

    return fig, axs


# %% funtion definitions for strong scaling plots
def plot_strong_scaling_nthreads_efficiency(
    path2builds: Path,
    buildtypes: list[str],
    buildtype_reference: str,
    nthreads_reference: int,
    executable: str,
    ngbxs_nsupers_runs: dict,
):
    fig, axes = hfuncs.subplots(
        figsize=(12, 20), nrows=4, ncols=1, hratios=[0.25] + [7] * 3
    )

    cax = axes[0]
    axs = axes[1:]

    fig.suptitle("Strong Scaling: Efficiency")
    fig.colorbar(
        ScalarMappable(cmap=cmap, norm=norm),
        cax=cax,
        location="top",
        label="total nsupers",
    )

    variables = ["summary", "init", "timestep"]

    for ax, var in zip(axs, variables):
        for buildtype in buildtypes:
            a = 0
            for ngbxs, nsupers in ngbxs_nsupers_runs.keys():
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
                try:
                    total_time = ds[var].sel(ngbxs=ngbxs)[:, :, 0]
                except KeyError:
                    msg = f"warning: skipping buildtype={buildtype} ngbxs={ngbxs}, nsupers={nsupers}"
                    print(msg)
                    total_time = None
                    continue

                ref = hfuncs.open_kerneltimer_dataset(
                    path2builds,
                    buildtype_reference,
                    executable,
                    "gbxs",
                    nsupers,
                )
                if ngbxs in ref.ngbxs:
                    total_time_ref = ref[var].sel(
                        ngbxs=ngbxs, nthreads=nthreads_reference
                    )[:, 0]
                else:
                    total_time_ref = ref[var].sel(nthreads=nthreads_reference)[:, :, 0]
                    total_time_ref = hfuncs.extrapolate_ngbxs_coord(
                        total_time_ref, ds.ngbxs
                    )
                    total_time_ref = total_time_ref.sel(ngbxs=ngbxs)

                x = ds.nthreads
                y = hfuncs.calculate_efficiency(
                    total_time[:, 0], total_time_ref[0], ds.nthreads
                )
                lq = hfuncs.calculate_efficiency(
                    total_time[:, 3], total_time_ref[2], ds.nthreads
                )
                uq = hfuncs.calculate_efficiency(
                    total_time[:, 2], total_time_ref[3], ds.nthreads
                )

                llab = None
                if a == 0:
                    llab = f"{buildtype}, nsupers={nsupers}"
                c = ngbxs_nsupers_colors[(ngbxs, nsupers)]
                ax.plot(
                    x,
                    y,
                    color=c,
                    marker=markers[buildtype],
                    linestyle=lstyles[buildtype],
                    label=llab,
                )
                hfuncs.add_shading(ax, x, lq, uq, c, lstyles[buildtype])
                a += 1
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
fig, axs = plot_strong_scaling_wallclock(
    path2builds, all_buildtypes, executable, ngbxs_nsupers_runs
)
savename = savedir / "strong_scaling_wallclock_gbxsensemble.png"
hfuncs.savefig(savename, tight=False)

# %%
fig, axs = plot_strong_scaling_speedup(
    path2builds,
    buildtypes,
    buildtype_reference,
    nthreads_reference,
    executable,
    ngbxs_nsupers_runs,
)
savename = savedir / "strong_scaling_speedup_gbxsensemble.png"
hfuncs.savefig(savename, tight=False)

# %%
fig, axs = plot_strong_scaling_nthreads_efficiency(
    path2builds,
    buildtypes,
    buildtype_reference,
    nthreads_reference,
    executable,
    ngbxs_nsupers_runs,
)
savename = savedir / "strong_scaling_efficiency_nthreads_gbxsensemble.png"
hfuncs.savefig(savename, tight=False)

# %%
for b in buildtypes:
    fig, axs = plot_strong_scaling_wallclock(
        path2builds, [b], executable, ngbxs_nsupers_runs
    )
    savename = savedir / f"strong_scaling_wallclock_{b}_gbxsensemble.png"
    hfuncs.savefig(savename, tight=False)

    fig, axs = plot_strong_scaling_speedup(
        path2builds,
        [b],
        buildtype_reference,
        nthreads_reference,
        executable,
        ngbxs_nsupers_runs,
    )
    savename = savedir / f"strong_scaling_speedup_{b}_gbxsensemble.png"
    hfuncs.savefig(savename, tight=False)

    fig, axs = plot_strong_scaling_nthreads_efficiency(
        path2builds,
        [b],
        buildtype_reference,
        nthreads_reference,
        executable,
        ngbxs_nsupers_runs,
    )
    savename = savedir / f"strong_scaling_efficiency_nthreads_{b}_gbxsensemble.png"
    hfuncs.savefig(savename, tight=False)
