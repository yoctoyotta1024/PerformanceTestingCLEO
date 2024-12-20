"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: basic_kerneltimer_metrics.py
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
Script for plotting basic performance scaling results for a given build
from zarr xarray datasets for kokkos kernel timer profiling data.
Note: standard data format assumed.
"""

# %%
import argparse
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
    default="/work/bm1183/m300950/performance_testing_cleo/builds/",
)
parser.add_argument(
    "--executable",
    type=str,
    choices=["colls0d"],
    help="Executable name, e.g. colls0d",
    default="colls0d",
)
parser.add_argument(
    "--buildtype",
    type=str,
    choices=["serial", "openmp", "cuda", "threads"],
    help="Type of build: serial, openmp, cuda or threads",
    default="openmp",
)
args, unknown = parser.parse_known_args()

buildtype = args.buildtype
buildtype_references = "serial"
nsupers_per_gbx = [1, 16]
lstyles = hfuncs.buildtype_lstyles
markers = hfuncs.buildtype_markers

savedir = Path("/home/m/m300950/performance_testing_cleo/plots/")

processing_units = {
    # TODO(CB): get from kokkos configuration statement during runtime so efficiency
    # calculatin is not only a rough calculation
    "serial": 1,
    "threads": 1,
    "openmp": 256,
    "cuda": 6912,
}


# %% funtion definitions for kernel timer plots
def plot_speedup_scaling(
    datasets: dict, references: dict, buildtype: str, buildtype_references: str
):
    fig, axs = hfuncs.subplots(figsize=(12, 20), nrows=3, logx=True)
    fig.suptitle(f"{buildtype} compared to {buildtype_references}")

    for nsupers in datasets.keys():
        ds = datasets[nsupers]
        ref = references[nsupers]

        total_time = ds.summary[:, 0, 0]
        total_time_ref = ref.summary[:, 0, 0]
        speedup = hfuncs.calculate_speedup(
            total_time,
            total_time_ref,
            extrapolate=True,
        )

        axs[0].plot(
            ds.ngbxs,
            speedup,
            marker=markers[buildtype],
            linestyle=lstyles[buildtype],
            label=f"nsupers={nsupers}",
        )
    axs[0].set_title("total runtime")

    for nsupers in datasets.keys():
        ds = datasets[nsupers]
        ref = references[nsupers]

        total_time = ds.init[:, 0, 0]
        total_time_ref = ref.init[:, 0, 0]
        speedup = hfuncs.calculate_speedup(
            total_time,
            total_time_ref,
            extrapolate=True,
        )

        axs[1].plot(
            ds.ngbxs,
            speedup,
            marker=markers[buildtype],
            linestyle=lstyles[buildtype],
            label=f"nsupers={nsupers}",
        )
    axs[1].set_title("initialisation")

    for nsupers in datasets.keys():
        ds = datasets[nsupers]
        ref = references[nsupers]

        total_time = ds.timestep[:, 0, 0]
        total_time_ref = ref.timestep[:, 0, 0]
        speedup = hfuncs.calculate_speedup(
            total_time,
            total_time_ref,
            extrapolate=True,
        )

        axs[2].plot(
            ds.ngbxs,
            speedup,
            marker=markers[buildtype],
            linestyle=lstyles[buildtype],
            label=f"nsupers={nsupers}",
        )
    axs[2].set_title("timestepping")

    for ax in axs:
        ax.hlines(
            1.0,
            ds.ngbxs[0],
            ds.ngbxs[-1],
            color="grey",
            linewidth=0.8,
            label="benchmark",
        )
        ax.set_ylabel("wallclock time speedup")
    axs[0].legend()
    axs[-1].set_xlabel("number of gridboxes")

    return fig, axs


def plot_rough_efficiency_scaling(
    datasets: dict, references: dict, buildtype: str, buildtype_references: str
):
    fig, axs = hfuncs.subplots(figsize=(12, 20), nrows=3, logx=True)
    fig.suptitle(f"{buildtype} compared to {buildtype_references}")

    for nsupers in datasets.keys():
        ds = datasets[nsupers]
        ref = references[nsupers]

        total_time = ds.summary[:, 0, 0]
        total_time_ref = ref.summary[:, 0, 0]
        efficiency = hfuncs.calculate_efficiency(
            total_time,
            total_time_ref,
            buildtype,
            processing_units,
            extrapolate=True,
        )

        axs[0].plot(
            ds.ngbxs,
            efficiency,
            marker=markers[buildtype],
            linestyle=lstyles[buildtype],
            label=f"nsupers={nsupers}",
        )
    axs[0].set_title("total runtime")

    for nsupers in datasets.keys():
        ds = datasets[nsupers]
        ref = references[nsupers]

        total_time = ds.init[:, 0, 0]
        total_time_ref = ref.init[:, 0, 0]
        efficiency = hfuncs.calculate_efficiency(
            total_time,
            total_time_ref,
            buildtype,
            processing_units,
            extrapolate=True,
        )

        axs[1].plot(
            ds.ngbxs,
            efficiency,
            marker=markers[buildtype],
            linestyle=lstyles[buildtype],
            label=f"nsupers={nsupers}",
        )
    axs[1].set_title("initialisation")

    for nsupers in datasets.keys():
        ds = datasets[nsupers]
        ref = references[nsupers]

        total_time = ds.timestep[:, 0, 0]
        total_time_ref = ref.timestep[:, 0, 0]
        efficiency = hfuncs.calculate_efficiency(
            total_time,
            total_time_ref,
            buildtype,
            processing_units,
            extrapolate=True,
        )

        axs[2].plot(
            ds.ngbxs,
            efficiency,
            marker=markers[buildtype],
            linestyle=lstyles[buildtype],
            label=f"nsupers={nsupers}",
        )
    axs[2].set_title("timestepping")

    for ax in axs:
        ax.hlines(
            1.0,
            ds.ngbxs[0],
            ds.ngbxs[-1],
            color="grey",
            linewidth=0.8,
            label="benchmark",
        )
        ax.set_ylabel("wallclock time efficiency")
    axs[0].legend()
    axs[-1].set_xlabel("number of gridboxes")

    return fig, axs


# %% load data
datasets = {}
references = {}
for nsupers in nsupers_per_gbx:
    datasets[nsupers] = hfuncs.open_kerneltimer_dataset(
        args.path2builds, buildtype, args.executable, nsupers
    )
    references[nsupers] = hfuncs.open_kerneltimer_dataset(
        args.path2builds, buildtype_references, args.executable, nsupers
    )

# %%
fig, axs = plot_speedup_scaling(datasets, references, buildtype, buildtype_references)
savename = savedir / f"speedup_{buildtype}.png"
hfuncs.savefig(savename)

# %%
fig, axs = plot_rough_efficiency_scaling(
    datasets, references, buildtype, buildtype_references
)
savename = savedir / f"efficiency_{buildtype}.png"
hfuncs.savefig(savename)
