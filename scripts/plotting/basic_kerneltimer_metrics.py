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
nthreads_reference = 1

ensembletype = "supers"
fixed_ensemb_vals = [1]

lstyles = hfuncs.buildtype_lstyles
markers = hfuncs.buildtype_markers

savedir = Path("/home/m/m300950/performance_testing_cleo/plots/")


# %% funtion definitions for kernel timer plots
def domain_totnsupers(data):
    try:
        x = data.attrs["nsupers"] * data.ngbxs
    except KeyError:
        x = data.attrs["ngbxs"] * data.nsupers
    return x


def plot_speedup_scaling(
    datasets: dict,
    references: dict,
    buildtype: str,
    buildtype_references: str,
    nthreads_ref: int,
    ensembletype: str,
):
    fig, axs = hfuncs.subplots(figsize=(12, 20), nrows=3, logx=True)
    fig.suptitle(f"{buildtype} compared to {buildtype_references}")

    for n in datasets.keys():
        ds = datasets[n]
        ref = references[n]
        for nthreads in ds.nthreads:
            x = domain_totnsupers(ds)
            total_time = ds.summary.sel(nthreads=nthreads)[:, 0, 0]
            total_time_ref = ref.summary.sel(nthreads=nthreads_ref)[:, 0, 0]
            speedup = hfuncs.calculate_speedup(
                total_time, total_time_ref, extrapolate=True, coord=f"n{ensembletype}"
            )

            axs[0].plot(
                x,
                speedup,
                marker=markers[buildtype],
                linestyle=lstyles[buildtype],
                label=f"n={n}, nthreads={nthreads.values}",
            )
    axs[0].set_title("total runtime")

    for n in datasets.keys():
        ds = datasets[n]
        ref = references[n]
        for nthreads in ds.nthreads:
            x = domain_totnsupers(ds)
            total_time = ds.init.sel(nthreads=nthreads)[:, 0, 0]
            total_time_ref = ref.init.sel(nthreads=nthreads_ref)[:, 0, 0]
            speedup = hfuncs.calculate_speedup(
                total_time, total_time_ref, extrapolate=True, coord=f"n{ensembletype}"
            )

            axs[1].plot(
                x,
                speedup,
                marker=markers[buildtype],
                linestyle=lstyles[buildtype],
                label=f"n={n}, nthreads={nthreads.values}",
            )
    axs[1].set_title("initialisation")

    for ns in datasets.keys():
        ds = datasets[n]
        ref = references[n]

        for nthreads in ds.nthreads:
            x = domain_totnsupers(ds)
            total_time = ds.timestep.sel(nthreads=nthreads)[:, 0, 0]
            total_time_ref = ref.timestep.sel(nthreads=nthreads_ref)[:, 0, 0]
            speedup = hfuncs.calculate_speedup(
                total_time, total_time_ref, extrapolate=True, coord=f"n{ensembletype}"
            )

            axs[2].plot(
                x,
                speedup,
                marker=markers[buildtype],
                linestyle=lstyles[buildtype],
                label=f"n={n}, nthreads={nthreads.values}",
            )
    axs[2].set_title("timestepping")

    for ax in axs:
        ax.hlines(
            1.0,
            ax.get_xlim()[0],
            ax.get_xlim()[-1],
            color="grey",
            linewidth=0.8,
            label="benchmark",
        )
        ax.set_ylabel("wallclock time speedup")
    axs[0].legend()
    axs[-1].set_xlabel("total superpdroplets in domain")

    fig.tight_layout()
    fig.subplots_adjust(top=0.95)

    return fig, axs


def plot_nthreads_efficiency_scaling(
    datasets: dict,
    references: dict,
    buildtype: str,
    buildtype_references: str,
    nthreads_ref: int,
    ensembletype: str,
):
    fig, axs = hfuncs.subplots(figsize=(12, 20), nrows=3, logx=True)
    fig.suptitle(f"{buildtype} compared to {buildtype_references}")

    for n in datasets.keys():
        ds = datasets[n]
        ref = references[n]
        for nthreads in ds.nthreads:
            x = domain_totnsupers(ds)
            total_time = ds.summary.sel(nthreads=nthreads)[:, 0, 0]
            total_time_ref = ref.summary.sel(nthreads=nthreads_ref)[:, 0, 0]
            efficiency = hfuncs.calculate_efficiency(
                total_time,
                total_time_ref,
                nthreads,
                extrapolate=True,
                coord=f"n{ensembletype}",
            )

            axs[0].plot(
                x,
                efficiency,
                marker=markers[buildtype],
                linestyle=lstyles[buildtype],
                label=f"n={n}, nthreads={nthreads.values}",
            )
    axs[0].set_title("total runtime")

    for n in datasets.keys():
        ds = datasets[n]
        ref = references[n]
        for nthreads in ds.nthreads:
            x = domain_totnsupers(ds)
            total_time = ds.init.sel(nthreads=nthreads)[:, 0, 0]
            total_time_ref = ref.init.sel(nthreads=nthreads_ref)[:, 0, 0]
            efficiency = hfuncs.calculate_efficiency(
                total_time,
                total_time_ref,
                nthreads,
                extrapolate=True,
                coord=f"n{ensembletype}",
            )

            axs[1].plot(
                x,
                efficiency,
                marker=markers[buildtype],
                linestyle=lstyles[buildtype],
                label=f"n={n}, nthreads={nthreads.values}",
            )
    axs[1].set_title("initialisation")

    for n in datasets.keys():
        ds = datasets[n]
        ref = references[n]
        for nthreads in ds.nthreads:
            x = domain_totnsupers(ds)
            total_time = ds.timestep.sel(nthreads=nthreads)[:, 0, 0]
            total_time_ref = ref.timestep.sel(nthreads=nthreads_ref)[:, 0, 0]
            efficiency = hfuncs.calculate_efficiency(
                total_time,
                total_time_ref,
                nthreads,
                extrapolate=True,
                coord=f"n{ensembletype}",
            )

            axs[2].plot(
                x,
                efficiency,
                marker=markers[buildtype],
                linestyle=lstyles[buildtype],
                label=f"n={n}, nthreads={nthreads.values}",
            )
    axs[2].set_title("timestepping")

    for ax in axs:
        ax.hlines(
            1.0,
            ax.get_xlim()[0],
            ax.get_xlim()[-1],
            color="grey",
            linewidth=0.8,
            label="benchmark",
        )
        ax.set_ylabel("wallclock time efficiency")
    axs[0].legend()
    axs[-1].set_xlabel("total superdroplets in domain")

    fig.tight_layout()
    fig.subplots_adjust(top=0.95)

    return fig, axs


# %% load data
datasets = {}
references = {}
for n in fixed_ensemb_vals:
    datasets[n] = hfuncs.open_kerneltimer_dataset(
        args.path2builds, buildtype, args.executable, ensembletype, n
    )
    references[n] = hfuncs.open_kerneltimer_dataset(
        args.path2builds, buildtype_references, args.executable, ensembletype, n
    )

# %%
fig, axs = plot_speedup_scaling(
    datasets,
    references,
    buildtype,
    buildtype_references,
    nthreads_reference,
    ensembletype,
)
savename = savedir / f"speedup_{buildtype}_{ensembletype}ensemble.png"
hfuncs.savefig(savename, tight=False)
# %%
fig, axs = plot_nthreads_efficiency_scaling(
    datasets,
    references,
    buildtype,
    buildtype_references,
    nthreads_reference,
    ensembletype,
)
savename = savedir / f"efficiency_nthreads_{buildtype}_{ensembletype}ensemble.png"
hfuncs.savefig(savename, tight=False)
