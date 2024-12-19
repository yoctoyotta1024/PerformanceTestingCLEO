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
import numpy as np
from pathlib import Path
import sys

path2src = Path(__file__).resolve().parent.parent.parent / "src"
sys.path.append(str(path2src))  # for imports for input files generation
from plotting import helperfuncs as hfuncs

# e.g. ipykernel_launcher.py [path2builds] [executable]
parser = argparse.ArgumentParser()
parser.add_argument(
    "--path2builds",
    type=Path,
    help="Absolute path to builds",
    default="/work/bm1183/m300950/performance_testing_cleo/thirdattempt_strongscaling",
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

all_buildtypes = ["serial", "openmp", "threads", "cuda"]
buildtypes = ["openmp", "threads", "cuda"]
buildtype_reference = "serial"
nthreads_reference = 1

nthreads = [1, 8, 16, 64, 128, 256]

ngbxs_nsupers_runs = {
    (4096, 16): 1,
    (8192, 16): 1,
    (16384, 16): 1,
    (262144, 16): 1,
}

lstyles = hfuncs.buildtype_lstyles
markers = hfuncs.buildtype_markers

ngbxs_nsupers_colours = {
    (4096, 16): "firebrick",
    (8192, 16): "orange",
    (16384, 16): "gold",
    (262144, 16): "limegreen",
}

savedir = Path("/home/m/m300950/performance_testing_cleo/plots/")


# %% funtion definitions for strong scaling plots
def plot_strong_scaling_wallclock(
    path2builds: Path,
    buildtypes: list[str],
    executable: str,
    ngbxs_nsupers_runs: dict,
    nthreads2plt: list[int],
):
    fig, axs = hfuncs.subplots(
        figsize=(12, 20), nrows=3, sharex=True, logx=True, logy=True
    )

    variables = ["summary", "init", "timestep"]

    for ax, var in zip(axs, variables):
        for buildtype in buildtypes:
            for ngbxs, nsupers in ngbxs_nsupers_runs.keys():
                x, yarr = [], []
                for nthreads in nthreads2plt:
                    try:
                        ds = hfuncs.open_kerneltimer_dataset(
                            path2builds,
                            buildtype,
                            executable,
                            nsupers,
                            nthreads=nthreads,
                        )
                    except FileNotFoundError:
                        msg = f"warning: skipping buildtype={buildtype} nsupers={nsupers}, nthreads={nthreads}"
                        print(msg)
                        continue
                    try:
                        total_time = ds[var].sel(ngbxs=ngbxs)[:, 0]
                    except KeyError:
                        msg = f"warning: skipping buildtype={buildtype} ngbxs={ngbxs}, nsupers={nsupers}, nthreads={nthreads}"
                        print(msg)
                        continue
                    x.append(nthreads)
                    yarr.append(total_time)
                if x != []:
                    x = np.asarray(x)
                    yarr = np.asarray(yarr)
                    y = yarr[:, 0]
                    lq = yarr[:, 2]
                    uq = yarr[:, 3]
                    lab = f"{buildtype} ngbxs={ngbxs} nsupers={nsupers}"
                    c = ngbxs_nsupers_colours[(ngbxs, nsupers)]
                    ax.plot(
                        x,
                        y,
                        color=c,
                        marker=markers[buildtype],
                        linestyle=lstyles[buildtype],
                        label=lab,
                    )
                    hfuncs.add_shading(ax, x, lq, uq, c, lstyles[buildtype])
        ax.legend()
        ax.set_title(var)
        ax.set_ylabel("wall clock time /s")
    axs[-1].set_xlabel("number of CPU threads")

    return fig, axs


# %% funtion definitions for strong scaling plots
def plot_strong_scaling_speedup(
    path2builds: Path,
    buildtypes: list[str],
    buildtype_reference: str,
    executable: str,
    ngbxs_nsupers_runs: dict,
    nthreads2plt: list[int],
    nthreads_reference: int,
):
    fig, axs = hfuncs.subplots(
        figsize=(12, 20), nrows=3, sharex=True, logx=False, logy=False
    )

    variables = ["summary", "init", "timestep"]

    for ax, var in zip(axs, variables):
        for buildtype in buildtypes:
            for ngbxs, nsupers in ngbxs_nsupers_runs.keys():
                ref = hfuncs.open_kerneltimer_dataset(
                    path2builds,
                    buildtype_reference,
                    executable,
                    nsupers,
                    nthreads=nthreads_reference,
                )
                total_time_ref = ref[var].sel(ngbxs=ngbxs)[:, 0]

                x, y, lq, uq = [], [], [], []
                for nthreads in nthreads2plt:
                    try:
                        ds = hfuncs.open_kerneltimer_dataset(
                            path2builds,
                            buildtype,
                            executable,
                            nsupers,
                            nthreads=nthreads,
                        )
                    except FileNotFoundError:
                        msg = f"warning: skipping buildtype={buildtype} nsupers={nsupers}, nthreads={nthreads}"
                        print(msg)
                        continue
                    try:
                        total_time = ds[var].sel(ngbxs=ngbxs)[:, 0]
                    except KeyError:
                        msg = f"warning: skipping buildtype={buildtype} ngbxs={ngbxs}, nsupers={nsupers}, nthreads={nthreads}"
                        print(msg)
                        continue

                    x.append(nthreads)
                    y.append(hfuncs.calculate_speedup(total_time[0], total_time_ref[0]))
                    lq.append(
                        hfuncs.calculate_speedup(total_time[3], total_time_ref[2])
                    )
                    uq.append(
                        hfuncs.calculate_speedup(total_time[2], total_time_ref[3])
                    )

                if x != []:
                    lab = f"{buildtype} ngbxs={ngbxs} nsupers={nsupers}"
                    c = ngbxs_nsupers_colours[(ngbxs, nsupers)]
                    ax.plot(
                        x,
                        y,
                        color=c,
                        marker=markers[buildtype],
                        linestyle=lstyles[buildtype],
                        label=lab,
                    )
                    hfuncs.add_shading(ax, x, lq, uq, c, lstyles[buildtype])
        ax.legend()
        ax.set_title(var)
        ax.set_ylabel("speedup")
    axs[-1].set_xlabel("number of CPU threads")
    return fig, axs


# %%
fig, axs = plot_strong_scaling_wallclock(
    path2builds, all_buildtypes, executable, ngbxs_nsupers_runs, nthreads
)
savename = savedir / "strong_scaling_wallclock.png"
hfuncs.savefig(savename)

# %%
fig, axs = plot_strong_scaling_speedup(
    path2builds,
    buildtypes,
    buildtype_reference,
    executable,
    ngbxs_nsupers_runs,
    nthreads,
    nthreads_reference,
)
savename = savedir / "strong_scaling_speedup.png"
hfuncs.savefig(savename)

# %%
